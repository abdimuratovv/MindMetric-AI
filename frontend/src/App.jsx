import PageBackground from './components/PageBackground.jsx';
import { ASSESSMENT_TYPES } from './constants/assessments.js';
import AppShell from './pages/Shell/AppShell.jsx';
import Auth from './pages/Auth.jsx';
import FocusedTestShell from './pages/FocusedTest/FocusedTestShell.jsx';
import StudentSurvey from './pages/StudentSurvey.jsx';
import VideoCallPage from './pages/VideoCall/VideoCallPage.jsx';
import Welcome from './pages/Welcome.jsx';
import { useAppState } from './state/useAppState.js';

const SHELL_SCREENS = ['selection', 'results', 'achievements', 'analytics', 'teacherReview', 'admin', 'questionBank'];

/**
 * Top-level router. Mirrors the mockup's four mutually-exclusive `sc-if`
 * blocks (isWelcome / isAuth / showShell / isFocusedTest, lines 29-620) —
 * same branching, now driven by real navigation state instead of
 * `Component.state.screen`. 'videoCall' is a fifth, full-screen branch
 * (no sidebar), same tier as the assessment-type branch below it.
 */
export default function App() {
  const { screen, goTo, user, onLoginSuccess, onProfileCompleted, logout, activeCall, enterCall, leaveCall } = useAppState();

  return (
    <PageBackground>
      {screen === 'welcome' && (
        <Welcome onGoAuth={() => goTo('auth')} />
      )}
      {screen === 'auth' && <Auth onLoginSuccess={onLoginSuccess} onGoWelcome={() => goTo('welcome')} />}
      {screen === 'studentSurvey' && (
        <StudentSurvey user={user} onComplete={onProfileCompleted} onLogout={logout} />
      )}
      {ASSESSMENT_TYPES.includes(screen) && <FocusedTestShell screen={screen} goTo={goTo} />}
      {screen === 'videoCall' && <VideoCallPage call={activeCall} onLeave={leaveCall} />}
      {SHELL_SCREENS.includes(screen) && (
        <AppShell screen={screen} goTo={goTo} user={user} logout={logout} enterCall={enterCall} />
      )}
    </PageBackground>
  );
}
