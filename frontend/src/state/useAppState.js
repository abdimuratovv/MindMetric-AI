import { useCallback, useEffect, useState } from 'react';

import { getToken } from '../api/client.js';
import { logout as apiLogout, me } from '../api/auth.js';

const LANDING_BY_ROLE = { student: 'selection', admin: 'admin' };

// A student who hasn't submitted the one-time onboarding survey yet
// (profile_completed: false, from UserSerializer) is routed to it instead of
// straight to test-selection — see App.jsx's 'studentSurvey' branch.
function resolveLandingScreen(user) {
  if (user.role === 'student' && !user.profile_completed) return 'studentSurvey';
  return LANDING_BY_ROLE[user.role];
}

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
  // { callId, roomName, livekitUrl, token } while a video call is open —
  // set by TeacherReview's "start call" and AppShell's incoming-call banner,
  // both via enterCall(). See pages/VideoCall/VideoCallPage.jsx.
  const [activeCall, setActiveCall] = useState(null);
  const [screenBeforeCall, setScreenBeforeCall] = useState('selection');

  // The mockup has no equivalent of this — its `state` lived only in memory,
  // so a refresh always dropped back to Welcome. A real JWT survives a
  // refresh in localStorage, so a mount with a stored token should resume
  // the session instead of stranding a signed-in user on the landing page.
  useEffect(() => {
    if (!getToken()) return;
    me().then((loggedInUser) => {
      setUser(loggedInUser);
      setScreen(resolveLandingScreen(loggedInUser));
    }).catch(() => {}); // expired/invalid token — stay on Welcome, same as no token
  }, []);

  const goTo = useCallback((next) => setScreen(next), []);

  const enterCall = useCallback((callInfo) => {
    setScreenBeforeCall(screen);
    setActiveCall(callInfo);
    setScreen('videoCall');
  }, [screen]);

  const leaveCall = useCallback(() => {
    setActiveCall(null);
    setScreen((current) => (current === 'videoCall' ? screenBeforeCall : current));
  }, [screenBeforeCall]);

  const onLoginSuccess = useCallback((loggedInUser) => {
    setUser(loggedInUser);
    setScreen(resolveLandingScreen(loggedInUser));
  }, []);

  const onProfileCompleted = useCallback((updatedUser) => {
    setUser(updatedUser);
    setScreen('selection');
  }, []);

  const logout = useCallback(async () => {
    await apiLogout();
    setUser(null);
    setActiveCall(null);
    setScreen('welcome');
  }, []);

  return { screen, goTo, user, onLoginSuccess, onProfileCompleted, logout, activeCall, enterCall, leaveCall };
}
