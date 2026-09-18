import { useEffect, useRef, useState } from 'react';

import { answerLearning, getLearningState, startLearning, submitLearning } from '../../api/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import CompletionOverlay from './CompletionOverlay.jsx';

const CARD = {
  width: '100%', maxWidth: '680px', padding: 'clamp(24px,6vw,40px) clamp(20px,6vw,44px)', borderRadius: '24px',
  background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(18px)',
  boxShadow: '0 20px 50px rgba(31,55,75,0.08)', boxSizing: 'border-box',
};
const EYEBROW = { fontSize: '12px', fontWeight: 700, color: '#2E5570', letterSpacing: '0.04em', marginBottom: '8px' };
const PRIMARY_BTN = {
  padding: '12px 26px', borderRadius: '100px', border: 'none', background: '#2E5570', color: '#fff',
  fontWeight: 700, fontSize: '13.5px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px',
};
const CODE = {
  margin: 0, padding: '14px 18px', borderRadius: '12px', background: '#F1F5F7', border: '1px solid rgba(31,55,75,0.08)',
  fontFamily: "'JetBrains Mono','Consolas',monospace", fontSize: '15px', color: '#161F24', lineHeight: 1.6,
  whiteSpace: 'pre-wrap', overflowX: 'auto',
};

function Rules({ rules }) {
  return (
    <ol style={{ margin: 0, paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
      {rules.map((rule, i) => (
        <li key={i} style={{ fontSize: '14.5px', color: '#161F24', lineHeight: 1.55, fontWeight: 500 }}>{rule}</li>
      ))}
    </ol>
  );
}

/**
 * learning_speed: study a novel mini-system's rules (timed, then hidden), answer
 * three blocks of items one at a time, and see a per-block review (correct answer,
 * explanation, rules again) between blocks — the feedback students learn from.
 */
export default function Learning({ goTo, onProgress }) {
  const [state, setState] = useState(null);
  const [phase, setPhase] = useState('loading'); // loading | study | block | feedback
  const [itemIndex, setItemIndex] = useState(0);
  const [selected, setSelected] = useState(null);
  const [feedback, setFeedback] = useState(null); // { items, done }
  const [studyLeft, setStudyLeft] = useState(0);
  const [busy, setBusy] = useState(false);
  const [completion, setCompletion] = useState(null);
  const shownAtRef = useRef(null);
  const studyDeadlineRef = useRef(null);
  const { t } = useLanguage();

  const loadState = async () => {
    const next = await getLearningState();
    if (next.done) {
      setCompletion(await submitLearning());
      return;
    }
    setState(next);
    setItemIndex(0);
    setSelected(null);
    setFeedback(null);
    if (next.phase === 'study') {
      studyDeadlineRef.current = Date.now() + next.module.studySeconds * 1000;
      setStudyLeft(next.module.studySeconds);
      setPhase('study');
    } else {
      setPhase('block');
      shownAtRef.current = Date.now();
    }
  };

  useEffect(() => {
    (async () => {
      await startLearning();
      await loadState();
    })();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!state) return;
    const answered = state.answered + (phase === 'block' ? itemIndex : 0);
    onProgress({ pct: `${Math.round((answered / state.total) * 100)}%`, timeRemainingSeconds: null });
  }, [state, itemIndex, phase]); // eslint-disable-line react-hooks/exhaustive-deps

  const beginBlock = () => {
    setPhase('block');
    shownAtRef.current = Date.now();
  };

  useEffect(() => {
    if (phase !== 'study') return undefined;
    const id = setInterval(() => {
      const left = Math.max(0, Math.round((studyDeadlineRef.current - Date.now()) / 1000));
      setStudyLeft(left);
      if (left === 0) beginBlock();
    }, 500);
    return () => clearInterval(id);
  }, [phase]);

  const submitAnswer = async () => {
    if (selected == null || busy) return;
    setBusy(true);
    try {
      const item = state.items[itemIndex];
      const result = await answerLearning(item.id, selected, Date.now() - shownAtRef.current);
      if (result.block_complete) {
        setFeedback({ items: result.feedback, done: result.done });
        setPhase('feedback');
        return;
      }
      setItemIndex((i) => i + 1);
      setSelected(null);
      shownAtRef.current = Date.now();
    } finally {
      setBusy(false);
    }
  };

  const continueAfterFeedback = async () => {
    setBusy(true);
    try {
      if (feedback.done) setCompletion(await submitLearning());
      else await loadState();
    } finally {
      setBusy(false);
    }
  };

  if (completion) {
    return (
      <CompletionOverlay
        indicatorKey="learning_speed"
        score={completion.score}
        achievement={completion.achievement}
        onContinue={() => goTo('selection')}
      />
    );
  }
  if (!state || phase === 'loading') return null;

  const header = `${t('learning.moduleLabel')(state.moduleNumber, state.moduleTotal)} · ${state.module.title}`;

  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'flex-start', justifyContent: 'center', padding: 'clamp(20px,6vw,40px) clamp(14px,4vw,24px) 60px' }}>
      {phase === 'study' && (
        <div style={CARD}>
          <div style={EYEBROW}>{header}</div>
          <h2 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '24px', color: '#161F24', margin: '0 0 18px' }}>
            {t('learning.studyTitle')}
          </h2>
          <div style={{ padding: '18px 20px', borderRadius: '16px', background: 'rgba(255,255,255,0.7)', border: '1px solid rgba(31,55,75,0.08)', marginBottom: '18px' }}>
            <Rules rules={state.module.rules} />
          </div>
          <p style={{ fontSize: '12.5px', color: '#556269', margin: '0 0 18px', lineHeight: 1.5 }}>{t('learning.studyHint')}</p>
          <div style={{ height: '4px', borderRadius: '4px', background: '#EAF2F5', marginBottom: '8px', overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${(studyLeft / state.module.studySeconds) * 100}%`, background: '#3E7EA6', transition: 'width 0.5s linear' }} />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '12px', fontWeight: 700, color: '#556269', fontVariantNumeric: 'tabular-nums' }}>{t('learning.timeLeft')(studyLeft)}</span>
            <button className="mm-btn" onClick={beginBlock} style={PRIMARY_BTN}>{t('learning.ready')}</button>
          </div>
        </div>
      )}

      {phase === 'block' && (() => {
        const item = state.items[itemIndex];
        return (
          <div style={CARD}>
            <div style={EYEBROW}>
              {header} · {t('learning.blockLabel')(state.block, state.blockTotal)} · {t('learning.questionLabel')(state.blockSize - state.items.length + itemIndex + 1, state.blockSize)}
            </div>
            <h2 style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: '19px', color: '#161F24', lineHeight: 1.5, margin: '0 0 16px' }}>{item.prompt}</h2>
            {item.code && <pre style={{ ...CODE, marginBottom: '22px' }}>{item.code}</pre>}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '10px', marginBottom: '26px' }}>
              {item.options.map((opt, idx) => {
                const on = selected === idx;
                return (
                  <button key={idx} className="mm-btn" onClick={() => setSelected(idx)} style={{
                    textAlign: 'left', padding: '14px 18px', borderRadius: '14px', cursor: 'pointer',
                    border: `1.5px solid ${on ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
                    background: on ? 'rgba(46,85,112,0.12)' : 'rgba(255,255,255,0.5)',
                    color: on ? '#1F374B' : '#3B444A', fontFamily: 'Manrope', fontSize: '14.5px', fontWeight: 600,
                  }}>{opt}</button>
                );
              })}
            </div>
            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <button className="mm-btn" disabled={selected == null || busy} onClick={submitAnswer}
                style={{ ...PRIMARY_BTN, opacity: selected == null ? 0.45 : 1, cursor: selected == null ? 'not-allowed' : 'pointer' }}>
                {busy && <span className="mm-spinner" />}
                {t('learning.answer')}
              </button>
            </div>
          </div>
        );
      })()}

      {phase === 'feedback' && (() => {
        const correct = feedback.items.filter((f) => f.isCorrect).length;
        const lastBlockOfModule = state.block >= state.blockTotal;
        const nextLabel = feedback.done ? t('learning.finish') : lastBlockOfModule ? t('learning.nextModule') : t('learning.nextBlock');
        return (
          <div style={CARD}>
            <div style={EYEBROW}>{header}</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: '12px', flexWrap: 'wrap', marginBottom: '18px' }}>
              <h2 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '22px', color: '#161F24', margin: 0 }}>
                {t('learning.feedbackTitle')(state.block)}
              </h2>
              <span style={{ fontSize: '13px', fontWeight: 700, color: correct === feedback.items.length ? '#2E7052' : '#556269' }}>
                {t('learning.correctCount')(correct, feedback.items.length)}
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '20px' }}>
              {feedback.items.map((f) => (
                <div key={f.id} style={{
                  padding: '14px 16px', borderRadius: '14px', background: 'rgba(255,255,255,0.7)',
                  borderLeft: `4px solid ${f.isCorrect ? '#2E7052' : '#BD5B4C'}`,
                }}>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start', marginBottom: f.code ? '8px' : '6px' }}>
                    <span style={{ fontWeight: 800, color: f.isCorrect ? '#2E7052' : '#BD5B4C' }}>{f.isCorrect ? '✓' : '✗'}</span>
                    <span style={{ fontSize: '13.5px', fontWeight: 600, color: '#161F24', lineHeight: 1.5 }}>{f.prompt}</span>
                  </div>
                  {f.code && <pre style={{ ...CODE, fontSize: '13px', padding: '10px 14px', marginBottom: '8px' }}>{f.code}</pre>}
                  <div style={{ fontSize: '12.5px', color: '#3B444A', lineHeight: 1.6 }}>
                    {!f.isCorrect && (
                      <div>{t('learning.yourAnswer')}: <b style={{ color: '#BD5B4C' }}>{f.options[f.selectedIndex]}</b></div>
                    )}
                    <div>{t('learning.correctAnswer')}: <b style={{ color: '#2E7052' }}>{f.options[f.correctIndex]}</b></div>
                    {f.explanation && <div style={{ color: '#556269', marginTop: '2px' }}>{f.explanation}</div>}
                  </div>
                </div>
              ))}
            </div>

            {!lastBlockOfModule && (
              <div style={{ padding: '16px 18px', borderRadius: '14px', background: 'rgba(62,126,166,0.08)', marginBottom: '22px' }}>
                <div style={{ fontSize: '11.5px', fontWeight: 700, color: '#2E5570', letterSpacing: '0.04em', marginBottom: '10px' }}>
                  {t('learning.rulesReminder')}
                </div>
                <Rules rules={state.module.rules} />
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <button className="mm-btn" disabled={busy} onClick={continueAfterFeedback} style={PRIMARY_BTN}>
                {busy && <span className="mm-spinner" />}
                {nextLabel}
              </button>
            </div>
          </div>
        );
      })()}
    </div>
  );
}
