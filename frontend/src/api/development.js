import { api } from './client.js';

const base = '/development';
export const getDevelopmentCapabilities = () => api.get(`${base}/capabilities/`);
export const getDevelopmentModules = () => api.get(`${base}/modules/`);
export const getDevelopmentPlan = () => api.get(`${base}/plan/`);
export const enrollDevelopment = (key) => api.post(`${base}/modules/${encodeURIComponent(key)}/enroll/`, {});
export const getDevelopmentEnrollment = (id) => api.get(`${base}/enrollments/${id}/`);
export const completeDevelopmentLesson = (id, key) => api.post(`${base}/enrollments/${id}/lessons/${encodeURIComponent(key)}/complete/`, {});
export const startDevelopmentSession = (id, purpose) => api.post(`${base}/enrollments/${id}/sessions/`, { purpose });
export const answerDevelopmentQuestion = (id, payload) => api.post(`${base}/sessions/${id}/answers/`, payload);
export const getDevelopmentHint = (id, key) => api.post(`${base}/sessions/${id}/hints/`, { exercise_key: key });
export const finishDevelopmentSession = (id) => api.post(`${base}/sessions/${id}/finish/`, {});
