/**
 * Thin fetch wrapper: attaches the JWT, serializes JSON, throws on non-2xx
 * with the server's {detail} message so callers can surface it verbatim
 * (e.g. into {{ loginError }} / {{ behavioralError }}).
 */
import { getStoredLanguage } from '../i18n/LanguageContext.jsx';

const TOKEN_KEY = 'mindmetric_access_token';

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json', 'X-Language': getStoredLanguage() };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`/api${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (res.status === 204) return null;

  const data = await res.json().catch(() => null);
  if (!res.ok) {
    // An expired/invalid access token still gets attached above and rejected by
    // JWTAuthentication before permission checks run — that would otherwise 401
    // every request, including AllowAny ones like /public/stats/. Drop it so the
    // app falls back to a logged-out state instead of repeating a dead token.
    if (res.status === 401 && token) setToken(null);
    throw new Error(data?.detail || `Request failed: ${res.status}`);
  }
  return data;
}

export const api = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),
  patch: (path, body) => request('PATCH', path, body),
  delete: (path) => request('DELETE', path),
};
