import { api } from './client.js';

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

/** Likert pattern — teamwork, patience, learning_speed. */
export const startLikert = (type) => api.post(`/assessments/likert/${type}/start/`, {});
export const getLikertItems = (type) => api.get(`/assessments/likert/${type}/items/`);
export const answerLikert = (type, itemId, value) =>
  api.patch(`/assessments/likert/${type}/answer/`, { item_id: itemId, value });
export const submitLikert = (type) => api.post(`/assessments/likert/${type}/submit/`, {});

/** Generic "start" dispatcher used by StudentSelection's card list. `hybrid`
 * (algorithmic) always begins at its MCQ phase, same as plain `mcq` types —
 * Hybrid.jsx's own Coding phase calls startCoding() once that phase is reached. */
export const startAssessment = (type, pattern) => {
  if (pattern === 'mcq' || pattern === 'hybrid') return startMcq(type);
  if (pattern === 'likert') return startLikert(type);
  return startCoding();
};

/** "Save & exit" on the focused-test header. */
export const pauseAttempt = (assessmentType, timeRemainingSeconds) =>
  api.post(`/assessments/${assessmentType}/pause/`, { time_remaining_seconds: timeRemainingSeconds });
