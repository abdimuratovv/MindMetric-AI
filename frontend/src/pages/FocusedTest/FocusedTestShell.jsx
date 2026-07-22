import { useState } from 'react';

import { pauseAttempt } from '../../api/assessments.js';
import { ASSESSMENT_PATTERN } from '../../constants/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import Coding from './Coding.jsx';
import Likert from './Likert.jsx';
import Mcq from './Mcq.jsx';

/**
 * Header/timer/progress bar shared by all ten focused-test screens, plus the
 * pattern-based dispatch (mcq/coding/likert) that picks which generalized
 * screen component handles the current `screen` type — see
 * constants/assessments.js's ASSESSMENT_PATTERN, mirroring
 * apps.assessments.models.AssessmentAttempt's MCQ_TYPES/CODING_TYPES/LIKERT_TYPES.
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

  const timerLabel = pattern === 'mcq' && progress.timeRemainingSeconds != null
    ? `${Math.floor(progress.timeRemainingSeconds / 60)}:${String(progress.timeRemainingSeconds % 60).padStart(2, '0')}`
    : '';
  const timerColor = progress.timeRemainingSeconds != null && progress.timeRemainingSeconds < 60 ? '#BD5B4C' : '#1F374B';

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px 40px',
        borderBottom: '1px solid rgba(31,55,75,0.08)', background: 'rgba(255,255,255,0.4)', backdropFilter: 'blur(14px)',
      }}>
        <button
          className="mm-btn"
          disabled={isExiting}
          onClick={exitTest}
          style={{ border: 'none', background: 'none', color: '#556269', fontWeight: 600, fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '7px' }}>
          {isExiting && <span className="mm-spinner mm-spinner-dark" />}
          {t('focusedTest.saveExit')}
        </button>
        <div style={{ fontWeight: 700, fontSize: '13.5px', color: '#161F24' }}>{t('assessmentsMeta.' + screen).title}</div>
        <div style={{ fontWeight: 700, fontSize: '14px', color: timerColor, fontVariantNumeric: 'tabular-nums' }}>{timerLabel}</div>
      </header>
      <div style={{ height: '4px', background: '#EAF2F5' }}>
        <div style={{ height: '100%', width: progress.pct, background: '#2E5570', transition: 'width 0.3s' }} />
      </div>

      {pattern === 'mcq' && <Mcq assessmentType={screen} goTo={goTo} onProgress={setProgress} />}
      {pattern === 'coding' && <Coding goTo={goTo} onProgress={setProgress} />}
      {pattern === 'likert' && <Likert assessmentType={screen} goTo={goTo} onProgress={setProgress} />}
    </div>
  );
}
