import { api } from './client.js';

/** Review queue — {{ teacherStudents }}, searchable. */
export const getTeacherStudents = (search) =>
  api.get(`/teacher/students/${search ? `?search=${encodeURIComponent(search)}` : ''}`);

/** Selected student detail — {{ selectedStudent }}. */
export const getTeacherStudentDetail = (studentId) => api.get(`/teacher/students/${studentId}/`);

/** {{ submitReview }}. */
export const submitReview = (studentId, rubricScores, comment) =>
  api.post(`/teacher/students/${studentId}/review/`, { rubric_scores: rubricScores, comment });
