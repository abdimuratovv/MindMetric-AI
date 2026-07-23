import { api, setToken } from './client.js';

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
