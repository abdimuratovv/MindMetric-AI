import { api, buildQuery } from './client.js';

/** Review queue — {{ teacherStudents }}, searchable and filterable by faculty/course/group. */
export const getTeacherStudents = (search, filters = {}) =>
  api.get(`/teacher/students/${buildQuery({ search, ...filters })}`);

/** Selected student detail — {{ selectedStudent }}. */
export const getTeacherStudentDetail = (studentId) => api.get(`/teacher/students/${studentId}/`);

/** {{ submitReview }}. */
export const submitReview = (studentId, rubricScores, comment) =>
  api.post(`/teacher/students/${studentId}/review/`, { rubric_scores: rubricScores, comment });
