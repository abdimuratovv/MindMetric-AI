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
