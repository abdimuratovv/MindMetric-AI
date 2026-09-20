import { api } from './client.js';

/** Effective per-indicator question counts / time limits ({math: {questions, minutes}, ...}). */
export const getAssessmentConfig = () => api.get('/assessments/config/');

/** Selection screen — {{ assessments }} status badges. */
export const getStatus = () => api.get('/assessments/status/');

/**
 * MCQ pattern — math, logic, algorithmic, creative, problem_solving, attention, iq.
 * `payload` is `{selected_indices, response_time_ms}` for single/multi-select questions or
 * `{essay_text, response_time_ms}` for essay/open-ended ones (see CognitiveQuestion.QuestionType
 * on the backend). `response_time_ms` feeds AdaptiveTestingEngine's speed-aware difficulty step.
 */
export const startMcq = (type) => api.post(`/assessments/mcq/${type}/start/`, {});
export const getMcqNextQuestion = (type) => api.get(`/assessments/mcq/${type}/next-question/`);
export const answerMcq = (type, questionId, payload) =>
  api.post(`/assessments/mcq/${type}/answer/`, { question_id: questionId, ...payload });
export const submitMcq = (type) => api.post(`/assessments/mcq/${type}/submit/`, {});

/**
 * Coding pattern — algorithmic (the only member). Runs CODING_TASK_CAP distinct
 * problems per attempt; getCodingProblem returns the next unseen one (mirrors
 * getMcqNextQuestion's {question, cqNumber, cqTotal} as {problem, cpNumber, cpTotal}).
 * `elapsedMs` is client-measured time on that one problem (shown → submitted),
 * mirroring answerMcq's response_time_ms.
 */
export const startCoding = () => api.post('/assessments/coding/start/', {});
export const getCodingProblem = () => api.get('/assessments/coding/problem/');
export const runCode = (problemId, code) => api.post('/assessments/coding/run/', { problem_id: problemId, code });
export const submitCoding = (problemId, code, elapsedMs) =>
  api.post('/assessments/coding/submit/', { problem_id: problemId, code, elapsed_ms: elapsedMs });
/** Same endpoint with no problem_id — "finish the coding phase" when getCodingProblem
 * has no task left to serve (the cap was lowered under an attempt already past it, or
 * the pool ran dry). Mirrors Mcq.jsx's submitMcq() on a null question; without it the
 * student is stranded on a screen that can never load a problem. */
export const finishCoding = () => api.post('/assessments/coding/submit/', {});

/**
 * Learning pattern — learning_speed. getLearningState returns the current module
 * (rules), block and its unanswered items; the answer that completes a block
 * returns that block's feedback.
 */
export const startLearning = () => api.post('/assessments/learning/start/', {});
export const getLearningState = () => api.get('/assessments/learning/state/');
export const answerLearning = (itemId, selectedIndex, responseTimeMs) =>
  api.post('/assessments/learning/answer/', { item_id: itemId, selected_index: selectedIndex, response_time_ms: responseTimeMs });
export const submitLearning = () => api.post('/assessments/learning/submit/', {});

/**
 * SJT pattern — teamwork. getSjtNext returns {scenario: {id, situation, options: [{index, text}]}, number, total}
 * (options arrive shuffled; answers send back each option's original `index`), or scenario: null when done.
 */
export const startSjt = () => api.post('/assessments/sjt/start/', {});
export const getSjtNext = () => api.get('/assessments/sjt/next/');
export const answerSjt = (scenarioId, bestIndex, worstIndex, responseTimeMs) =>
  api.post('/assessments/sjt/answer/', {
    scenario_id: scenarioId, best_index: bestIndex, worst_index: worstIndex, response_time_ms: responseTimeMs,
  });
export const submitSjt = () => api.post('/assessments/sjt/submit/', {});

/**
 * Anagram pattern — patience. getAnagramCurrent returns {item: {id, letters, activeMs}, number, total}
 * or item: null when every anagram is solved or skipped. `activeMs` is the time the student
 * was actually working on the item (tab visible, recent input) — resumed from the server on refresh.
 */
export const startAnagram = () => api.post('/assessments/anagram/start/', {});
export const getAnagramCurrent = () => api.get('/assessments/anagram/current/');
export const guessAnagram = (itemId, guess, activeMs) =>
  api.post('/assessments/anagram/guess/', { item_id: itemId, guess, active_ms: activeMs });
export const skipAnagram = (itemId, activeMs) =>
  api.post('/assessments/anagram/skip/', { item_id: itemId, active_ms: activeMs });
export const submitAnagram = () => api.post('/assessments/anagram/submit/', {});

/** Generic "start" dispatcher used by StudentSelection's card list. `hybrid`
 * (algorithmic) always begins at its MCQ phase, same as plain `mcq` types —
 * Hybrid.jsx's own Coding phase calls startCoding() once that phase is reached. */
export const startAssessment = (type, pattern) => {
  if (pattern === 'mcq' || pattern === 'hybrid') return startMcq(type);
  if (pattern === 'anagram') return startAnagram();
  if (pattern === 'learning') return startLearning();
  if (pattern === 'sjt') return startSjt();
  return startCoding();
};

/** "Save & exit" on the focused-test header. */
export const pauseAttempt = (assessmentType, timeRemainingSeconds) =>
  api.post(`/assessments/${assessmentType}/pause/`, { time_remaining_seconds: timeRemainingSeconds });
