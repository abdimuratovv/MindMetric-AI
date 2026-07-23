import logoIcon from '../../assets/logo-icon.png';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import Achievements from './Achievements.jsx';
import AdminOverview from './AdminOverview.jsx';
import Analytics from './Analytics.jsx';
import QuestionBank from './QuestionBank.jsx';
import Results from './Results.jsx';
import StudentSelection from './StudentSelection.jsx';
import TeacherReview from './TeacherReview.jsx';

// Ported from `navConfigs` in renderVals() (lines 827-839). `labelKey` looks
// up the translated label at render time (see i18n/translations.js `nav`).
// Review Queue lives under `admin` now — the teacher role was removed (a
// teacher could only ever view student results, nothing else, so that
// screen is just another admin capability rather than its own role).
const NAV_CONFIGS = {
  student: [
    { key: 'selection', labelKey: 'assessments', iconPath: 'M3 3h8v8H3zM13 3h8v5h-8zM13 12h8v9h-8zM3 15h8v6H3z' },
    { key: 'results', labelKey: 'myResults', iconPath: 'M9 5h6a2 2 0 012 2v12a2 2 0 01-2 2H9a2 2 0 01-2-2V7a2 2 0 012-2zM9 3h6v4H9zM8 12l2 2 4-4' },
    { key: 'achievements', labelKey: 'achievements', iconPath: 'M12 2l2.4 5.8L20 9l-4.5 4 1.3 6-4.8-3-4.8 3 1.3-6L4 9l5.6-1.2z' },
  ],
  admin: [
    { key: 'admin', labelKey: 'overview', iconPath: 'M12 3l7 3v6c0 5-3.5 8-7 9-3.5-1-7-4-7-9V6z' },
    { key: 'teacherReview', labelKey: 'reviewQueue', iconPath: 'M17 21v-2a4 4 0 00-3-3.87M9 11a4 4 0 100-8 4 4 0 000 8zM3 21v-2a4 4 0 013-3.87M16 3.13a4 4 0 010 7.75' },
    { key: 'questionBank', labelKey: 'questionBank', iconPath: 'M9 4h6a1 1 0 011 1v1h1a2 2 0 012 2v11a2 2 0 01-2 2H7a2 2 0 01-2-2V8a2 2 0 012-2h1V5a1 1 0 011-1zM8 12h8M8 16h5' },
  ],
};

/**
 * Ported verbatim from MindMetric AI.dc.html lines 111-136 (`showShell`
 * sidebar) plus the content-area router (lines 138-514) that swaps in the
 * screen matching `screen`.
 */
export default function AppShell({ screen, goTo, user, logout }) {
  const { t } = useLanguage();
  const role = user?.role || 'student';
  const navItems = (NAV_CONFIGS[role] || NAV_CONFIGS.student).map((n) => ({
    ...n,
    label: t(`nav.${n.labelKey}`),
    bg: screen === n.key ? 'rgba(46,85,112,0.12)' : 'transparent',
    color: screen === n.key ? '#1F374B' : '#556269',
  }));

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex' }}>
      <aside style={{
        width: '246px', flexShrink: 0, padding: '24px 16px', display: 'flex', flexDirection: 'column',
        background: 'rgba(255,255,255,0.5)', borderRight: '1px solid rgba(255,255,255,0.7)', backdropFilter: 'blur(18px)',
        // Pin the sidebar to the viewport instead of stretching to match the
        // main content column's height — otherwise on tall pages (long
        // student/admin screens) the flex row's default `align-items: stretch`
        // stretches the aside too, and the profile/logout footer (pushed to
        // the bottom via `nav`'s flex:1) ends up far below the fold.
        position: 'sticky', top: 0, height: '100vh', alignSelf: 'flex-start', overflowY: 'auto',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '9px', padding: '8px 10px 22px' }}>
          <img src={logoIcon} alt="MindMetric AI" style={{ width: '28px', height: '28px', borderRadius: '8px' }} />
          <span style={{ fontWeight: 800, fontSize: '14.5px', color: '#161F24' }}>MindMetric AI</span>
        </div>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '3px', flex: 1 }}>
          {navItems.map((item) => (
            <button key={item.key} className="mm-btn" onClick={() => goTo(item.key)} style={{
              display: 'flex', alignItems: 'center', gap: '11px', padding: '11px 14px', borderRadius: '12px',
              border: 'none', cursor: 'pointer', textAlign: 'left', background: item.bg, color: item.color,
              fontFamily: 'Manrope', fontWeight: 600, fontSize: '13.5px',
            }}>
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
                <path d={item.iconPath}></path>
              </svg>
              {item.label}
            </button>
          ))}
        </nav>
        <div style={{
          display: 'flex', alignItems: 'center', gap: '10px', padding: '12px', borderRadius: '14px',
          background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.8)',
        }}>
          <div style={{
            width: '34px', height: '34px', borderRadius: '50%', background: '#DCECEF', display: 'flex',
            alignItems: 'center', justifyContent: 'center', fontWeight: 700, color: '#1F374B', fontSize: '13px',
          }}>{user?.initials}</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: '12.5px', fontWeight: 700, color: '#161F24', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {user?.name}
            </div>
            <div style={{ fontSize: '11px', color: '#939EA3' }}>{t(`roles.${role}`)}</div>
          </div>
          <button className="mm-btn" onClick={logout} title={t('nav.logout')} style={{ border: 'none', background: 'none', cursor: 'pointer', color: '#939EA3', padding: '4px' }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"></path>
            </svg>
          </button>
        </div>
      </aside>

      <div style={{ flex: 1, minWidth: 0, padding: '32px 44px 60px', overflowX: 'hidden' }}>
        {screen === 'selection' && <StudentSelection user={user} goTo={goTo} />}
        {screen === 'results' && <Results user={user} goTo={goTo} />}
        {screen === 'achievements' && <Achievements />}
        {screen === 'analytics' && <Analytics goTo={goTo} />}
        {screen === 'teacherReview' && <TeacherReview />}
        {screen === 'admin' && <AdminOverview />}
        {screen === 'questionBank' && <QuestionBank />}
      </div>
    </div>
  );
}
