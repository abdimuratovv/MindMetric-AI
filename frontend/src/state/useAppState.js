import { useCallback, useEffect, useState } from 'react';

import { getToken } from '../api/client.js';
import { logout as apiLogout, me } from '../api/auth.js';

const LANDING_BY_ROLE = { student: 'selection', teacher: 'teacherReview', admin: 'admin' };

/**
 * Client-side navigation state — the parts of the mockup's `Component.state`
 * that stay purely client-side even in the real app: `screen` and `role`.
 * Everything else that used to live in `state` (completed{}, cqAnswers,
 * behavioralAnswers, teacherSearch, adminSearch, …) now lives server-side
 * (see StudentStateTracker) or in the owning page component's own local
 * state, fetched fresh each time that screen mounts.
 */
export function useAppState() {
  const [screen, setScreen] = useState('welcome');
  const [user, setUser] = useState(null); // { id, name, initials, role, program }

  // The mockup has no equivalent of this — its `state` lived only in memory,
  // so a refresh always dropped back to Welcome. A real JWT survives a
  // refresh in localStorage, so a mount with a stored token should resume
  // the session instead of stranding a signed-in user on the landing page.
  useEffect(() => {
    if (!getToken()) return;
    me().then((loggedInUser) => {
      setUser(loggedInUser);
      setScreen(LANDING_BY_ROLE[loggedInUser.role]);
    }).catch(() => {}); // expired/invalid token — stay on Welcome, same as no token
  }, []);

  const goTo = useCallback((next) => setScreen(next), []);

  const onLoginSuccess = useCallback((loggedInUser) => {
    setUser(loggedInUser);
    setScreen(LANDING_BY_ROLE[loggedInUser.role]);
  }, []);

  const logout = useCallback(async () => {
    await apiLogout();
    setUser(null);
    setScreen('welcome');
  }, []);

  return { screen, goTo, user, onLoginSuccess, logout };
}
