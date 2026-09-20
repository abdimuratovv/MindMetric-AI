import { useEffect, useRef, useState } from 'react';

import { getCodingProblem, runCode as apiRunCode, startCoding, submitCoding as apiSubmitCoding } from '../../api/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import CompletionOverlay from './CompletionOverlay.jsx';

/** Label chip used for the task counter and the recommended-solve-time hint. */
function Chip({ tone, children }) {
  const palette = {
    navy: { bg: 'rgba(46,85,112,0.1)', border: 'rgba(46,85,112,0.18)', color: '#2E5570' },
    amber: { bg: 'rgba(184,134,47,0.12)', border: 'rgba(184,134,47,0.22)', color: '#8A6D1F' },
  }[tone];
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '5px 12px', borderRadius: '100px',
      background: palette.bg, border: `1px solid ${palette.border}`, color: palette.color,
      fontSize: '11.5px', fontWeight: 700, letterSpacing: '0.03em', whiteSpace: 'nowrap',
    }}>{children}</span>
  );
}

/**
 * algorithmic's coding phase — CODING_TASK_CAP (backend apps.assessments.views)
 * distinct problems in sequence, mirroring Mcq.jsx's next-question loop: each
 * "Submit solution" either hands back {phase: 'next', cpNumber, cpTotal} (fetch the
 * next problem and keep going) or a completed {score, achievement} once the cap is
 * reached — see apps.assessments.views.SubmitCodingView.
 */
