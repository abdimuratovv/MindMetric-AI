import { useState } from 'react';

import { login } from '../api/auth.js';
import logoIcon from '../assets/logo-icon.png';
import { useLanguage } from '../i18n/LanguageContext.jsx';

const ROLES = ['student', 'teacher', 'admin'];

/** Ported verbatim from MindMetric AI.dc.html lines 72-109 (`isAuth`). */
export default function Auth({ onLoginSuccess, onGoWelcome }) {
  const [authTab, setAuthTab] = useState('student');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [emailFocused, setEmailFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);
  const { t } = useLanguage();

  const doLogin = async () => {
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

  const activeRoleLabel = t(`roles.${authTab}`);

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
      <div style={{
        width: '420px', padding: '40px 36px', borderRadius: '24px', background: 'rgba(255,255,255,0.6)',
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
        <h2 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '28px', color: '#161F24', margin: '0 0 6px' }}>{t('auth.welcomeBack')}</h2>
        <p style={{ fontSize: '13.5px', color: '#556269', margin: '0 0 22px' }}>{t('auth.subtitle')}</p>

        <div style={{ display: 'flex', gap: '6px', padding: '4px', borderRadius: '12px', background: 'rgba(241,238,231,0.7)', marginBottom: '20px' }}>
          {ROLES.map((r) => (
            <button
              key={r}
              className="mm-btn"
              disabled={isLoggingIn}
              onClick={() => { setAuthTab(r); setLoginError(''); }}
              style={{
                flex: 1, padding: '9px 0', borderRadius: '9px', border: 'none', cursor: 'pointer', fontFamily: 'Manrope',
                fontWeight: 700, fontSize: '12.5px', background: authTab === r ? '#2E5570' : 'transparent',
                color: authTab === r ? '#fff' : '#556269',
              }}>{t(`roles.${r}`)}</button>
          ))}
        </div>

        <label style={{ display: 'block', fontSize: '12.5px', fontWeight: 600, color: '#1F374B', marginBottom: '6px' }}>{t('auth.emailLabel')}</label>
        <input
          value={email}
          onChange={(e) => { setEmail(e.target.value); setLoginError(''); }}
          onFocus={() => setEmailFocused(true)}
          onBlur={() => setEmailFocused(false)}
          placeholder={t('auth.emailPlaceholder')}
          style={{
            width: '100%', padding: '12px 14px', borderRadius: '12px',
            border: `1px solid ${emailFocused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
            boxShadow: emailFocused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
            transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
            background: 'rgba(255,255,255,0.7)', fontFamily: 'Manrope', fontSize: '14px', color: '#161F24',
            marginBottom: '16px', outline: 'none',
          }}
        />

        <label style={{ display: 'block', fontSize: '12.5px', fontWeight: 600, color: '#1F374B', marginBottom: '6px' }}>{t('auth.passwordLabel')}</label>
        <input
          type="password"
          value={password}
          onChange={(e) => { setPassword(e.target.value); setLoginError(''); }}
          onFocus={() => setPasswordFocused(true)}
          onBlur={() => setPasswordFocused(false)}
          placeholder="••••••••"
          style={{
            width: '100%', padding: '12px 14px', borderRadius: '12px',
            border: `1px solid ${passwordFocused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
            boxShadow: passwordFocused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
            transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
            background: 'rgba(255,255,255,0.7)', fontFamily: 'Manrope', fontSize: '14px', color: '#161F24',
            marginBottom: '8px', outline: 'none',
          }}
        />

        {loginError && (
          <div style={{
            display: 'flex', gap: '8px', alignItems: 'center', padding: '10px 12px', borderRadius: '10px',
            background: '#F6E0DC', color: '#BD5B4C', fontSize: '12.5px', fontWeight: 600, margin: '8px 0',
          }}>
            <span>⚠</span><span>{loginError}</span>
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', margin: '6px 0 20px' }}>
          <a href="#" style={{ fontSize: '12px', fontWeight: 600, textDecoration: 'none' }}>{t('auth.forgotPassword')}</a>
        </div>

        <button
          className="mm-btn"
          disabled={isLoggingIn}
          onClick={doLogin}
          style={{
            width: '100%', padding: '13px 0', borderRadius: '100px', border: 'none', cursor: 'pointer',
            background: '#2E5570', color: '#fff', fontFamily: 'Manrope', fontWeight: 700, fontSize: '14.5px',
            boxShadow: '0 10px 24px rgba(46,85,112,0.25)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
          }}>
          {isLoggingIn && <span className="mm-spinner" />}
          {t('auth.signInAs')(activeRoleLabel)}
        </button>

        <p style={{ textAlign: 'center', fontSize: '11.5px', color: '#939EA3', margin: '16px 0 0' }}>
          {t('auth.demoNotice')}
        </p>
      </div>
    </div>
  );
}
