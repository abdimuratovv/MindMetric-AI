import { useCallback, useEffect, useState } from 'react';

import { SESSION_ENDED_EVENT, getToken } from '../api/client.js';
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
const NO_FILTERS = { faculty: '', course: '', group: '' };

// Dashboard: just the faculty/course/group filters that narrow its widgets.
export const INITIAL_ADMIN_VIEW = { filters: NO_FILTERS };

// Students roster: filters, search, sort and paging.
export const INITIAL_STUDENTS_VIEW = {
  search: '',
  filters: NO_FILTERS,
  level: '',
  status: '',
  sort: { field: 'name', direction: 'asc' },
  page: 1,
  pageSize: 10,
};

// Support inbox: queue filters plus which thread is open. Same reason as the
// two views above — an admin who opens a student's report from a thread should
// come back to that thread, not to an empty queue.
export const INITIAL_SUPPORT_VIEW = {
  selectedId: null,
  filters: { assignee: 'all', status: '', category: '', search: '' },
};

// Screens a student report can be opened from and returned to. Anything else
// (the dashboard's own widgets) falls back to the overview, as before.
const STUDENT_RETURN_SCREENS = ['adminStudents', 'supportInbox'];

export function useAppState() {
  const [screen, setScreen] = useState('welcome');
  const [user, setUser] = useState(null); // { id, name, initials, role, program }
  // { callId, roomName, livekitUrl, token } while a video call is open —
  // set by TeacherReview's "start call" and AppShell's incoming-call banner,
  // both via enterCall(). See pages/VideoCall/VideoCallPage.jsx.
  const [activeCall, setActiveCall] = useState(null);
  const [screenBeforeCall, setScreenBeforeCall] = useState('selection');
  const [selectedStudentId, setSelectedStudentId] = useState(null); // admin's open student report
  // Dashboard filters/search/sort/page live here (not in AdminOverview) so they survive opening a student and coming back.
  const [adminView, setAdminView] = useState(INITIAL_ADMIN_VIEW);
  const [studentsView, setStudentsView] = useState(INITIAL_STUDENTS_VIEW);
  const [supportView, setSupportView] = useState(INITIAL_SUPPORT_VIEW);
  const [studentReturnScreen, setStudentReturnScreen] = useState('admin'); // where "back" leads from a student report

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

  const openStudent = useCallback((id) => {
    setStudentReturnScreen(STUDENT_RETURN_SCREENS.includes(screen) ? screen : 'admin');
    setSelectedStudentId(id);
    setScreen('adminStudent');
  }, [screen]);

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

  // Profile settings saved a new name — refreshes the sidebar without leaving the screen.
  const updateUser = useCallback((updatedUser) => setUser(updatedUser), []);

  const resetSession = useCallback(() => {
    setUser(null);
    setActiveCall(null);
    setAdminView(INITIAL_ADMIN_VIEW);
    setStudentsView(INITIAL_STUDENTS_VIEW);
    setSupportView(INITIAL_SUPPORT_VIEW);
    setScreen('welcome');
  }, []);

  const logout = useCallback(async () => {
    await apiLogout();
    resetSession();
  }, [resetSession]);

  // The server refused this tab's token (see api/client.js) — e.g. the password
  // was changed on another device — so nothing signed-in can load any more.
  useEffect(() => {
    window.addEventListener(SESSION_ENDED_EVENT, resetSession);
    return () => window.removeEventListener(SESSION_ENDED_EVENT, resetSession);
  }, [resetSession]);

  return { screen, goTo, openStudent, selectedStudentId, adminView, setAdminView, studentsView, setStudentsView, supportView, setSupportView, studentReturnScreen, user, onLoginSuccess, onProfileCompleted, updateUser, logout, activeCall, enterCall, leaveCall };
}
