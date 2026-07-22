import { LANGUAGES, useLanguage } from '../i18n/LanguageContext.jsx';

const LABELS = { ru: 'RU', uz: 'UZ' };

/**
 * Two-way RU/UZ segmented toggle, styled to match the mockup's glass/pill
 * language (same track shape as Auth.jsx's role tabs). Persists the choice
 * via useLanguage()'s localStorage-backed setLanguage — every subsequent
 * API call picks it up through the X-Language header (api/client.js).
 */
export default function LanguageSwitcher({ compact = false }) {
  const { language, setLanguage } = useLanguage();

  return (
    <div
      role="group"
      aria-label="Til / Язык"
      style={{
        display: 'inline-flex', gap: '2px', padding: '3px', borderRadius: '100px',
        background: compact ? 'rgba(241,238,231,0.7)' : 'rgba(255,255,255,0.55)',
        border: '1px solid rgba(255,255,255,0.9)', backdropFilter: 'blur(10px)',
      }}
    >
      {LANGUAGES.map((code) => {
        const active = language === code;
        return (
          <button
            key={code}
            className="mm-btn"
            onClick={() => setLanguage(code)}
            aria-pressed={active}
            style={{
              padding: compact ? '5px 12px' : '7px 14px',
              borderRadius: '100px',
              border: 'none',
              cursor: 'pointer',
              fontFamily: 'Manrope',
              fontWeight: 700,
              fontSize: compact ? '11px' : '12px',
              letterSpacing: '0.02em',
              background: active ? '#2E5570' : 'transparent',
              color: active ? '#fff' : '#556269',
              transition: 'background 0.15s, color 0.15s',
            }}
          >
            {LABELS[code]}
          </button>
        );
      })}
    </div>
  );
}
