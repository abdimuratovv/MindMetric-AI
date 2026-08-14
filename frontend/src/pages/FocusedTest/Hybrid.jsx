import { useState } from 'react';

import Coding from './Coding.jsx';
import Mcq from './Mcq.jsx';

/**
 * algorithmic's two-phase attempt (apps.assessments.models.AssessmentAttempt.
 * HYBRID_TYPES on the backend): MCQ questions first, then a coding task, blended
 * into one score by apps.scoring.state_tracker._score_hybrid — MCQ questions
 * alone can't show whether a student can actually produce working code.
 *
 * Mcq's submit hands off via `onPhaseComplete` instead of rendering its own
 * CompletionOverlay for this type (see SubmitMcqView on the backend); Coding's
 * own submit is the one that actually finishes the attempt and shows the
 * combined score.
 */
export default function Hybrid({ goTo, onProgress }) {
  const [phase, setPhase] = useState('mcq');

  // Each phase reports its own 0-100% locally; map mcq -> first half of the bar,
  // coding -> second half, so the header progress bar reads as one continuous test.
  const scaledProgress = (progress) => onProgress({
    ...progress,
    pct: phase === 'mcq' ? `${parseFloat(progress.pct) / 2}%` : `${50 + parseFloat(progress.pct) / 2}%`,
  });

  if (phase === 'mcq') {
    return <Mcq assessmentType="algorithmic" goTo={goTo} onProgress={scaledProgress} onPhaseComplete={() => setPhase('coding')} />;
  }
  return <Coding goTo={goTo} onProgress={scaledProgress} />;
}
