import { useEffect, useState } from 'react';

import { getResultsAnalytics } from '../../api/results.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

/** Ported verbatim from MindMetric AI.dc.html lines 236-273 (`isAnalytics`). */
export default function Analytics({ goTo }) {
  const [indicatorsDetail, setIndicatorsDetail] = useState(null);
  const { t, language } = useLanguage();

  useEffect(() => { getResultsAnalytics().then(setIndicatorsDetail); }, [language]);

  if (!indicatorsDetail) return null;

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <button className="mm-btn" onClick={() => goTo('results')} style={{ border: 'none', background: 'none', color: '#556269', fontWeight: 600, fontSize: '13px', cursor: 'pointer', marginBottom: '14px', padding: 0 }}>
        {t('analytics.back')}
      </button>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>
        {t('analytics.title')}
      </h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 24px' }}>
        {t('analytics.subtitle')}
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {indicatorsDetail.map((d) => (
          <div key={d.key} style={{
            padding: '24px 28px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)',
            backdropFilter: 'blur(14px)', boxShadow: '0 8px 24px rgba(31,55,75,0.05)', opacity: d.completed ? 1 : 0.75,
          }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '22px', alignItems: 'center' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
                  <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#161F24', margin: 0 }}>{d.label}</h3>
                  <span style={{ fontSize: '11px', fontWeight: 700, padding: '3px 10px', borderRadius: '100px', background: d.tierBg, color: d.tierColor }}>{d.tier}</span>
                </div>
                <p style={{ fontSize: '12.5px', color: '#556269', lineHeight: 1.55, margin: '0 0 10px', maxWidth: '420px' }}>{d.explanation}</p>
                <div style={{ height: '7px', borderRadius: '100px', background: '#EAF2F5', overflow: 'hidden', maxWidth: '320px' }}>
                  <div style={{ height: '100%', width: d.pct, background: d.color, borderRadius: '100px' }} />
                </div>
              </div>
              {d.completed ? (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '18px', justifyContent: 'center' }}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '36px', color: '#1F374B' }}>{d.score}</div>
                    <div style={{ fontSize: '11.5px', color: '#939EA3', fontWeight: 600 }}>{t('analytics.yourScore')}</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '36px', color: '#939EA3' }}>{d.cohortAvg}</div>
                    <div style={{ fontSize: '11.5px', color: '#939EA3', fontWeight: 600 }}>{t('analytics.cohortAverage')(d.percentile)}</div>
                  </div>
                </div>
              ) : (
                <div style={{ textAlign: 'center' }}>
                  <button className="mm-btn" onClick={() => goTo('selection')} style={{ border: 'none', background: 'none', color: '#2E5570', fontWeight: 700, fontSize: '13px', cursor: 'pointer', padding: 0 }}>
                    {t('analytics.takeTest')}
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '20px', padding: '18px 24px', borderRadius: '16px', background: 'rgba(241,238,231,0.5)', border: '1px solid rgba(255,255,255,0.7)', fontSize: '12px', color: '#556269', lineHeight: 1.6 }}>
        {t('analytics.methodology')}
      </div>
    </div>
  );
}
