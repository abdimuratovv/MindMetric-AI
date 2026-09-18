import { useCallback, useEffect, useRef, useState } from 'react';

import { getAnagramCurrent, guessAnagram, skipAnagram, startAnagram, submitAnagram } from '../../api/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import CompletionOverlay from './CompletionOverlay.jsx';

// Time only counts while the tab is visible and the student touched something recently,
// so leaving an unsolvable anagram open in the background earns nothing.
const IDLE_AFTER_MS = 15_000;
const TICK_MS = 1_000;

const KEYFRAMES = `
@keyframes mm-anagram-shake { 0%,100% { transform: translateX(0) } 20% { transform: translateX(-7px) } 40% { transform: translateX(6px) } 60% { transform: translateX(-4px) } 80% { transform: translateX(3px) } }
@keyframes mm-anagram-pop { 0% { transform: scale(1) } 45% { transform: scale(1.12) } 100% { transform: scale(1) } }
@keyframes mm-anagram-in { from { opacity: 0; transform: translateY(6px) } to { opacity: 1; transform: none } }
`;

const shuffled = (list) => {
  const copy = [...list];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
};

const TOOL_BTN = {
  padding: '9px 16px', borderRadius: '100px', border: '1px solid rgba(31,55,75,0.15)', background: 'rgba(255,255,255,0.6)',
  color: '#2E5570', fontWeight: 700, fontSize: '12.5px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px',
};

/**
 * patience: rearrange letter tiles into a word. Items get harder, and a few have no
 * solution — the server never reveals which. No timer is shown; "Skip" is always
 * available and deliberately neutral. What's measured is active time and distinct
 * attempts on the hard/unsolvable items (see state_tracker._score_anagram).
 */
