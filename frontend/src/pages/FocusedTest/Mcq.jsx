import { useEffect, useRef, useState } from 'react';

import { answerMcq, getMcqNextQuestion, startMcq, submitMcq } from '../../api/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import CompletionOverlay from './CompletionOverlay.jsx';

/** Empty-answer shape per question_type — single: no selection yet; multi: no options
 * checked yet; essay: no text typed yet. */
const emptyAnswerFor = (questionType) => (questionType === 'multi' ? [] : questionType === 'essay' ? '' : null);

/**
 * Generalized MCQ screen shared by all seven MCQ-pattern indicators (math, logic,
 * algorithmic, creative, problem_solving, attention, iq) — each is its own
 * AssessmentAttempt scoped to one indicator, difficulty-matched by
 * apps.scoring.engine.AdaptiveTestingEngine. "Previous" reviews already-answered
 * questions from local history rather than re-deriving position in a fixed array —
 * an adaptive test has no fixed array to index into.
 *
 * Renders three interaction modes per question.question_type (only `logic` currently
 * mixes all three; the other six indicators are single-only):
 * - single: one of N option buttons, exclusive selection (classic MCQ + step-ordering
 *   questions folded into this type).
 * - multi: same option rows as non-exclusive toggles ("select all that apply").
 * - essay: a free-text textarea, graded by apps.scoring.essay_grader on the backend.
 *
 * `onPhaseComplete` is set only by Hybrid.jsx (algorithmic's MCQ phase) — when
 * present, a `{phase: 'coding'}` submit response hands off to the coding phase
 * instead of this component showing its own CompletionOverlay.
 */
