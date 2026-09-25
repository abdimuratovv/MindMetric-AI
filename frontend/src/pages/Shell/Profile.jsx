import { useEffect, useState } from 'react';

import { changePassword, getProfile, signOutEverywhere, updateProfile } from '../../api/auth.js';
import LanguageSwitcher from '../../components/LanguageSwitcher.jsx';
import PasswordVisibilityToggle from '../../components/PasswordVisibilityToggle.jsx';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

// Same field look as AdminSettings, so the two settings screens read as one family.
const INPUT_STYLE = {
  width: '100%', boxSizing: 'border-box', padding: '11px 14px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.14)',
  fontSize: '14px', fontFamily: 'Manrope', outline: 'none', background: 'rgba(255,255,255,0.85)', color: '#161F24',
};
const LABEL_STYLE = { display: 'block', fontSize: '12.5px', fontWeight: 700, color: '#556269', marginBottom: '6px' };
const CARD_STYLE = {
  padding: '24px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)',
  backdropFilter: 'blur(14px)', display: 'flex', flexDirection: 'column', gap: '16px',
};
const CARD_TITLE_STYLE = { fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '18px', color: '#161F24', margin: 0 };
const CARD_HINT_STYLE = { fontSize: '13px', color: '#556269', margin: '4px 0 0', lineHeight: 1.5 };
const GRID_STYLE = { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px 16px' };

const primaryButtonStyle = (busy) => ({
  padding: '10px 22px', borderRadius: '10px', border: 'none', background: '#1F374B', color: '#fff',
  fontFamily: 'Manrope', fontWeight: 700, fontSize: '13.5px', cursor: busy ? 'default' : 'pointer', opacity: busy ? 0.6 : 1,
});

const NAME_FIELDS = ['first_name', 'last_name'];
// The onboarding-survey answers; the profile endpoint only sends these for students.
const STUDY_FIELDS = ['faculty', 'course', 'group', 'specialization'];
const NO_PASSWORDS = { current: '', next: '', confirm: '' };

function StatusMessage({ message }) {
  if (!message) return null;
  return <span role="status" style={{ fontSize: '13px', fontWeight: 600, color: message.error ? '#BD5B4C' : '#2E7052' }}>{message.text}</span>;
}

function PasswordField({ id, label, value, onChange, autoComplete }) {
  const { t } = useLanguage();
  const [visible, setVisible] = useState(false);
  return (
    <div>
      <label htmlFor={id} style={LABEL_STYLE}>{label}</label>
      <div style={{ position: 'relative' }}>
        <input
          id={id} type={visible ? 'text' : 'password'} value={value} autoComplete={autoComplete}
          onChange={(e) => onChange(e.target.value)} style={{ ...INPUT_STYLE, paddingRight: '42px' }}
        />
        <PasswordVisibilityToggle
          visible={visible} onToggle={() => setVisible((v) => !v)}
          label={visible ? t('auth.hidePassword') : t('auth.showPassword')}
        />
      </div>
    </div>
  );
}

/**
 * Profile settings for every role: name (plus the onboarding-survey answers for
 * a student), password, interface language, and ending other sessions. Email
 * is shown but not editable — it is the login (see ProfileUpdateSerializer).
 */
export default function Profile({ onUserUpdated }) {
  const { t } = useLanguage();
  const [saved, setSaved] = useState(null); // the profile as last returned by the server
  const [form, setForm] = useState(null);
  const [loadError, setLoadError] = useState(false);
  const [saving, setSaving] = useState(false);
  const [profileMessage, setProfileMessage] = useState(null); // {text, error}

  const [passwords, setPasswords] = useState(NO_PASSWORDS);
  const [changingPassword, setChangingPassword] = useState(false);
  const [passwordMessage, setPasswordMessage] = useState(null);

  const [signingOut, setSigningOut] = useState(false);
  const [sessionsMessage, setSessionsMessage] = useState(null);

  useEffect(() => {
    getProfile()
      .then((profile) => { setSaved(profile); setForm(profile); })
      .catch(() => setLoadError(true));
  }, []);

  const header = (
    <>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('profile.title')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 6px' }}>{t('profile.subtitle')}</p>
    </>
  );

  if (loadError) {
    return (
      <div style={{ animation: 'mm-fade-up 0.4s ease both', maxWidth: '760px', display: 'flex', flexDirection: 'column', gap: '18px' }}>
        <div>{header}</div>
        <StatusMessage message={{ text: t('profile.loadError'), error: true }} />
      </div>
    );
  }
  if (!form) return null;

  const isStudent = saved.role === 'student';
  const editableFields = isStudent ? [...NAME_FIELDS, ...STUDY_FIELDS] : NAME_FIELDS;
  const dirty = editableFields.some((field) => form[field] !== saved[field]);
  const initials = `${saved.first_name.charAt(0)}${saved.last_name.charAt(0)}`.toUpperCase() || saved.email.charAt(0).toUpperCase();

  const updateField = (field, value) => { setForm((f) => ({ ...f, [field]: value })); setProfileMessage(null); };
  const updatePassword = (field, value) => { setPasswords((p) => ({ ...p, [field]: value })); setPasswordMessage(null); };

  const saveProfile = async (e) => {
    e.preventDefault();
    if (editableFields.some((field) => !form[field].trim())) {
      setProfileMessage({ text: t('profile.missingFields'), error: true });
      return;
    }
    const changes = Object.fromEntries(
      editableFields.filter((field) => form[field] !== saved[field]).map((field) => [field, form[field].trim()]),
    );
    setSaving(true);
    try {
      const { profile, user } = await updateProfile(changes);
      setSaved(profile);
      setForm(profile);
      onUserUpdated(user);
      setProfileMessage({ text: t('profile.saved'), error: false });
    } catch (err) {
      setProfileMessage({ text: err.message, error: true });
    } finally {
      setSaving(false);
    }
  };

  const submitPassword = async (e) => {
    e.preventDefault();
    const { current, next, confirm } = passwords;
    if (!current || !next.trim() || !confirm) {
      setPasswordMessage({ text: t('profile.passwordMissing'), error: true });
      return;
    }
    if (next !== confirm) {
      setPasswordMessage({ text: t('profile.passwordMismatch'), error: true });
      return;
    }
    setChangingPassword(true);
    try {
      await changePassword(current, next);
      setPasswords(NO_PASSWORDS);
      setPasswordMessage({ text: t('profile.passwordChanged'), error: false });
    } catch (err) {
      setPasswordMessage({ text: err.message, error: true });
    } finally {
      setChangingPassword(false);
    }
  };

  const endOtherSessions = async () => {
    setSigningOut(true);
    setSessionsMessage(null);
    try {
      await signOutEverywhere();
      setSessionsMessage({ text: t('profile.signedOutEverywhere'), error: false });
    } catch (err) {
      setSessionsMessage({ text: err.message, error: true });
    } finally {
      setSigningOut(false);
    }
  };

  const textField = (field, label, autoComplete) => (
    <div key={field}>
      <label htmlFor={`profile-${field}`} style={LABEL_STYLE}>{label}</label>
      <input
        id={`profile-${field}`} value={form[field]} maxLength={150} autoComplete={autoComplete}
        onChange={(e) => updateField(field, e.target.value)} style={INPUT_STYLE}
      />
    </div>
  );

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both', maxWidth: '760px', display: 'flex', flexDirection: 'column', gap: '18px' }}>
      <div>{header}</div>

      <form onSubmit={saveProfile} style={CARD_STYLE}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '52px', height: '52px', borderRadius: '50%', background: '#DCECEF', flexShrink: 0, display: 'flex',
            alignItems: 'center', justifyContent: 'center', fontWeight: 700, color: '#1F374B', fontSize: '18px',
          }}>{initials}</div>
          <div style={{ minWidth: 0 }}>
            <h2 style={CARD_TITLE_STYLE}>{t('profile.personalTitle')}</h2>
            <div style={{ fontSize: '12.5px', color: '#939EA3', fontWeight: 600, marginTop: '2px' }}>{t(`roles.${saved.role}`)}</div>
          </div>
        </div>
        <div style={GRID_STYLE}>
          {textField('first_name', t('profile.firstNameLabel'), 'given-name')}
          {textField('last_name', t('profile.lastNameLabel'), 'family-name')}
        </div>
        <div>
          <label htmlFor="profile-email" style={LABEL_STYLE}>{t('profile.emailLabel')}</label>
          <input id="profile-email" value={saved.email} readOnly style={{ ...INPUT_STYLE, background: 'rgba(237,241,238,0.8)', color: '#556269' }} />
          <div style={{ fontSize: '11.5px', color: '#939EA3', marginTop: '5px' }}>{t('profile.emailHint')}</div>
        </div>
        {isStudent && (
          <div style={{ borderTop: '1px solid rgba(31,55,75,0.1)', paddingTop: '16px' }}>
            <h3 style={{ fontSize: '14.5px', fontWeight: 700, color: '#161F24', margin: '0 0 12px' }}>{t('profile.studyTitle')}</h3>
            <div style={GRID_STYLE}>
              {textField('faculty', t('survey.facultyLabel'))}
              {textField('course', t('survey.courseLabel'))}
              {textField('group', t('survey.groupLabel'))}
              {textField('specialization', t('survey.specializationLabel'))}
            </div>
          </div>
        )}
        <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '10px 14px' }}>
          <button type="submit" disabled={!dirty || saving} style={primaryButtonStyle(!dirty || saving)}>{t('profile.save')}</button>
          <StatusMessage message={profileMessage} />
        </div>
      </form>

      <form onSubmit={submitPassword} style={CARD_STYLE}>
        <div>
          <h2 style={CARD_TITLE_STYLE}>{t('profile.passwordTitle')}</h2>
          <p style={CARD_HINT_STYLE}>{t('profile.passwordSubtitle')}</p>
        </div>
        {/* Lets password managers tie the new password to this account. */}
        <input type="email" value={saved.email} autoComplete="username" readOnly hidden />
        <PasswordField
          id="profile-current-password" label={t('profile.currentPasswordLabel')} autoComplete="current-password"
          value={passwords.current} onChange={(v) => updatePassword('current', v)}
        />
        <div style={GRID_STYLE}>
          <PasswordField
            id="profile-new-password" label={t('profile.newPasswordLabel')} autoComplete="new-password"
            value={passwords.next} onChange={(v) => updatePassword('next', v)}
          />
          <PasswordField
            id="profile-confirm-password" label={t('profile.confirmPasswordLabel')} autoComplete="new-password"
            value={passwords.confirm} onChange={(v) => updatePassword('confirm', v)}
          />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '10px 14px' }}>
          <button type="submit" disabled={changingPassword} style={primaryButtonStyle(changingPassword)}>{t('profile.changePassword')}</button>
          <StatusMessage message={passwordMessage} />
        </div>
      </form>

      <section style={CARD_STYLE}>
        <div>
          <h2 style={CARD_TITLE_STYLE}>{t('profile.languageTitle')}</h2>
          <p style={CARD_HINT_STYLE}>{t('profile.languageSubtitle')}</p>
        </div>
        <div><LanguageSwitcher /></div>
      </section>

      <section style={CARD_STYLE}>
        <div>
          <h2 style={CARD_TITLE_STYLE}>{t('profile.sessionsTitle')}</h2>
          <p style={CARD_HINT_STYLE}>{t('profile.sessionsSubtitle')}</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '10px 14px' }}>
          <button type="button" onClick={endOtherSessions} disabled={signingOut} style={{
            padding: '9px 18px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.18)', background: 'transparent',
            color: '#2E5570', fontFamily: 'Manrope', fontWeight: 700, fontSize: '13px',
            cursor: signingOut ? 'default' : 'pointer', opacity: signingOut ? 0.6 : 1,
          }}>{t('profile.signOutEverywhere')}</button>
          <StatusMessage message={sessionsMessage} />
        </div>
      </section>
    </div>
  );
}
