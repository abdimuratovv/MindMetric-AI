import { useState } from 'react';

import { login, register } from '../api/auth.js';
import logoIcon from '../assets/logo-icon.png';
import { useLanguage } from '../i18n/LanguageContext.jsx';

// Teacher removed as a role: a teacher could only ever view student results
// in their own section, nothing else — that's now folded into Admin.
const ROLES = ['student', 'admin'];

/** Open/closed eye icon toggling a password field between masked and plain text. */
function PasswordVisibilityToggle({ visible, onToggle, label }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label={label}
      aria-pressed={visible}
      style={{
        position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)',
        width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center',
        border: 'none', background: 'transparent', cursor: 'pointer', padding: 0, color: '#7C8A91',
      }}
    >
      {visible ? (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M17.94 17.94A10.94 10.94 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A10.94 10.94 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
          <line x1="1" y1="1" x2="23" y2="23" />
        </svg>
      ) : (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8Z" />
          <circle cx="12" cy="12" r="3" />
        </svg>
      )}
    </button>
  );
}

/** Shared label+input look for both the login and register forms below. */
function AuthField({ label, type = 'text', value, onChange, placeholder, focused, onFocus, onBlur, marginBottom = '16px', showLabel, hideLabel }) {
  const isPassword = type === 'password';
  const [visible, setVisible] = useState(false);

  return (
    <>
      <label style={{ display: 'block', fontSize: '12.5px', fontWeight: 600, color: '#1F374B', marginBottom: '6px' }}>{label}</label>
      <div style={{ position: 'relative', marginBottom }}>
        <input
          type={isPassword && visible ? 'text' : type}
          value={value}
          onChange={onChange}
          onFocus={onFocus}
          onBlur={onBlur}
          placeholder={placeholder}
          style={{
            width: '100%', padding: isPassword ? '12px 42px 12px 14px' : '12px 14px', borderRadius: '12px',
            border: `1px solid ${focused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
            boxShadow: focused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
            transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
            background: 'rgba(255,255,255,0.7)', fontFamily: 'Manrope', fontSize: '14px', color: '#161F24',
            outline: 'none', boxSizing: 'border-box',
          }}
        />
        {isPassword && (
          <PasswordVisibilityToggle visible={visible} onToggle={() => setVisible((v) => !v)} label={visible ? hideLabel : showLabel} />
        )}
      </div>
    </>
  );
}

/** Ported verbatim from MindMetric AI.dc.html lines 72-109 (`isAuth`), later extended with a register mode. */
export default function Auth({ onLoginSuccess, onGoWelcome }) {
  const [authMode, setAuthMode] = useState('login'); // 'login' | 'register'
  const [authTab, setAuthTab] = useState('student');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [registerError, setRegisterError] = useState('');
  const [registerSuccess, setRegisterSuccess] = useState(false);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [emailFocused, setEmailFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);
  const [firstNameFocused, setFirstNameFocused] = useState(false);
  const [lastNameFocused, setLastNameFocused] = useState(false);
  const [confirmPasswordFocused, setConfirmPasswordFocused] = useState(false);
  const { t } = useLanguage();

  const doLogin = async () => {
    setRegisterSuccess(false);
    if (!email.trim() || !password.trim()) {
      setLoginError(t('auth.missingFields'));
      return;
    }
    setIsLoggingIn(true);
    try {
      const user = await login(email, password, authTab);
      onLoginSuccess(user);
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setIsLoggingIn(false);
    }
  };

  const doRegister = async () => {
    if (!firstName.trim() || !lastName.trim() || !email.trim() || !password.trim() || !confirmPassword.trim()) {
      setRegisterError(t('register.missingFields'));
      return;
    }
    if (password !== confirmPassword) {
      setRegisterError(t('register.passwordMismatch'));
      return;
    }
    setIsRegistering(true);
    try {
      await register(firstName, lastName, email, password);
      setPassword('');
      setConfirmPassword('');
      setFirstName('');
      setLastName('');
      setAuthMode('login');
      setRegisterSuccess(true);
    } catch (err) {
      setRegisterError(err.message);
    } finally {
      setIsRegistering(false);
    }
  };

  const switchToRegister = () => { setAuthMode('register'); setLoginError(''); setRegisterSuccess(false); };
  const switchToLogin = () => { setAuthMode('login'); setRegisterError(''); };

  const clearEmailPasswordErrors = () => { setLoginError(''); setRegisterError(''); };

  const activeRoleLabel = t(`roles.${authTab}`);
  const isBusy = isLoggingIn || isRegistering;

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
      <div style={{
        width: '100%', maxWidth: '420px', padding: 'clamp(26px,7vw,40px) clamp(20px,6vw,36px)', borderRadius: '24px', background: 'rgba(255,255,255,0.6)',
        border: '1px solid rgba(255,255,255,0.9)', backdropFilter: 'blur(20px)', boxShadow: '0 20px 60px rgba(31,55,75,0.1)',
        animation: 'mm-fade-up 0.5s ease both',
      }}>
        <div
          onClick={onGoWelcome}
          style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '26px', cursor: 'pointer', width: 'fit-content' }}
        >
          <img src={logoIcon} alt="MindMetric AI" style={{ width: '30px', height: '30px', borderRadius: '8px' }} />
          <span style={{ fontWeight: 800, fontSize: '16px', color: '#161F24' }}>{t('common.brand')}</span>
        </div>
        <h2 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '28px', color: '#161F24', margin: '0 0 6px' }}>
          {authMode === 'login' ? t('auth.welcomeBack') : t('register.title')}
        </h2>
        <p style={{ fontSize: '13.5px', color: '#556269', margin: '0 0 22px' }}>
          {authMode === 'login' ? t('auth.subtitle') : t('register.subtitle')}
        </p>

        {authMode === 'login' && (
          <div style={{ display: 'flex', gap: '6px', padding: '4px', borderRadius: '12px', background: 'rgba(241,238,231,0.7)', marginBottom: '20px' }}>
            {ROLES.map((r) => (
              <button
                key={r}
                className="mm-btn"
                disabled={isBusy}
                onClick={() => { setAuthTab(r); setLoginError(''); }}
                style={{
                  flex: 1, padding: '9px 0', borderRadius: '9px', border: 'none', cursor: 'pointer', fontFamily: 'Manrope',
                  fontWeight: 700, fontSize: '12.5px', background: authTab === r ? '#2E5570' : 'transparent',
                  color: authTab === r ? '#fff' : '#556269',
                }}>{t(`roles.${r}`)}</button>
            ))}
          </div>
        )}

        {authMode === 'register' && (
          <>
            <AuthField
              label={t('register.firstNameLabel')}
              value={firstName}
              onChange={(e) => { setFirstName(e.target.value); setRegisterError(''); }}
              onFocus={() => setFirstNameFocused(true)}
              onBlur={() => setFirstNameFocused(false)}
              placeholder={t('register.firstNamePlaceholder')}
              focused={firstNameFocused}
            />
            <AuthField
              label={t('register.lastNameLabel')}
              value={lastName}
              onChange={(e) => { setLastName(e.target.value); setRegisterError(''); }}
              onFocus={() => setLastNameFocused(true)}
              onBlur={() => setLastNameFocused(false)}
              placeholder={t('register.lastNamePlaceholder')}
              focused={lastNameFocused}
            />
          </>
        )}

        <AuthField
          label={t('auth.emailLabel')}
          value={email}
          onChange={(e) => { setEmail(e.target.value); clearEmailPasswordErrors(); }}
          onFocus={() => setEmailFocused(true)}
          onBlur={() => setEmailFocused(false)}
          placeholder={t('auth.emailPlaceholder')}
          focused={emailFocused}
          marginBottom={authMode === 'register' ? '4px' : '16px'}
        />
        {authMode === 'register' && (
          <p style={{ fontSize: '11px', color: '#939EA3', margin: '0 0 16px' }}>{t('register.emailHint')}</p>
        )}

        <AuthField
          label={t('auth.passwordLabel')}
          type="password"
          value={password}
          onChange={(e) => { setPassword(e.target.value); clearEmailPasswordErrors(); }}
          onFocus={() => setPasswordFocused(true)}
          onBlur={() => setPasswordFocused(false)}
          placeholder="••••••••"
          focused={passwordFocused}
          marginBottom={authMode === 'register' ? '16px' : '8px'}
          showLabel={t('auth.showPassword')}
          hideLabel={t('auth.hidePassword')}
        />

        {authMode === 'register' && (
          <AuthField
            label={t('register.confirmPasswordLabel')}
            type="password"
            value={confirmPassword}
            onChange={(e) => { setConfirmPassword(e.target.value); setRegisterError(''); }}
            onFocus={() => setConfirmPasswordFocused(true)}
            onBlur={() => setConfirmPasswordFocused(false)}
            placeholder="••••••••"
            focused={confirmPasswordFocused}
            marginBottom="8px"
            showLabel={t('auth.showPassword')}
            hideLabel={t('auth.hidePassword')}
          />
        )}

        {authMode === 'login' && loginError && (
          <div style={{
            display: 'flex', gap: '8px', alignItems: 'center', padding: '10px 12px', borderRadius: '10px',
            background: '#F6E0DC', color: '#BD5B4C', fontSize: '12.5px', fontWeight: 600, margin: '8px 0',
          }}>
            <span>⚠</span><span>{loginError}</span>
          </div>
        )}
        {authMode === 'register' && registerError && (
          <div style={{
            display: 'flex', gap: '8px', alignItems: 'center', padding: '10px 12px', borderRadius: '10px',
            background: '#F6E0DC', color: '#BD5B4C', fontSize: '12.5px', fontWeight: 600, margin: '8px 0',
          }}>
            <span>⚠</span><span>{registerError}</span>
          </div>
        )}

        {authMode === 'login' && (
          <div style={{ display: 'flex', justifyContent: 'flex-end', margin: '6px 0 20px' }}>
            <a href="#" style={{ fontSize: '12px', fontWeight: 600, textDecoration: 'none' }}>{t('auth.forgotPassword')}</a>
          </div>
        )}

        <button
          className="mm-btn"
          disabled={isBusy}
          onClick={authMode === 'login' ? doLogin : doRegister}
          style={{
            width: '100%', padding: '13px 0', borderRadius: '100px', border: 'none', cursor: 'pointer',
            background: '#2E5570', color: '#fff', fontFamily: 'Manrope', fontWeight: 700, fontSize: '14.5px',
            boxShadow: '0 10px 24px rgba(46,85,112,0.25)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
            marginTop: authMode === 'register' ? '20px' : 0,
          }}>
          {isBusy && <span className="mm-spinner" />}
          {authMode === 'login' ? t('auth.signInAs')(activeRoleLabel) : t('register.submitButton')}
        </button>

        {authMode === 'login' && registerSuccess && (
          <div style={{
            display: 'flex', gap: '8px', alignItems: 'center', padding: '10px 12px', borderRadius: '10px',
            background: '#DCEFE2', color: '#1F4B39', fontSize: '12.5px', fontWeight: 600, margin: '16px 0 0',
          }}>
            <span>✓</span><span>{t('register.successMessage')}</span>
          </div>
        )}

        <p style={{ textAlign: 'center', fontSize: '12.5px', color: '#556269', margin: '16px 0 0' }}>
          {authMode === 'login' ? (
            <>{t('auth.noAccount')} <a href="#" onClick={(e) => { e.preventDefault(); switchToRegister(); }}>{t('auth.createAccount')}</a></>
          ) : (
            <>{t('register.haveAccount')} <a href="#" onClick={(e) => { e.preventDefault(); switchToLogin(); }}>{t('register.signIn')}</a></>
          )}
        </p>
      </div>
    </div>
  );
}
