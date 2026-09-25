import { api, setToken, withTokenRotation } from './client.js';

/** Backs auth.jsx's `doLogin`. */
export async function login(email, password, role) {
  const data = await api.post('/auth/login/', { email, password, role });
  setToken(data.access);
  return data.user;
}

export async function logout() {
  await api.post('/auth/logout/', {});
  setToken(null);
}

export function me() {
  return api.get('/accounts/me/');
}

/** Backs auth.jsx's `doRegister`. Does not touch the token — registering never logs the user in. */
export function register(firstName, lastName, email, password) {
  return api.post('/auth/register/', { first_name: firstName, last_name: lastName, email, password });
}

/** Backs StudentSurvey's submit. Returns the updated user (profile_completed: true). */
export function completeProfile({ faculty, course, group, specialization }) {
  return api.post('/accounts/complete-profile/', { faculty, course, group, specialization });
}

/** Profile settings form values: names and email, plus the survey fields for a student. */
export function getProfile() {
  return api.get('/accounts/profile/');
}

/** Returns {profile, user} — the refreshed form values and the sidebar's user payload. */
export function updateProfile(fields) {
  return api.patch('/accounts/profile/', fields);
}

/**
 * Both of these end every other session server-side (User.tokens_valid_after),
 * including the token this tab holds, so the fresh one they return replaces it.
 */
export async function changePassword(currentPassword, newPassword) {
  await withTokenRotation(() => api.post('/accounts/change-password/', { current_password: currentPassword, new_password: newPassword }));
}

export async function signOutEverywhere() {
  await withTokenRotation(() => api.post('/accounts/sign-out-everywhere/', {}));
}
