import { useEffect, useRef, useState } from 'react';

import { answerSjt, getSjtNext, startSjt, submitSjt } from '../../api/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import CompletionOverlay from './CompletionOverlay.jsx';

const CHIP = {
  padding: '7px 12px', borderRadius: '100px', fontSize: '12px', fontWeight: 700, cursor: 'pointer', whiteSpace: 'nowrap',
};

/**
 * teamwork situational judgment test: one scenario at a time, the student marks
 * the most and the least effective action among four. No feedback is shown —
 * the key is the experts' rating of each option.
 */
export default function Sjt({ goTo, onProgress }) {
  const [scenario, setScenario] = useState(null);
  const [number, setNumber] = useState(1);
  const [total, setTotal] = useState(10);
  const [best, setBest] = useState(null);
  const [worst, setWorst] = useState(null);
  const [busy, setBusy] = useState(false);
  const [completion, setCompletion] = useState(null);
  const shownAtRef = useRef(null);
  const { t } = useLanguage();

  const loadNext = async () => {
    const next = await getSjtNext();
    if (!next.scenario) {
      setCompletion(await submitSjt());
      return;
    }
    setScenario(next.scenario);
    setNumber(next.number);
    setTotal(next.total);
    setBest(null);
    setWorst(null);
    shownAtRef.current = Date.now();
  };

  useEffect(() => {
    (async () => {
      await startSjt();
      await loadNext();
    })();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    onProgress({ pct: `${Math.round(((number - 1) / total) * 100)}%`, timeRemainingSeconds: null });
  }, [number, total]); // eslint-disable-line react-hooks/exhaustive-deps

  const pickBest = (index) => {
    setBest(index);
    if (worst === index) setWorst(null);
  };
  const pickWorst = (index) => {
    setWorst(index);
    if (best === index) setBest(null);
  };

  const submit = async () => {
    if (best == null || worst == null || busy) return;
    setBusy(true);
    try {
      const result = await answerSjt(scenario.id, best, worst, Date.now() - shownAtRef.current);
      if (result.is_last) setCompletion(await submitSjt());
      else await loadNext();
    } finally {
      setBusy(false);
    }
  };

  if (completion) {
    return (
      <CompletionOverlay
        indicatorKey="teamwork"
        score={completion.score}
        achievement={completion.achievement}
        onContinue={() => goTo('selection')}
      />
    );
  }
  if (!scenario) return null;

  const ready = best != null && worst != null;

  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'flex-start', justifyContent: 'center', padding: 'clamp(20px,6vw,40px) clamp(14px,4vw,24px) 60px' }}>
      <div style={{
        width: '100%', maxWidth: '720px', padding: 'clamp(24px,6vw,40px) clamp(20px,6vw,44px)', borderRadius: '24px', boxSizing: 'border-box',
        background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(18px)', boxShadow: '0 20px 50px rgba(31,55,75,0.08)',
      }}>
        <div style={{ fontSize: '12px', fontWeight: 700, color: '#2E5570', letterSpacing: '0.04em', marginBottom: '8px' }}>
          {t('sjt.scenarioLabel')(number, total)}
        </div>
        <h2 style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: '19px', color: '#161F24', lineHeight: 1.55, margin: '0 0 10px' }}>
          {scenario.situation}
        </h2>
        <p style={{ fontSize: '12.5px', color: '#556269', margin: '0 0 20px', lineHeight: 1.5 }}>{t('sjt.instruction')}</p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '26px' }}>
          {scenario.options.map((opt) => {
            const isBest = best === opt.index;
            const isWorst = worst === opt.index;
            return (
              <div key={opt.index} style={{
                display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '10px 14px',
                padding: '14px 16px', borderRadius: '14px',
                background: isBest ? 'rgba(46,112,82,0.08)' : isWorst ? 'rgba(189,91,76,0.07)' : 'rgba(255,255,255,0.55)',
                border: `1.5px solid ${isBest ? '#2E7052' : isWorst ? '#BD5B4C' : 'rgba(31,55,75,0.12)'}`,
              }}>
                <span style={{ flex: '1 1 280px', fontSize: '14px', color: '#161F24', fontWeight: 500, lineHeight: 1.5 }}>{opt.text}</span>
                <div style={{ display: 'flex', gap: '6px', flexShrink: 0 }}>
                  <button className="mm-btn" onClick={() => pickBest(opt.index)} style={{
                    ...CHIP,
                    border: `1.5px solid ${isBest ? '#2E7052' : 'rgba(46,112,82,0.35)'}`,
                    background: isBest ? '#2E7052' : 'transparent', color: isBest ? '#fff' : '#2E7052',
                  }}>{t('sjt.best')}</button>
                  <button className="mm-btn" onClick={() => pickWorst(opt.index)} style={{
                    ...CHIP,
                    border: `1.5px solid ${isWorst ? '#BD5B4C' : 'rgba(189,91,76,0.35)'}`,
                    background: isWorst ? '#BD5B4C' : 'transparent', color: isWorst ? '#fff' : '#BD5B4C',
                  }}>{t('sjt.worst')}</button>
                </div>
              </div>
            );
          })}
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button className="mm-btn" disabled={!ready || busy} onClick={submit} style={{
            padding: '12px 26px', borderRadius: '100px', border: 'none', background: '#2E5570', color: '#fff',
            fontWeight: 700, fontSize: '13.5px', display: 'flex', alignItems: 'center', gap: '8px',
            opacity: ready ? 1 : 0.45, cursor: ready ? 'pointer' : 'not-allowed',
          }}>
            {busy && <span className="mm-spinner" />}
            {number >= total ? t('sjt.finish') : t('sjt.next')}
          </button>
        </div>
      </div>
    </div>
  );
}
