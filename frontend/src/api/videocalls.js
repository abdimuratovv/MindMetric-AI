import { api } from './client.js';

/** Admin starts a call with a student — {{ startCall }}. */
export const startCall = (studentId) => api.post('/videocalls/start/', { student_id: studentId });

/** Polled by the student side to detect an incoming call. Resolves to `null` when there is none. */
export const getActiveCall = () => api.get('/videocalls/active/');

/** Either participant joins/rejoins an existing call and gets a fresh LiveKit token. */
export const joinCall = (callId) => api.post(`/videocalls/${callId}/join/`);

/** Either participant ends the call. */
export const endCall = (callId) => api.post(`/videocalls/${callId}/end/`);