export default function Anagram({ goTo, onProgress }) {
  const [item, setItem] = useState(null); // {id, letters}
  const [number, setNumber] = useState(1);
  const [total, setTotal] = useState(12);
  const [tiles, setTiles] = useState([]); // [{id, ch}]
  const [slots, setSlots] = useState([]); // tile id per slot, or null
  const [status, setStatus] = useState('idle'); // idle | checking | wrong | correct
  const [completion, setCompletion] = useState(null);
  const { t } = useLanguage();

  const activeMsRef = useRef(0);
  const lastInputRef = useRef(Date.now());
  const busyRef = useRef(false);

  const loadCurrent = useCallback(async () => {
    const current = await getAnagramCurrent();
    if (!current.item) {
      setCompletion(await submitAnagram());
      return;
    }
    setItem(current.item);
    setNumber(current.number);
    setTotal(current.total);
    setTiles(current.item.letters.map((ch, i) => ({ id: i, ch })));
    setSlots(current.item.letters.map(() => null));
    setStatus('idle');
    activeMsRef.current = current.item.activeMs || 0;
    lastInputRef.current = Date.now();
  }, []);

  useEffect(() => {
    (async () => {
      await startAnagram();
      await loadCurrent();
    })();
  }, [loadCurrent]);

  useEffect(() => {
    onProgress({ pct: `${Math.round(((number - 1) / total) * 100)}%`, timeRemainingSeconds: null });
  }, [number, total]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const id = setInterval(() => {
      const visible = document.visibilityState === 'visible';
      if (visible && Date.now() - lastInputRef.current <= IDLE_AFTER_MS) activeMsRef.current += TICK_MS;
    }, TICK_MS);
    const touch = () => { lastInputRef.current = Date.now(); };
    window.addEventListener('pointerdown', touch);
    window.addEventListener('pointermove', touch);
    window.addEventListener('keydown', touch);
    return () => {
      clearInterval(id);
      window.removeEventListener('pointerdown', touch);
      window.removeEventListener('pointermove', touch);
      window.removeEventListener('keydown', touch);
    };
  }, []);

  const placed = new Set(slots.filter((s) => s != null));
  const locked = status === 'checking' || status === 'correct';

  const checkWord = useCallback(async (filledSlots) => {
    if (busyRef.current) return;
    busyRef.current = true;
    setStatus('checking');
    try {
      const word = filledSlots.map((tileId) => tiles.find((tile) => tile.id === tileId).ch).join('');
      const result = await guessAnagram(item.id, word, activeMsRef.current);
      if (result.correct) {
        setStatus('correct');
        setTimeout(() => { busyRef.current = false; loadCurrent(); }, 900);
        return;
      }
      setStatus('wrong');
      setTimeout(() => {
        setSlots((prev) => prev.map(() => null));
        setStatus('idle');
        busyRef.current = false;
      }, 750);
    } catch {
      setStatus('idle');
      busyRef.current = false;
    }
  }, [item, tiles, loadCurrent]);

  useEffect(() => {
    if (status === 'idle' && slots.length > 0 && !slots.includes(null)) checkWord(slots);
  }, [slots, status, checkWord]);

  const placeTile = (tileId) => {
    if (locked || placed.has(tileId)) return;
    setSlots((prev) => {
      const index = prev.indexOf(null);
      if (index === -1) return prev;
      const next = [...prev];
      next[index] = tileId;
      return next;
    });
  };

  const removeFromSlot = (slotIndex) => {
    if (locked || status === 'wrong') return;
    setSlots((prev) => prev.map((s, i) => (i === slotIndex ? null : s)));
  };

  const removeLast = () => {
    if (locked) return;
    setSlots((prev) => {
      const lastIndex = prev.map((s) => s != null).lastIndexOf(true);
      if (lastIndex === -1) return prev;
      return prev.map((s, i) => (i === lastIndex ? null : s));
    });
  };

  const clearAll = () => { if (!locked) setSlots((prev) => prev.map(() => null)); };
  const shuffleTiles = () => setTiles((prev) => shuffled(prev));

  const skip = async () => {
    if (busyRef.current) return;
    busyRef.current = true;
    try {
      await skipAnagram(item.id, activeMsRef.current);
      await loadCurrent();
    } finally {
      busyRef.current = false;
    }
  };

  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key === 'Backspace') { e.preventDefault(); removeLast(); return; }
      if (e.key === 'Escape') { clearAll(); return; }
      if (e.key.length !== 1) return;
      const ch = e.key.toUpperCase();
      const tile = tiles.find((tl) => tl.ch === ch && !placed.has(tl.id));
      if (tile) placeTile(tile.id);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }); // re-bound every render so it always sees current tiles/slots

  if (completion) {
    return (
      <CompletionOverlay
        indicatorKey="patience"
        score={completion.score}
        achievement={completion.achievement}
        onContinue={() => goTo('selection')}
      />
    );
  }
  if (!item) return null;

  const n = slots.length;
  const cell = `min(56px, calc((100% - ${(n - 1) * 8}px) / ${n}))`;
  const slotColor = status === 'correct' ? '#2E7052' : status === 'wrong' ? '#BD5B4C' : '#2E5570';

  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'flex-start', justifyContent: 'center', padding: 'clamp(20px,6vw,40px) clamp(14px,4vw,24px) 60px' }}>
      <style>{KEYFRAMES}</style>
      <div key={item.id} style={{
        width: '100%', maxWidth: '680px', padding: 'clamp(24px,6vw,40px) clamp(16px,5vw,44px)', borderRadius: '24px', boxSizing: 'border-box',
        background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(18px)',
        boxShadow: '0 20px 50px rgba(31,55,75,0.08)', animation: 'mm-anagram-in 0.35s ease both',
      }}>
        <div style={{ fontSize: '12px', fontWeight: 700, color: '#2E5570', letterSpacing: '0.04em', marginBottom: '8px' }}>
          {t('anagram.counter')(number, total)}
        </div>
        <p style={{ fontSize: '13px', color: '#556269', margin: '0 0 30px', lineHeight: 1.5 }}>{t('anagram.instruction')}</p>

        <div style={{
          display: 'flex', justifyContent: 'center', gap: '8px', marginBottom: '14px',
          animation: status === 'wrong' ? 'mm-anagram-shake 0.45s ease' : 'none',
        }}>
          {slots.map((tileId, i) => {
            const tile = tileId != null ? tiles.find((tl) => tl.id === tileId) : null;
            return (
              <button key={i} className="mm-btn" onClick={() => removeFromSlot(i)} aria-label={tile ? tile.ch : '_'} style={{
                width: cell, aspectRatio: '5 / 6', borderRadius: '12px', padding: 0, cursor: tile && !locked ? 'pointer' : 'default',
                border: tile ? `2px solid ${slotColor}` : '2px dashed rgba(31,55,75,0.22)',
                background: status === 'correct' ? '#DCEFE2' : status === 'wrong' ? '#F6E0DC' : tile ? '#fff' : 'rgba(255,255,255,0.35)',
                color: slotColor, fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: 'clamp(15px, 4.5vw, 24px)',
                animation: status === 'correct' ? `mm-anagram-pop 0.45s ease ${i * 40}ms both` : 'none',
                transition: 'background 0.2s, border-color 0.2s',
              }}>{tile ? tile.ch : ''}</button>
            );
          })}
        </div>

        <div style={{ height: '22px', textAlign: 'center', fontSize: '12.5px', fontWeight: 600, marginBottom: '18px', color: status === 'correct' ? '#2E7052' : '#BD5B4C' }}>
          {status === 'wrong' && t('anagram.notAWord')}
          {status === 'correct' && t('anagram.solved')}
        </div>

        <div style={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: '8px', marginBottom: '30px' }}>
          {tiles.map((tile) => {
            const used = placed.has(tile.id);
            return (
              <button key={tile.id} className="mm-btn" onClick={() => placeTile(tile.id)} disabled={used || locked} style={{
                width: cell, aspectRatio: '5 / 6', borderRadius: '12px', padding: 0,
                border: used ? '1.5px dashed rgba(31,55,75,0.12)' : '1.5px solid rgba(46,85,112,0.25)',
                background: used ? 'transparent' : 'linear-gradient(180deg,#FFFFFF 0%,#EEF4F7 100%)',
                boxShadow: used ? 'none' : '0 3px 0 rgba(46,85,112,0.18)',
                color: used ? 'transparent' : '#1F374B', cursor: used || locked ? 'default' : 'pointer',
                fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: 'clamp(15px, 4.5vw, 24px)',
                transition: 'transform 0.1s, opacity 0.15s', opacity: used ? 0.5 : 1,
              }}>{tile.ch}</button>
            );
          })}
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="mm-btn" onClick={shuffleTiles} disabled={locked} style={TOOL_BTN}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5" /></svg>
              {t('anagram.shuffle')}
            </button>
            <button className="mm-btn" onClick={clearAll} disabled={locked || placed.size === 0} style={{ ...TOOL_BTN, opacity: placed.size === 0 ? 0.5 : 1 }}>
              {t('anagram.clear')}
            </button>
          </div>
          <button className="mm-btn" onClick={skip} disabled={locked} style={{
            padding: '9px 16px', borderRadius: '100px', border: 'none', background: 'rgba(31,55,75,0.06)',
            color: '#556269', fontWeight: 600, fontSize: '12.5px', cursor: 'pointer',
          }}>{t('anagram.skip')}</button>
        </div>
      </div>
    </div>
  );
}
