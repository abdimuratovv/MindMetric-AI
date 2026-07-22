import { useEffect, useState } from 'react';

import { getStatus, startAssessment } from '../../api/assessments.js';
import { ASSESSMENT_ICONS, ASSESSMENT_PATTERN, ASSESSMENT_TYPES } from '../../constants/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

/** Ported (extended to 10 indicator-specific cards) from MindMetric AI.dc.html lines 140-169 (`isSelection`). */
export default function StudentSelection({ user, goTo }) {
  const [statusByType, setStatusByType] = useState(null);
  const [startingKey, setStartingKey] = useState(null);
  const { t } = useLanguage();

  const refresh = () => getStatus().then(setStatusByType);
  useEffect(() => { refresh(); }, []);

  if (!statusByType) return null;

  const anyCompleted = statusByType.any_completed;
  const studentFirstName = (user?.name || '').split(' ')[0];

  const assessments = ASSESSMENT_TYPES.map((key) => {
    const attemptStatus = statusByType[key]?.status;
    const done = attemptStatus === 'completed';
    const inProgress = attemptStatus === 'in_progress';
    const meta = t(`assessmentsMeta.${key}`);
    const icon = ASSESSMENT_ICONS[key];
    return {
      key, ...icon,
      title: meta.title, desc: meta.desc, duration: meta.duration,
      statusLabel: done
        ? t('selection.statusCompleted')
        : inProgress ? t('selection.statusInProgress') : t('selection.statusAvailable'),
      statusBg: done ? '#DCEFE2' : inProgress ? '#F5E9D3' : '#EAF5EE',
      statusColor: done ? '#1F4B39' : inProgress ? '#8A6D1F' : '#55695F',
      btnLabel: done ? t('selection.btnRetake') : inProgress ? t('selection.btnContinue') : t('selection.btnStart'),
      btnBg: done ? 'rgba(255,255,255,0.6)' : '#2E5570',
      btnColor: done ? '#1F374B' : '#fff',
      onStart: async () => {
        setStartingKey(key);
        try {
          await startAssessment(key, ASSESSMENT_PATTERN[key]);
          goTo(key);
        } finally {
          setStartingKey(null);
        }
      },
    };
  });

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '32px', color: '#161F24', margin: '0 0 6px' }}>
            {t('selection.greeting')(studentFirstName)}
          </h1>
          <p style={{ fontSize: '14px', color: '#556269', margin: 0 }}>{t('selection.subtitle')}</p>
        </div>
        <button
          className="mm-btn"
          onClick={() => anyCompleted && goTo('results')}
          disabled={!anyCompleted}
          style={{
            padding: '12px 24px', borderRadius: '100px', border: 'none', cursor: 'pointer', fontWeight: 700, fontSize: '13.5px',
            background: anyCompleted ? '#2E5570' : '#EAF2F5', color: anyCompleted ? '#fff' : '#939EA3',
            opacity: anyCompleted ? 1 : 0.7,
          }}
        >{t('selection.viewResults')}</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(280px,1fr))', gap: '20px' }}>
        {assessments.map((a) => (
          <div key={a.key} style={{
            padding: '26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)',
            backdropFilter: 'blur(16px)', boxShadow: '0 10px 30px rgba(31,55,75,0.06)', display: 'flex', flexDirection: 'column', gap: '14px',
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ width: '42px', height: '42px', borderRadius: '12px', background: a.iconBg, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={a.iconColor} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d={a.iconPath}></path>
                </svg>
              </div>
              <span style={{ fontSize: '11px', fontWeight: 700, padding: '5px 11px', borderRadius: '100px', background: a.statusBg, color: a.statusColor }}>
                {a.statusLabel}
              </span>
            </div>
            <div>
              <h3 style={{ fontSize: '17px', fontWeight: 700, color: '#161F24', margin: '0 0 6px' }}>{a.title}</h3>
              <p style={{ fontSize: '13px', color: '#556269', margin: 0, lineHeight: 1.5 }}>{a.desc}</p>
            </div>
            <div style={{ fontSize: '12px', color: '#939EA3', fontWeight: 600 }}>{a.duration}</div>
            <button
              className="mm-btn"
              disabled={startingKey === a.key}
              onClick={a.onStart}
              style={{
                marginTop: '4px', padding: '11px 0', borderRadius: '100px', border: 'none', cursor: 'pointer',
                fontWeight: 700, fontSize: '13.5px', background: a.btnBg, color: a.btnColor,
                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
              }}>
              {startingKey === a.key && <span className={`mm-spinner${a.btnColor === '#fff' ? '' : ' mm-spinner-dark'}`} />}
              {a.btnLabel}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
