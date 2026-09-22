import { api, buildQuery } from './client.js';

/** Category/status vocabularies (server-localized) + the admins a student can address. */
export const getSupportOptions = () => api.get('/support/options/');

/**
 * The caller's own threads (student) or the inbox (admin). Admin-only filters:
 * {status, category, assignee: 'me'|'unassigned'|'all', search}.
 */
export const getSupportThreads = (filters = {}) => api.get(`/support/threads/${buildQuery(filters)}`);

/** Attachments always go as multipart, so text-only posts use the same path. */
function toFormData(fields, files = []) {
  const form = new FormData();
  Object.entries(fields).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') form.append(key, value);
  });
  files.forEach((file) => form.append('attachments', file, file.name));
  return form;
}

/**
 * Student opens a report. `assigneeId` omitted/empty means the shared "any
 * admin" queue; `files` are the already-compressed screenshots.
 */
export const createSupportThread = ({ category, subject, body, assigneeId }, files = []) =>
  api.postForm('/support/threads/', toFormData({ category, subject, body, assignee_id: assigneeId }, files));

/** Thread + full message history; clears the caller's unread counter server-side. */
export const getSupportThread = (id) => api.get(`/support/threads/${id}/`);

/** Reply, from either side. A message may be screenshots with no text. */
export const sendSupportMessage = (id, body, files = []) =>
  api.postForm(`/support/threads/${id}/messages/`, toFormData({ body }, files));

/** Messages newer than `afterId` — the open conversation's polling delta. */
export const getSupportMessagesAfter = (id, afterId) =>
  api.get(`/support/threads/${id}/messages/${buildQuery({ after: afterId })}`);

/** Admin queue management: {status} and/or {assignee_id}. */
export const updateSupportThread = (id, payload) => api.patch(`/support/threads/${id}/`, payload);

/** {threads, messages} for the sidebar badge — polled by AppShell. */
export const getSupportUnread = () => api.get('/support/unread/');
