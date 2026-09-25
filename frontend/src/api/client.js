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

// Credential endpoints never need a token; a stale one would be rejected by
// JWTAuthentication ("Given token not valid for any token type") before AllowAny applies.
const TOKENLESS_PATHS = ['/auth/login/', '/auth/register/'];

// Fired when the server refuses the stored token — expired, or revoked by a
// password change / "sign out everywhere" on another device. useAppState
// listens and returns to the landing page, instead of leaving a signed-in
// screen whose every request now fails.
export const SESSION_ENDED_EVENT = 'mindmetric:session-ended';

let rotatingToken = false;

/**
 * Runs a request that swaps this tab's token for a fresh one (password change,
 * sign out everywhere). The server revokes the old token before the response
 * arrives, so a background poll landing in that gap gets a 401 that doesn't
 * mean this session is over — see the 401 checks below.
 */
export async function withTokenRotation(sendRequest) {
  rotatingToken = true;
  try {
    const data = await sendRequest();
    setToken(data.access);
    return data;
  } finally {
    rotatingToken = false;
  }
}

/** A 401 ends the session only for the token this tab still holds, and not mid-rotation. */
function handleUnauthorized(sentToken) {
  if (!sentToken || rotatingToken || sentToken !== getToken()) return;
  setToken(null);
  window.dispatchEvent(new Event(SESSION_ENDED_EVENT));
}

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json', 'X-Language': getStoredLanguage() };
  const token = TOKENLESS_PATHS.includes(path) ? null : getToken();
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
    if (res.status === 401) handleUnauthorized(token);
    throw new Error(data?.detail || `Request failed: ${res.status}`);
  }
  return data;
}

/**
 * Multipart POST — for the support screenshots, which can't ride in a JSON
 * body. Content-Type is deliberately left unset so the browser adds the
 * multipart boundary itself.
 */
async function postForm(path, formData) {
  const headers = { 'X-Language': getStoredLanguage() };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`/api${path}`, { method: 'POST', headers, body: formData });
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    if (res.status === 401) handleUnauthorized(token);
    throw new Error(data?.detail || `Request failed: ${res.status}`);
  }
  return data;
}

export const api = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),
  postForm,
  patch: (path, body) => request('PATCH', path, body),
  delete: (path) => request('DELETE', path),
};

/**
 * Authenticated image fetch as an object URL. A plain <img src="/api/…"> can't
 * carry the JWT, and support attachments are permission-checked per request
 * (apps.support.views.AttachmentView), so the bytes are fetched here instead.
 * Callers must URL.revokeObjectURL() when the image unmounts.
 */
export async function fetchBlobUrl(path) {
  const headers = {};
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`/api${path}`, { headers });
  if (!res.ok) throw new Error(`Fetch failed: ${res.status}`);
  return URL.createObjectURL(await res.blob());
}

/** Builds a `?key=value&...` query string, skipping empty/falsy values (e.g. unset filters). */
export function buildQuery(params) {
  const qs = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => { if (value) qs.set(key, value); });
  const s = qs.toString();
  return s ? `?${s}` : '';
}

/** Authenticated file download (the JWT can't ride on a plain <a href>): fetches `path` and saves it under `filename`. */
export async function downloadFile(path, filename) {
  const headers = { 'X-Language': getStoredLanguage() };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`/api${path}`, { headers });
  if (!res.ok) throw new Error(`Download failed: ${res.status}`);
  const url = URL.createObjectURL(await res.blob());
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}