export default function Mcq({ assessmentType, goTo, onProgress, onPhaseComplete }) {
  const [liveQuestion, setLiveQuestion] = useState(null);
  const [cqNumber, setCqNumber] = useState(1);
  const [cqTotal, setCqTotal] = useState(5);
  const [history, setHistory] = useState([]); // [{category, prompt, options, question_type, answer}]
  const [position, setPosition] = useState(0); // index into [...history, live]
  const [localAnswer, setLocalAnswer] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(null);
  const [isAdvancing, setIsAdvancing] = useState(false);
  const [completion, setCompletion] = useState(null); // {score, achievement} once submitted
  const { t } = useLanguage();
  // Wall-clock deadline, not a per-tick counter — a tab that's backgrounded (switched away,
  // laptop sleep) has setInterval throttled by the browser, so decrementing "by 1 per tick"
  // would drift low. Recomputing from Date.now() every tick self-corrects instead.
  const deadlineRef = useRef(null);
  // When the current live question was displayed — sent back as response_time_ms so
  // AdaptiveTestingEngine can factor answer speed into the next question's difficulty.
  const questionShownAtRef = useRef(null);

  useEffect(() => {
    (async () => {
      const start = await startMcq(assessmentType);
      deadlineRef.current = Date.now() + start.time_remaining_seconds * 1000;
      setTimeRemaining(start.time_remaining_seconds);
      const next = await getMcqNextQuestion(assessmentType);
      // Reached with all questions already answered but not yet submitted — e.g. a
      // hybrid attempt whose MCQ phase already finished and the student refreshed
      // while on the coding phase (Hybrid.jsx always mounts back into 'mcq' first).
      // Re-submitting is idempotent (finish_mcq_phase just recomputes the same
      // score), so this hands off/completes immediately instead of stalling on a
      // blank screen with no question to show.
      if (!next.question) {
        const result = await submitMcq(assessmentType);
        if (result.phase === 'coding') { onPhaseComplete(); return; }
        setCompletion(result);
        return;
      }
      setLiveQuestion(next.question);
      setLocalAnswer(emptyAnswerFor(next.question?.question_type));
      setCqNumber(next.cqNumber);
      setCqTotal(next.cqTotal);
      questionShownAtRef.current = Date.now();
    })();
  }, [assessmentType]);

  useEffect(() => {
    onProgress({
      pct: `${Math.round((cqNumber / cqTotal) * 100)}%`,
      timeRemainingSeconds: timeRemaining,
    });
  }, [cqNumber, cqTotal, timeRemaining]); // eslint-disable-line react-hooks/exhaustive-deps

  // Ticks the local timer down once per second — the server round-trips (start/answer/pause)
  // only exchange snapshots; between them the client is the clock (see AssessmentAttempt.
  // time_remaining_seconds' docstring). Stops decrementing once it hits 0 rather than going negative.
  useEffect(() => {
    const id = setInterval(() => {
      if (deadlineRef.current == null) return;
      setTimeRemaining(Math.max(0, Math.round((deadlineRef.current - Date.now()) / 1000)));
    }, 1000);
    return () => clearInterval(id);
  }, []);

  // Auto-submits exactly once when the clock runs out, same finalize path as answering the
  // last question — whatever was answered so far counts, matching a real timed test.
  useEffect(() => {
    if (timeRemaining !== 0 || completion) return;
    (async () => {
      const result = await submitMcq(assessmentType);
      if (result.phase === 'coding') { onPhaseComplete(); return; }
      setCompletion(result);
    })();
  }, [timeRemaining]); // eslint-disable-line react-hooks/exhaustive-deps

  if (completion) {
    return (
      <CompletionOverlay
        indicatorKey={assessmentType}
        score={completion.score}
        achievement={completion.achievement}
        onContinue={() => goTo('selection')}
      />
    );
  }

  const isReviewing = position < history.length;
  const cq = isReviewing ? history[position] : liveQuestion;
  const cqAnswer = isReviewing ? history[position].answer : localAnswer;

  if (!cq) return null;

  const isMulti = cq.question_type === 'multi';
  const isEssay = cq.question_type === 'essay';

  const isOptionSelected = (idx) => (isMulti ? Array.isArray(cqAnswer) && cqAnswer.includes(idx) : cqAnswer === idx);

  const selectOption = (idx) => {
    if (isReviewing) return;
    if (isMulti) {
      setLocalAnswer((prev) => (prev.includes(idx) ? prev.filter((i) => i !== idx) : [...prev, idx]));
    } else {
      setLocalAnswer(idx);
    }
  };

  const isAnswerValid = () => {
    if (isEssay) return typeof localAnswer === 'string' && localAnswer.trim().length > 0;
    if (isMulti) return Array.isArray(localAnswer) && localAnswer.length > 0;
    return localAnswer != null;
  };

  const goPrev = () => { if (position > 0) setPosition(position - 1); };

  const goNext = async () => {
    if (isReviewing) {
      setPosition(position + 1);
      return;
    }
    if (!isAnswerValid()) return;
    setIsAdvancing(true);
    try {
      const responseTimeMs = questionShownAtRef.current != null ? Date.now() - questionShownAtRef.current : null;
      const payload = {
        ...(isEssay ? { essay_text: localAnswer } : { selected_indices: isMulti ? localAnswer : [localAnswer] }),
        response_time_ms: responseTimeMs,
      };
      const result = await answerMcq(assessmentType, liveQuestion.id, payload);
      setHistory((h) => [...h, { ...liveQuestion, answer: localAnswer }]);
      setPosition(history.length + 1);
      setTimeRemaining(result.time_remaining_seconds);

      if (result.is_last) {
        const completionResult = await submitMcq(assessmentType);
        if (completionResult.phase === 'coding') { onPhaseComplete(); return; }
        setCompletion(completionResult);
        return;
      }
      const next = await getMcqNextQuestion(assessmentType);
      setLiveQuestion(next.question);
      setLocalAnswer(emptyAnswerFor(next.question?.question_type));
      setCqNumber(next.cqNumber);
      questionShownAtRef.current = Date.now();
    } finally {
      setIsAdvancing(false);
    }
  };

  const cqOptions = (cq.options || []).map((text, idx) => ({
    text,
    bg: isOptionSelected(idx) ? 'rgba(46,85,112,0.12)' : 'rgba(255,255,255,0.5)',
    border: isOptionSelected(idx) ? '#2E5570' : 'rgba(31,55,75,0.14)',
    color: isOptionSelected(idx) ? '#1F374B' : '#3B444A',
  }));

  const cqNextLabel = !isReviewing && cqNumber >= cqTotal ? t('mcq.submitTest') : t('mcq.next');
  const essayWordCount = typeof cqAnswer === 'string' ? cqAnswer.trim().split(/\s+/).filter(Boolean).length : 0;

  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 'clamp(20px,6vw,40px) clamp(14px,4vw,24px)' }}>
      <div style={{
        width: '100%', maxWidth: '640px', padding: 'clamp(24px,6vw,40px) clamp(20px,6vw,44px)', borderRadius: '24px', background: 'rgba(255,255,255,0.62)',
        border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(18px)', boxShadow: '0 20px 50px rgba(31,55,75,0.08)',
      }}>
        <div style={{ fontSize: '12px', fontWeight: 700, color: '#2E5570', letterSpacing: '0.04em', marginBottom: '8px' }}>
          {t('mcq.question')} {isReviewing ? position + 1 : cqNumber} {t('mcq.of')} {cqTotal} · {cq.category}
        </div>
        <h2 style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: '20px', color: '#161F24', lineHeight: 1.5, margin: '0 0 26px' }}>{cq.prompt}</h2>

        {isEssay ? (
          <div style={{ marginBottom: '30px' }}>
            <textarea
              value={cqAnswer || ''}
              onChange={(e) => !isReviewing && setLocalAnswer(e.target.value)}
              readOnly={isReviewing}
              placeholder={t('mcq.essayPlaceholder')}
              rows={8}
              style={{
                width: '100%', boxSizing: 'border-box', padding: '14px 18px', borderRadius: '14px',
                border: '1.5px solid rgba(31,55,75,0.14)', background: 'rgba(255,255,255,0.5)',
                color: '#161F24', fontFamily: 'Manrope', fontSize: '14px', lineHeight: 1.6, resize: 'vertical',
              }}
            />
            <div style={{ marginTop: '8px', fontSize: '12px', color: '#556269', fontWeight: 600 }}>
              {t('mcq.wordCount')(essayWordCount)}
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '30px' }}>
            {isMulti && (
              <div style={{ fontSize: '12px', fontWeight: 700, color: '#556269', marginBottom: '2px' }}>
                {t('mcq.selectAllThatApply')}
              </div>
            )}
            {cqOptions.map((opt, idx) => (
              <button key={idx} className="mm-btn" onClick={() => selectOption(idx)} style={{
                textAlign: 'left', padding: '14px 18px', borderRadius: '14px', border: `1.5px solid ${opt.border}`,
                background: opt.bg, color: opt.color, cursor: 'pointer', fontFamily: 'Manrope', fontSize: '14px', fontWeight: 600,
              }}>{opt.text}</button>
            ))}
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <button className="mm-btn" onClick={goPrev} disabled={position === 0} style={{
            padding: '11px 22px', borderRadius: '100px', border: '1px solid rgba(31,55,75,0.15)', background: 'rgba(255,255,255,0.5)',
            color: '#556269', fontWeight: 700, fontSize: '13px', cursor: 'pointer', opacity: position === 0 ? 0.4 : 1,
          }}>{t('mcq.previous')}</button>
          <button
            className="mm-btn"
            disabled={isAdvancing}
            onClick={goNext}
            style={{
              padding: '11px 26px', borderRadius: '100px', border: 'none', background: '#2E5570', color: '#fff',
              fontWeight: 700, fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px',
            }}>
            {isAdvancing && <span className="mm-spinner" />}
            {cqNextLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
