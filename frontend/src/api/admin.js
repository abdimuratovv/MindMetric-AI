import { api, buildQuery, downloadFile } from './client.js';

/** Institution overview screen. `filters` ({faculty, course, group}) narrow every widget, not just the table. */
export const getAdminKpis = (filters = {}) => api.get(`/admin/kpis/${buildQuery(filters)}`);
export const getCohortDistribution = (filters = {}) => api.get(`/admin/distribution/${buildQuery(filters)}`);
export const getFieldDistribution = (filters = {}) => api.get(`/admin/field-distribution/${buildQuery(filters)}`);
export const getFacultyActivity = (filters = {}) => api.get(`/admin/faculty-activity/${buildQuery(filters)}`);
/** Paginated: resolves to {results, total, page, pageSize}. `ordering` is e.g. 'score' / '-date'. */
export const getAdminStudents = ({ search, ordering, page, pageSize, ...filters } = {}) =>
  api.get(`/admin/students/${buildQuery({ search, ordering, page, pageSize, ...filters })}`);
/** One student's full report: {student, review, summary, mistakes}. */
export const getAdminStudentDetail = (id) => api.get(`/admin/students/${id}/`);
/** Downloads every student matching the search/filters/sort (not just the visible page) as CSV. */
export const downloadStudentsCsv = ({ search, ordering, ...filters } = {}) =>
  downloadFile(`/admin/students/export/${buildQuery({ search, ordering, ...filters })}`, 'students.csv');
/** Institution name + academic term ({name, academicTerm}) shown in the dashboard header. */
export const getInstitutionSettings = () => api.get('/admin/settings/');
export const updateInstitutionSettings = (payload) => api.patch('/admin/settings/', payload);
/** Distinct faculty/course/group values (from students' onboarding survey) for the roster filter dropdowns. */
export const getStudentFilterOptions = () => api.get('/admin/student-filter-options/');
export const getQuestionBank = () => api.get('/admin/question-bank/');
export const createMcqQuestion = (payload) => api.post('/admin/question-bank/mcq/', payload);
export const updateMcqQuestion = (id, payload) => api.patch(`/admin/question-bank/mcq/${id}/`, payload);
export const deleteMcqQuestion = (id) => api.delete(`/admin/question-bank/mcq/${id}/`);
