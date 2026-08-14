import { useEffect, useState } from 'react';

import { getCodingProblem, runCode as apiRunCode, startCoding, submitCoding as apiSubmitCoding } from '../../api/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import CompletionOverlay from './CompletionOverlay.jsx';

/** Ported verbatim from MindMetric AI.dc.html lines 545-585 (`isCoding`). */
export default function Coding({ goTo, onProgress }) {
  const [problem, setProblem] = useState(null);
  const [code, setCode] = useState('');
  const [hasRun, setHasRun] = useState(false);
  const [testResults, setTestResults] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [codeFocused, setCodeFocused] = useState(false);
  const [completion, setCompletion] = useState(null);
  const { t } = useLanguage();

  useEffect(() => {
    (async () => {
      await startCoding();
      const p = await getCodingProblem();
      setProblem(p);
      setCode(p.starter_code);
    })();
  }, []);

  useEffect(() => { onProgress({ pct: '50%', timeRemainingSeconds: null }); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (completion) {
    return (
      <CompletionOverlay
        indicatorKey="algorithmic"
        score={completion.score}
        achievement={completion.achievement}
        onContinue={() => goTo('selection')}
      />
    );
  }

  if (!problem) return null;

  const run = async () => {
    setIsRunning(true);
    try {
      const { testResults: results } = await apiRunCode(code);
      setHasRun(true);
      setTestResults(results.map((r) => ({
        icon: r.passed ? '✓' : '✕',
        label: r.label,
        color: r.passed ? '#4FAE83' : '#E38A7C',
        textColor: r.passed ? '#EAF5EE' : '#F6E0DC',
      })));
    } finally {
      setIsRunning(false);
    }
  };

  const submit = async () => {
    setIsSubmitting(true);
    try {
      const result = await apiSubmitCoding(code);
      setCompletion(result);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{
      flex: 1, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
      gap: '1px', background: 'rgba(31,55,75,0.08)', overflowY: 'auto',
    }}>
      <div style={{ background: 'rgba(245,247,248,0.9)', padding: 'clamp(20px,5vw,34px) clamp(18px,5vw,38px)', overflowY: 'auto' }}>
        <div style={{ fontSize: '12px', fontWeight: 700, color: '#2E5570', letterSpacing: '0.04em', marginBottom: '10px' }}>{t('coding.task')}</div>
        <h2 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '26px', color: '#161F24', margin: '0 0 14px' }}>{problem.title}</h2>
        <div style={{ fontSize: '12.5px', fontWeight: 600, color: '#8A6D1F', marginBottom: '14px' }}>
          {t('coding.targetTime')(Math.round(problem.target_time_seconds / 60))}
        </div>
        <p style={{ fontSize: '14px', lineHeight: 1.7, color: '#3B444A', margin: '0 0 18px' }}>{problem.statement}</p>
        <div style={{ padding: '16px 18px', borderRadius: '14px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', marginBottom: '18px' }}>
          <div style={{ fontSize: '11.5px', fontWeight: 700, color: '#939EA3', marginBottom: '8px' }}>{t('coding.example')}</div>
          <div style={{ fontFamily: 'ui-monospace,Menlo,monospace', fontSize: '13px', color: '#161F24', whiteSpace: 'pre-wrap' }}>{problem.example}</div>
        </div>
        <div style={{ fontSize: '11.5px', fontWeight: 700, color: '#939EA3', marginBottom: '8px' }}>{t('coding.constraints')}</div>
        <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '13px', color: '#556269', lineHeight: 1.8 }}>
          {problem.constraints.map((c, i) => <li key={i}>{c}</li>)}
        </ul>
      </div>
      <div style={{ background: '#161F24', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', gap: 0, borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
          <div style={{ padding: '12px 20px', fontSize: '12.5px', fontWeight: 700, color: '#8FBCD9', borderBottom: '2px solid #8FBCD9' }}>solution.js</div>
        </div>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          onFocus={() => setCodeFocused(true)}
          onBlur={() => setCodeFocused(false)}
          spellCheck={false}
          style={{
            flex: 1, background: 'transparent', border: 'none', outline: 'none', color: '#EAF2F5',
            fontFamily: 'ui-monospace,Menlo,monospace', fontSize: '13.5px', lineHeight: 1.7, padding: '22px 26px',
            resize: 'none', minHeight: '260px',
            boxShadow: codeFocused ? 'inset 0 0 0 2px rgba(143,188,217,0.35)' : 'inset 0 0 0 2px transparent',
            transition: 'box-shadow 0.15s ease',
          }}
        />
        <div style={{ borderTop: '1px solid rgba(255,255,255,0.08)', padding: '16px 24px' }}>
          <div style={{ display: 'flex', gap: '10px', marginBottom: '14px' }}>
            <button
              className="mm-btn"
              disabled={isRunning}
              onClick={run}
              style={{
                padding: '9px 20px', borderRadius: '100px', border: 'none', cursor: 'pointer', background: '#8FBCD9',
                color: '#161F24', fontWeight: 700, fontSize: '12.5px', display: 'flex', alignItems: 'center', gap: '7px',
              }}>
              {isRunning && <span className="mm-spinner mm-spinner-dark" />}
              {t('coding.runTests')}
            </button>
            <button
              className="mm-btn"
              disabled={isSubmitting}
              onClick={submit}
              style={{
                padding: '9px 20px', borderRadius: '100px', border: '1px solid rgba(255,255,255,0.2)', cursor: 'pointer',
                background: 'transparent', color: '#EAF2F5', fontWeight: 700, fontSize: '12.5px', display: 'flex', alignItems: 'center', gap: '7px',
              }}>
              {isSubmitting && <span className="mm-spinner" />}
              {t('coding.submitSolution')}
            </button>
          </div>
          {hasRun && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', maxHeight: '150px', overflowY: 'auto' }}>
              {testResults.map((tr, i) => (
                <div key={i} style={{ display: 'flex', gap: '8px', alignItems: 'flex-start', fontFamily: 'ui-monospace,Menlo,monospace', fontSize: '12px' }}>
                  <span style={{ color: tr.color, fontWeight: 700, flexShrink: 0 }}>{tr.icon}</span>
                  <span style={{ color: tr.textColor }}>{tr.label}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
