import { api, buildQuery } from './client.js';

/** Institution overview screen — 4 parallel calls, mirrors adminLoading → adminLoaded. */
export const getAdminKpis = () => api.get('/admin/kpis/');
export const getCohortDistribution = () => api.get('/admin/distribution/');
export const getFieldDistribution = () => api.get('/admin/field-distribution/');
export const getFacultyActivity = () => api.get('/admin/faculty-activity/');
export const getAdminStudents = (search, filters = {}) =>
  api.get(`/admin/students/${buildQuery({ search, ...filters })}`);
/** Distinct faculty/course/group values (from students' onboarding survey) for the roster filter dropdowns. */
export const getStudentFilterOptions = () => api.get('/admin/student-filter-options/');
export const getQuestionBank = () => api.get('/admin/question-bank/');
export const createMcqQuestion = (payload) => api.post('/admin/question-bank/mcq/', payload);
export const updateMcqQuestion = (id, payload) => api.patch(`/admin/question-bank/mcq/${id}/`, payload);
export const deleteMcqQuestion = (id) => api.delete(`/admin/question-bank/mcq/${id}/`);
export const createLikertItem = (payload) => api.post('/admin/question-bank/likert/', payload);
export const updateLikertItem = (id, payload) => api.patch(`/admin/question-bank/likert/${id}/`, payload);
export const deleteLikertItem = (id) => api.delete(`/admin/question-bank/likert/${id}/`);
