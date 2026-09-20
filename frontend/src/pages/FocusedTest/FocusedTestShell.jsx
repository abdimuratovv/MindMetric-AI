import { useState } from 'react';

import { pauseAttempt } from '../../api/assessments.js';
import { ASSESSMENT_PATTERN } from '../../constants/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import Anagram from './Anagram.jsx';
import Hybrid from './Hybrid.jsx';
import Learning from './Learning.jsx';
import Mcq from './Mcq.jsx';
import Sjt from './Sjt.jsx';

/**
 * Header/timer/progress bar shared by all ten focused-test screens, plus the
 * pattern-based dispatch that picks which generalized screen component handles
 * the current `screen` type — see constants/assessments.js's ASSESSMENT_PATTERN.
 */
export default function FocusedTestShell({ screen, goTo }) {
  const [progress, setProgress] = useState({ pct: '0%', timeRemainingSeconds: null });
  const [isExiting, setIsExiting] = useState(false);
  const { t } = useLanguage();

  const pattern = ASSESSMENT_PATTERN[screen];

  const exitTest = async () => {
    setIsExiting(true);
    try {
      if (progress.timeRemainingSeconds != null) {
        await pauseAttempt(screen, progress.timeRemainingSeconds);
      }
      goTo('selection');
    } finally {
      setIsExiting(false);
    }
  };

  const timerLabel = (pattern === 'mcq' || pattern === 'hybrid') && progress.timeRemainingSeconds != null
    ? `${Math.floor(progress.timeRemainingSeconds / 60)}:${String(progress.timeRemainingSeconds % 60).padStart(2, '0')}`
    : '';
  const timerColor = progress.timeRemainingSeconds != null && progress.timeRemainingSeconds < 60 ? '#BD5B4C' : '#1F374B';

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px',
        padding: 'clamp(12px,3.5vw,20px) clamp(16px,5vw,40px)',
        borderBottom: '1px solid rgba(31,55,75,0.08)', background: 'rgba(255,255,255,0.4)', backdropFilter: 'blur(14px)',
      }}>
        <button
          className="mm-btn mm-exit-btn"
          disabled={isExiting}
          onClick={exitTest}
          title={t('focusedTest.saveExitHint')}
          aria-label={t('focusedTest.saveExit')}
          style={{
            display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0, cursor: 'pointer',
            padding: '9px 16px 9px 13px', borderRadius: '100px',
            border: '1px solid rgba(31,55,75,0.14)', background: 'rgba(255,255,255,0.72)',
            color: '#3B444A', fontFamily: 'Manrope, sans-serif', fontWeight: 700, fontSize: '12.5px',
            boxShadow: '0 2px 8px rgba(31,55,75,0.06)', transition: 'transform 0.12s ease, background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease, color 0.18s ease',
          }}>
          {isExiting
            ? <span className="mm-spinner mm-spinner-dark" style={{ width: '14px', height: '14px' }} />
            : (
              <svg className="mm-exit-arrow" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M15 21h3a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-3" /><path d="M10 17l-5-5 5-5" /><path d="M15 12H5" />
              </svg>
            )}
          <span className="mm-exit-label">{t('focusedTest.saveExit')}</span>
          <span className="mm-exit-label-short" style={{ display: 'none' }}>{t('focusedTest.saveExitShort')}</span>
        </button>
        <div style={{
          fontWeight: 700, fontSize: '13.5px', color: '#161F24', flex: 1, minWidth: 0, textAlign: 'center',
          whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', padding: '0 8px',
        }}>{t('assessmentsMeta.' + screen).title}</div>
        <div style={{ fontWeight: 700, fontSize: '14px', color: timerColor, fontVariantNumeric: 'tabular-nums', flexShrink: 0 }}>{timerLabel}</div>
      </header>
      <div style={{ height: '4px', background: '#EAF2F5' }}>
        <div style={{ height: '100%', width: progress.pct, background: '#2E5570', transition: 'width 0.3s' }} />
      </div>

      {pattern === 'mcq' && <Mcq assessmentType={screen} goTo={goTo} onProgress={setProgress} />}
      {pattern === 'hybrid' && <Hybrid goTo={goTo} onProgress={setProgress} />}
      {pattern === 'anagram' && <Anagram goTo={goTo} onProgress={setProgress} />}
      {pattern === 'learning' && <Learning goTo={goTo} onProgress={setProgress} />}
      {pattern === 'sjt' && <Sjt goTo={goTo} onProgress={setProgress} />}
    </div>
  );
}