export default function Coding({ goTo, onProgress }) {
  const [problem, setProblem] = useState(null);
  const [cpNumber, setCpNumber] = useState(1);
  const [cpTotal, setCpTotal] = useState(1);
  const [code, setCode] = useState('');
  const [hasRun, setHasRun] = useState(false);
  const [testResults, setTestResults] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [codeFocused, setCodeFocused] = useState(false);
  const [completion, setCompletion] = useState(null);
  const [loadError, setLoadError] = useState(false);
  const [loadAttempt, setLoadAttempt] = useState(0);
  const { t } = useLanguage();
  // When the current problem was first shown — sent back as elapsed_ms so
  // state_tracker._score_hybrid can factor solve time into that problem's score.
  const problemShownAtRef = useRef(null);
  const codeRef = useRef(null);
  // A textarea can't render its own line numbers, so the gutter is a sibling
  // element scrolled in lockstep with it (same font size and line-height).
  const gutterRef = useRef(null);

  // Both calls fire together — the problem lookup doesn't depend on start's result
  // (the attempt row already exists from the MCQ phase), so running them in sequence
  // only doubled the wait. Cold starts / dropped requests used to leave this screen
  // blank forever, so a failure now surfaces a retry instead.
  useEffect(() => {
    let cancelled = false;
    setLoadError(false);
    (async () => {
      try {
        const [, next] = await Promise.all([startCoding(), getCodingProblem()]);
        if (cancelled) return;
        if (!next.problem) throw new Error('no coding problem');
        setProblem(next.problem);
        setCode(next.problem.starter_code || '');
        setCpNumber(next.cpNumber);
        setCpTotal(next.cpTotal);
        problemShownAtRef.current = Date.now();
      } catch {
        if (!cancelled) setLoadError(true);
      }
    })();
    return () => { cancelled = true; };
  }, [loadAttempt]);

  useEffect(() => {
    onProgress({ pct: `${Math.round((cpNumber / cpTotal) * 100)}%`, timeRemainingSeconds: null });
  }, [cpNumber, cpTotal]); // eslint-disable-line react-hooks/exhaustive-deps

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

  if (!problem) {
    return (
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        gap: '16px', padding: '80px 24px', textAlign: 'center', color: '#3B444A', fontSize: '14.5px',
      }}>
        {loadError ? (
          <>
            <span>{t('coding.loadError')}</span>
            <button
              className="mm-btn"
              onClick={() => setLoadAttempt((n) => n + 1)}
              style={{
                padding: '10px 22px', borderRadius: '100px', border: 'none', cursor: 'pointer',
                background: '#2E5570', color: '#fff', fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: '13px',
              }}>{t('coding.retry')}</button>
          </>
        ) : (
          <>
            <span className="mm-spinner mm-spinner-dark" style={{ width: '22px', height: '22px' }} />
            <span>{t('coding.loading')}</span>
          </>
        )}
      </div>
    );
  }

  const busy = isRunning || isSubmitting;

  const run = async () => {
    setIsRunning(true);
    try {
      const { testResults: results } = await apiRunCode(problem.id, code);
      setHasRun(true);
      setTestResults(results);
    } finally {
      setIsRunning(false);
    }
  };

  const submit = async () => {
    setIsSubmitting(true);
    try {
      const elapsedMs = problemShownAtRef.current != null ? Date.now() - problemShownAtRef.current : null;
      const result = await apiSubmitCoding(problem.id, code, elapsedMs);
      if (result.phase === 'next') {
        const next = await getCodingProblem();
        setProblem(next.problem);
        setCode(next.problem?.starter_code || '');
        setCpNumber(next.cpNumber);
        setCpTotal(next.cpTotal);
        setHasRun(false);
        setTestResults([]);
        problemShownAtRef.current = Date.now();
        return;
      }
      setCompletion(result);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Tab indents instead of leaving the editor, and Ctrl/Cmd+Enter runs the tests —
  // what anyone who has written code in any other editor expects to happen.
  const onCodeKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const el = e.target;
      const { selectionStart: start, selectionEnd: end } = el;
      setCode(`${code.slice(0, start)}  ${code.slice(end)}`);
      requestAnimationFrame(() => { el.selectionStart = start + 2; el.selectionEnd = start + 2; });
      return;
    }
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey) && !busy) {
      e.preventDefault();
      run();
    }
  };

  const resetCode = () => {
    if (!window.confirm(t('coding.resetConfirm'))) return;
    setCode(problem.starter_code || '');
    codeRef.current?.focus();
  };

  const lineCount = code.split('\n').length;
  const passedCount = testResults.filter((r) => r.passed).length;
  const allPassed = hasRun && testResults.length > 0 && passedCount === testResults.length;

  return (
    <div className="mm-code-layout">
      <div className="mm-code-brief mm-code-scroll" style={{
        background: 'rgba(245,247,248,0.92)', padding: 'clamp(20px,5vw,34px) clamp(18px,5vw,38px) clamp(28px,6vw,44px)',
      }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
          <Chip tone="navy">{t('coding.task')} {cpNumber} {t('mcq.of')} {cpTotal}</Chip>
          <Chip tone="amber">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" />
            </svg>
            {t('coding.targetTime')(Math.round(problem.target_time_seconds / 60))}
          </Chip>
        </div>
        <h2 style={{
          fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: 'clamp(21px,3.4vw,26px)',
          color: '#161F24', margin: '0 0 14px', lineHeight: 1.25,
        }}>{problem.title}</h2>
        <p style={{ fontSize: '14.5px', lineHeight: 1.75, color: '#3B444A', margin: '0 0 20px' }}>{problem.statement}</p>

        <div style={{
          padding: '16px 18px', borderRadius: '16px', background: 'rgba(255,255,255,0.72)',
          border: '1px solid rgba(255,255,255,0.9)', boxShadow: '0 8px 24px rgba(31,55,75,0.05)', marginBottom: '18px',
        }}>
          <div style={{ fontSize: '11px', fontWeight: 800, color: '#939EA3', letterSpacing: '0.07em', marginBottom: '10px' }}>{t('coding.example')}</div>
          <div style={{
            fontFamily: 'ui-monospace,Menlo,monospace', fontSize: '13px', lineHeight: 1.7, color: '#1F374B',
            whiteSpace: 'pre-wrap', wordBreak: 'break-word', padding: '12px 14px', borderRadius: '10px',
            background: 'rgba(220,236,239,0.5)', borderLeft: '3px solid #8FBCD9',
          }}>{problem.example}</div>
        </div>

        <div style={{ padding: '16px 18px', borderRadius: '16px', background: 'rgba(255,255,255,0.5)', border: '1px solid rgba(31,55,75,0.07)' }}>
          <div style={{ fontSize: '11px', fontWeight: 800, color: '#939EA3', letterSpacing: '0.07em', marginBottom: '10px' }}>{t('coding.constraints')}</div>
          <ul style={{ margin: 0, padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {problem.constraints.map((c, i) => (
              <li key={i} style={{ display: 'flex', gap: '10px', alignItems: 'flex-start', fontSize: '13.5px', color: '#556269', lineHeight: 1.6 }}>
                <span style={{ width: '5px', height: '5px', borderRadius: '50%', background: '#8FBCD9', flexShrink: 0, marginTop: '8px' }} />
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mm-code-editor" style={{ background: '#161F24' }}>
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px',
          borderBottom: '1px solid rgba(255,255,255,0.08)', background: 'rgba(255,255,255,0.02)', paddingRight: '12px',
        }}>
          <div style={{
            display: 'flex', alignItems: 'center', gap: '8px', padding: '13px 20px', fontSize: '12.5px',
            fontWeight: 700, color: '#8FBCD9', borderBottom: '2px solid #8FBCD9', marginBottom: '-1px',
          }}>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" /><path d="M14 3v5h5" />
            </svg>
            solution.js
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
            <span style={{ fontSize: '11px', fontWeight: 600, color: 'rgba(234,242,245,0.38)', fontVariantNumeric: 'tabular-nums' }}>{t('coding.lines')(lineCount)}</span>
            <button
              className="mm-btn mm-code-reset"
              disabled={busy}
              onClick={resetCode}
              title={t('coding.reset')}
              aria-label={t('coding.reset')}
              style={{
                display: 'flex', alignItems: 'center', padding: '6px 8px', borderRadius: '8px', border: 'none',
                background: 'transparent', color: 'rgba(234,242,245,0.5)', cursor: 'pointer',
                transition: 'color 0.15s ease, background 0.15s ease',
              }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M3 12a9 9 0 1 0 3-6.7" /><path d="M3 4v5h5" />
              </svg>
            </button>
          </div>
        </div>

        <div className="mm-code-surface" style={{
          boxShadow: codeFocused ? 'inset 0 0 0 1.5px rgba(143,188,217,0.32)' : 'inset 0 0 0 1.5px transparent',
          transition: 'box-shadow 0.15s ease',
        }}>
          <div ref={gutterRef} className="mm-code-gutter" aria-hidden="true">
            {Array.from({ length: lineCount }, (_, i) => <div key={i}>{i + 1}</div>)}
          </div>
          <textarea
            key={problem.id}
            ref={codeRef}
            className="mm-code-input mm-code-scroll"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onKeyDown={onCodeKeyDown}
            onScroll={(e) => { if (gutterRef.current) gutterRef.current.scrollTop = e.target.scrollTop; }}
            onFocus={() => setCodeFocused(true)}
            onBlur={() => setCodeFocused(false)}
            spellCheck={false}
            autoCapitalize="off"
            autoCorrect="off"
            // No soft wrapping: a wrapped line would take two visual rows while the
            // gutter still numbers it once, so the numbers would drift out of step.
            wrap="off"
            aria-label={t('coding.editorTitle')}
          />
        </div>

        <div style={{ borderTop: '1px solid rgba(255,255,255,0.08)', background: 'rgba(255,255,255,0.02)' }}>
          <div style={{ padding: '14px 20px' }}>
            {!hasRun ? (
              <div style={{ display: 'flex', gap: '9px', alignItems: 'flex-start', fontSize: '12px', color: 'rgba(234,242,245,0.45)', lineHeight: 1.5 }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0, marginTop: '1px' }} aria-hidden="true">
                  <circle cx="12" cy="12" r="9" /><path d="M12 11v5" /><path d="M12 8h.01" />
                </svg>
                <span>{t('coding.resultsEmpty')}</span>
              </div>
            ) : (
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', marginBottom: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '9px', minWidth: 0 }}>
                    <span style={{
                      width: '18px', height: '18px', borderRadius: '50%', flexShrink: 0,
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      background: allPassed ? 'rgba(79,174,131,0.18)' : 'rgba(227,138,124,0.18)',
                      color: allPassed ? '#4FAE83' : '#E38A7C',
                    }}>
                      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                        {allPassed ? <path d="M20 6L9 17l-5-5" /> : <><path d="M12 7v6" /><path d="M12 17h.01" /></>}
                      </svg>
                    </span>
                    <span style={{
                      fontSize: '12.5px', fontWeight: 700, color: allPassed ? '#8FD9B8' : '#F0B5AA',
                      whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                    }}>{allPassed ? t('coding.allPassed') : t('coding.someFailed')}</span>
                  </div>
                  <span style={{ fontSize: '11.5px', fontWeight: 700, color: 'rgba(234,242,245,0.5)', fontVariantNumeric: 'tabular-nums', flexShrink: 0 }}>
                    {t('coding.testsPassed')(passedCount, testResults.length)}
                  </span>
                </div>
                <div style={{ height: '4px', borderRadius: '100px', background: 'rgba(255,255,255,0.08)', overflow: 'hidden', marginBottom: '12px' }}>
                  <div style={{
                    height: '100%', width: `${testResults.length ? (passedCount / testResults.length) * 100 : 0}%`,
                    background: allPassed ? '#4FAE83' : '#E38A7C', borderRadius: '100px', transition: 'width 0.3s ease',
                  }} />
                </div>
                <div className="mm-code-scroll mm-code-results" style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  {testResults.map((tr, i) => (
                    <div key={i} className="mm-test-row" style={{
                      display: 'flex', gap: '9px', alignItems: 'flex-start', padding: '7px 10px', borderRadius: '8px',
                      background: tr.passed ? 'rgba(79,174,131,0.08)' : 'rgba(227,138,124,0.09)',
                      fontFamily: 'ui-monospace,Menlo,monospace', fontSize: '12px', lineHeight: 1.5,
                    }}>
                      <span style={{ color: tr.passed ? '#4FAE83' : '#E38A7C', fontWeight: 700, flexShrink: 0 }}>{tr.passed ? '✓' : '✕'}</span>
                      <span style={{ color: tr.passed ? '#D6EFE2' : '#F6E0DC', wordBreak: 'break-word' }}>{tr.label}</span>
                    </div>
                  ))}
                </div>
                <div style={{ marginTop: '10px', fontSize: '11px', color: 'rgba(234,242,245,0.34)', lineHeight: 1.5 }}>{t('coding.sampleNote')}</div>
              </div>
            )}
          </div>

          <div style={{
            borderTop: '1px solid rgba(255,255,255,0.07)', padding: '14px 20px',
            display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap',
          }}>
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
              <button
                className="mm-btn mm-code-ghost"
                disabled={busy}
                onClick={run}
                style={{
                  padding: '10px 18px', borderRadius: '100px', border: '1px solid rgba(255,255,255,0.22)', cursor: 'pointer',
                  background: 'rgba(255,255,255,0.04)', color: '#EAF2F5', fontFamily: 'Manrope, sans-serif',
                  fontWeight: 700, fontSize: '12.5px', display: 'flex', alignItems: 'center', gap: '8px',
                  transition: 'background 0.18s ease, border-color 0.18s ease',
                }}>
                {isRunning
                  ? <span className="mm-spinner" style={{ width: '13px', height: '13px' }} />
                  : (
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                      <path d="M7 4.5v15a1 1 0 0 0 1.53.85l12-7.5a1 1 0 0 0 0-1.7l-12-7.5A1 1 0 0 0 7 4.5z" />
                    </svg>
                  )}
                {isRunning ? t('coding.running') : t('coding.runTests')}
              </button>
              <button
                className="mm-btn mm-code-primary"
                disabled={busy}
                onClick={submit}
                style={{
                  padding: '10px 22px', borderRadius: '100px', border: 'none', cursor: 'pointer', background: '#8FBCD9',
                  color: '#0F1A20', fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: '12.5px',
                  display: 'flex', alignItems: 'center', gap: '8px', transition: 'background 0.18s ease, box-shadow 0.18s ease',
                }}>
                {isSubmitting && <span className="mm-spinner mm-spinner-dark" style={{ width: '13px', height: '13px' }} />}
                {cpNumber >= cpTotal ? t('mcq.submitTest') : t('coding.submitSolution')}
                {!isSubmitting && (
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <path d="M5 12h13" /><path d="M13 6l6 6-6 6" />
                  </svg>
                )}
              </button>
            </div>
            <span style={{ fontSize: '11px', fontWeight: 600, color: 'rgba(234,242,245,0.3)', whiteSpace: 'nowrap' }}>{t('coding.runHint')}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
