import { useState } from 'react';

import { completeProfile } from '../api/auth.js';
import logoIcon from '../assets/logo-icon.png';
import { useLanguage } from '../i18n/LanguageContext.jsx';

/** Same label+input look as Auth.jsx's AuthField. */
function SurveyField({ label, value, onChange, placeholder, focused, onFocus, onBlur }) {
  return (
    <>
      <label style={{ display: 'block', fontSize: '12.5px', fontWeight: 600, color: '#1F374B', marginBottom: '6px' }}>{label}</label>
      <input
        value={value}
        onChange={onChange}
        onFocus={onFocus}
        onBlur={onBlur}
        placeholder={placeholder}
        style={{
          width: '100%', padding: '12px 14px', borderRadius: '12px',
          border: `1px solid ${focused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
          boxShadow: focused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
          transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
          background: 'rgba(255,255,255,0.7)', fontFamily: 'Manrope', fontSize: '14px', color: '#161F24',
          marginBottom: '16px', outline: 'none',
        }}
      />
    </>
  );
}

/**
 * One-time onboarding survey shown right after a new student's first login,
 * before they can reach test-selection (App.jsx routes here instead of
 * 'selection' until profile_completed is true — see useAppState.js). No
 * sidebar, no way to navigate away except logging out — the student can't
 * skip this by design.
 */
export default function StudentSurvey({ user, onComplete, onLogout }) {
  const [faculty, setFaculty] = useState('');
  const [course, setCourse] = useState('');
  const [group, setGroup] = useState('');
  const [specialization, setSpecialization] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [facultyFocused, setFacultyFocused] = useState(false);
  const [courseFocused, setCourseFocused] = useState(false);
  const [groupFocused, setGroupFocused] = useState(false);
  const [specializationFocused, setSpecializationFocused] = useState(false);
  const { t } = useLanguage();

  const doSubmit = async () => {
    if (!faculty.trim() || !course.trim() || !group.trim() || !specialization.trim()) {
      setError(t('survey.missingFields'));
      return;
    }
    setIsSubmitting(true);
    try {
      const updatedUser = await completeProfile({ faculty, course, group, specialization });
      onComplete(updatedUser);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const firstName = user?.name ? user.name.split(' ')[0] : '';

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
      <div style={{
        width: '100%', maxWidth: '460px', padding: 'clamp(26px,7vw,40px) clamp(20px,6vw,36px)', borderRadius: '24px', background: 'rgba(255,255,255,0.6)',
        border: '1px solid rgba(255,255,255,0.9)', backdropFilter: 'blur(20px)', boxShadow: '0 20px 60px rgba(31,55,75,0.1)',
        animation: 'mm-fade-up 0.5s ease both',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '26px', width: 'fit-content' }}>
          <img src={logoIcon} alt="MindMetric AI" style={{ width: '30px', height: '30px', borderRadius: '8px' }} />
          <span style={{ fontWeight: 800, fontSize: '16px', color: '#161F24' }}>{t('common.brand')}</span>
        </div>
        <h2 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '28px', color: '#161F24', margin: '0 0 6px' }}>
          {firstName ? t('survey.greeting')(firstName) : t('survey.title')}
        </h2>
        <p style={{ fontSize: '13.5px', color: '#556269', margin: '0 0 22px' }}>
          {t('survey.subtitle')}
        </p>

        <SurveyField
          label={t('survey.facultyLabel')}
          value={faculty}
          onChange={(e) => { setFaculty(e.target.value); setError(''); }}
          onFocus={() => setFacultyFocused(true)}
          onBlur={() => setFacultyFocused(false)}
          placeholder={t('survey.facultyPlaceholder')}
          focused={facultyFocused}
        />
        <SurveyField
          label={t('survey.courseLabel')}
          value={course}
          onChange={(e) => { setCourse(e.target.value); setError(''); }}
          onFocus={() => setCourseFocused(true)}
          onBlur={() => setCourseFocused(false)}
          placeholder={t('survey.coursePlaceholder')}
          focused={courseFocused}
        />
        <SurveyField
          label={t('survey.groupLabel')}
          value={group}
          onChange={(e) => { setGroup(e.target.value); setError(''); }}
          onFocus={() => setGroupFocused(true)}
          onBlur={() => setGroupFocused(false)}
          placeholder={t('survey.groupPlaceholder')}
          focused={groupFocused}
        />
        <SurveyField
          label={t('survey.specializationLabel')}
          value={specialization}
          onChange={(e) => { setSpecialization(e.target.value); setError(''); }}
          onFocus={() => setSpecializationFocused(true)}
          onBlur={() => setSpecializationFocused(false)}
          placeholder={t('survey.specializationPlaceholder')}
          focused={specializationFocused}
        />

        {error && (
          <div style={{
            display: 'flex', gap: '8px', alignItems: 'center', padding: '10px 12px', borderRadius: '10px',
            background: '#F6E0DC', color: '#BD5B4C', fontSize: '12.5px', fontWeight: 600, margin: '8px 0',
          }}>
            <span>⚠</span><span>{error}</span>
          </div>
        )}

        <button
          className="mm-btn"
          disabled={isSubmitting}
          onClick={doSubmit}
          style={{
            width: '100%', padding: '13px 0', borderRadius: '100px', border: 'none', cursor: 'pointer',
            background: '#2E5570', color: '#fff', fontFamily: 'Manrope', fontWeight: 700, fontSize: '14.5px',
            boxShadow: '0 10px 24px rgba(46,85,112,0.25)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
            marginTop: '8px',
          }}>
          {isSubmitting && <span className="mm-spinner" />}
          {t('survey.submitButton')}
        </button>

        <p style={{ textAlign: 'center', fontSize: '12px', margin: '16px 0 0' }}>
          <a href="#" onClick={(e) => { e.preventDefault(); onLogout(); }} style={{ color: '#556269', fontWeight: 600, textDecoration: 'none' }}>
            {t('survey.logout')}
          </a>
        </p>
      </div>
    </div>
  );
}
