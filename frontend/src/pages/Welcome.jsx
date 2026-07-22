import { useEffect, useState } from 'react';

import { getPublicStats } from '../api/public.js';
import logoIcon from '../assets/logo-icon.png';
import LanguageSwitcher from '../components/LanguageSwitcher.jsx';
import { useLanguage } from '../i18n/LanguageContext.jsx';

/**
 * Ported verbatim (markup + inline styles) from MindMetric AI.dc.html
 * lines 30-69 (`isWelcome`). `welcomeStats` was a hardcoded array in
 * `renderVals()`; here it comes from GET /api/public/stats/.
 */
export default function Welcome({ onGoAuth }) {
  const [welcomeStats, setWelcomeStats] = useState([]);
  const { t, language } = useLanguage();

  useEffect(() => {
    getPublicStats().then(setWelcomeStats).catch(() => setWelcomeStats([]));
  }, [language]);

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '28px 56px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <img src={logoIcon} alt="MindMetric AI" style={{ width: '34px', height: '34px', borderRadius: '9px' }} />
          <span style={{ fontFamily: 'Manrope', fontWeight: 800, fontSize: '17px', letterSpacing: '-0.01em', color: '#161F24' }}>
            MindMetric <span style={{ color: '#2E5570' }}>AI</span>
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <LanguageSwitcher />
          <button className="mm-btn" onClick={onGoAuth} style={{
            fontFamily: 'Manrope', fontWeight: 600, fontSize: '14px', color: '#1F374B', background: 'rgba(255,255,255,0.6)',
            border: '1px solid rgba(255,255,255,0.9)', padding: '10px 20px', borderRadius: '100px', cursor: 'pointer', backdropFilter: 'blur(12px)',
          }}>{t('common.signIn')}</button>
        </div>
      </header>

      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '40px 24px 80px', textAlign: 'center' }}>
        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '7px 16px', borderRadius: '100px',
          background: 'rgba(255,255,255,0.65)', border: '1px solid rgba(255,255,255,0.9)', backdropFilter: 'blur(10px)',
          fontSize: '12.5px', fontWeight: 600, color: '#2E5570', letterSpacing: '0.02em', marginBottom: '28px',
          animation: 'mm-fade-up 0.6s ease both',
        }}>
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#4F87AE' }} />
          {t('welcome.badge')}
        </div>
        <h1 style={{
          fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: 'clamp(40px,6vw,72px)', lineHeight: 1.05,
          color: '#161F24', maxWidth: '900px', margin: '0 0 22px', animation: 'mm-fade-up 0.7s ease 0.05s both',
        }}>
          {t('welcome.headline')}<br /><span style={{ color: '#2E5570', fontStyle: 'normal' }}>{t('welcome.headlineEm')}</span>
        </h1>
        <p style={{
          fontFamily: 'Manrope', fontSize: '18px', lineHeight: 1.6, color: '#556269', maxWidth: '560px',
          margin: '0 0 40px', animation: 'mm-fade-up 0.7s ease 0.1s both',
        }}>
          {t('welcome.lede')}
        </p>
        <div style={{ display: 'flex', gap: '14px', animation: 'mm-fade-up 0.7s ease 0.15s both' }}>
          <button className="mm-btn" onClick={onGoAuth} style={{
            fontFamily: 'Manrope', fontWeight: 700, fontSize: '15px', color: '#fff', background: '#2E5570',
            border: 'none', padding: '14px 30px', borderRadius: '100px', cursor: 'pointer', boxShadow: '0 10px 24px rgba(46,85,112,0.28)',
          }}>{t('welcome.getStarted')}</button>
          <button className="mm-btn" onClick={onGoAuth} style={{
            fontFamily: 'Manrope', fontWeight: 600, fontSize: '15px', color: '#1F374B', background: 'rgba(255,255,255,0.55)',
            border: '1px solid rgba(255,255,255,0.9)', padding: '14px 26px', borderRadius: '100px', cursor: 'pointer', backdropFilter: 'blur(10px)',
          }}>{t('welcome.viewSample')}</button>
        </div>

        <div style={{
          display: 'flex', gap: '20px', marginTop: '72px', flexWrap: 'wrap', justifyContent: 'center',
          maxWidth: '980px', animation: 'mm-fade-up 0.8s ease 0.2s both',
        }}>
          {welcomeStats.map((s, i) => (
            <div key={i} style={{
              width: '210px', padding: '22px 20px', borderRadius: '18px', background: 'rgba(255,255,255,0.55)',
              border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(16px)', textAlign: 'left',
              boxShadow: '0 8px 30px rgba(31,55,75,0.06)',
            }}>
              <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '34px', color: '#1F374B' }}>{s.value}</div>
              <div style={{ fontSize: '12.5px', color: '#556269', marginTop: '4px', fontWeight: 600 }}>{s.label}</div>
            </div>
          ))}
        </div>
      </main>

      <footer style={{ padding: '22px 56px', fontSize: '12.5px', color: '#939EA3' }}>
        <span>{t('welcome.footer')}</span>
      </footer>
    </div>
  );
}
