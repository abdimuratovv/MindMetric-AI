import { api, buildQuery } from './client.js';

/** Category/status vocabularies (server-localized) + the admins a student can address. */
export const getSupportOptions = () => api.get('/support/options/');

/**
 * The caller's own threads (student) or the inbox (admin). Admin-only filters:
 * {status, category, assignee: 'me'|'unassigned'|'all', search}.
 */
export const getSupportThreads = (filters = {}) => api.get(`/support/threads/${buildQuery(filters)}`);

/** Student opens a report. `assigneeId` omitted/empty means the shared "any admin" queue. */
export const createSupportThread = ({ category, subject, body, assigneeId }) =>
  api.post('/support/threads/', { category, subject, body, assignee_id: assigneeId || null });

/** Thread + full message history; clears the caller's unread counter server-side. */
export const getSupportThread = (id) => api.get(`/support/threads/${id}/`);

/** Reply, from either side. */
export const sendSupportMessage = (id, body) => api.post(`/support/threads/${id}/messages/`, { body });

/** Admin queue management: {status} and/or {assignee_id}. */
export const updateSupportThread = (id, payload) => api.patch(`/support/threads/${id}/`, payload);
