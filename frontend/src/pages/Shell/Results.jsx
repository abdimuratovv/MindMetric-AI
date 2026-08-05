import { useEffect, useState } from 'react';

import { getResultsMistakes, getResultsSummary } from '../../api/results.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import { polar } from '../../theme/tokens.js';

// Formatted by hand rather than via toLocaleDateString('uz-Latn-UZ', …): browsers'
// bundled ICU data has no Uzbek month names and silently falls back to "M07"-style
// placeholders. Russian has full Intl support, but a shared formatter keeps both
// languages consistent and doesn't depend on the runtime's locale data at all.
const MONTH_ABBR = {
  ru: ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'],
  uz: ['yan', 'fev', 'mar', 'apr', 'may', 'iyun', 'iyul', 'avg', 'sen', 'okt', 'noy', 'dek'],
};

function formatDate(date, lang) {
  return `${date.getDate()} ${MONTH_ABBR[lang][date.getMonth()]} ${date.getFullYear()}`;
}

/** Ported verbatim from MindMetric AI.dc.html lines 171-234 (`isResults`). */
export default function Results({ user, goTo }) {
  const [data, setData] = useState(null);
  const [mistakes, setMistakes] = useState(null);
  const [hoverIdx, setHoverIdx] = useState(null);
  const { t, language } = useLanguage();

  useEffect(() => { getResultsSummary().then(setData); }, [language]);
  useEffect(() => { getResultsMistakes().then((res) => setMistakes(res.mistakes)); }, [language]);

  if (!data) return null;

  const {
    overallScore, band, bandBg, bandColor, bandExplanation, indicators, overallExplanation,
    programmingAptitudeScore, fieldRecommendations,
  } = data;

  // Radar geometry — ported from renderVals() lines 882-892 (pure presentation, computed client-side).
  const cx = 110, cy = 110, maxR = 84;
  const n = indicators.length;
  const radarAxes = indicators.map((_, idx) => polar((idx * 360) / n, maxR, cx, cy));
  const radarRings = [0.25, 0.5, 0.75, 1].map((f) => ({
    points: indicators.map((_, idx) => { const p = polar((idx * 360) / n, maxR * f, cx, cy); return `${p.x},${p.y}`; }).join(' '),
  }));
  const radarDots = indicators.map((ind, idx) => polar((idx * 360) / n, (maxR * (ind.score ?? 0)) / 100, cx, cy));
  const radarPoints = radarDots.map((p) => `${p.x},${p.y}`).join(' ');
  const radarLabels = indicators.map((_, idx) => polar((idx * 360) / n, maxR + 17, cx, cy));

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 4px' }}>
        {t('results.title')}
      </h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 26px' }}>
        {t('results.assessedOn')(user?.name, user?.program, formatDate(new Date(), language))}
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '22px', marginBottom: '22px' }}>
        <div style={{
          padding: '30px', borderRadius: '22px', background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)',
          backdropFilter: 'blur(16px)', boxShadow: '0 10px 30px rgba(31,55,75,0.06)', display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center', textAlign: 'center', gap: '10px',
        }}>
          <span style={{ fontSize: '12px', fontWeight: 700, letterSpacing: '0.04em', color: '#939EA3' }}>{t('results.overallScoreLabel')}</span>
          <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '76px', lineHeight: 1, color: '#1F374B' }}>{overallScore}</div>
          <span style={{ padding: '7px 18px', borderRadius: '100px', fontWeight: 700, fontSize: '13px', background: bandBg, color: bandColor }}>{band}</span>
          <p style={{ fontSize: '12.5px', color: '#556269', lineHeight: 1.55, margin: '8px 0 0', maxWidth: '280px' }}>{bandExplanation}</p>
          {programmingAptitudeScore != null && (
            <div style={{ marginTop: '10px', paddingTop: '12px', borderTop: '1px solid rgba(46,85,112,0.12)', width: '100%' }}>
              <span style={{ fontSize: '10.5px', fontWeight: 700, letterSpacing: '0.04em', color: '#939EA3' }}>{t('results.programmingAptitudeLabel')}</span>
              <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '28px', color: '#2E5570' }}>{programmingAptitudeScore}</div>
            </div>
          )}
        </div>

        <div style={{
          padding: '26px 30px', borderRadius: '22px', background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)',
          backdropFilter: 'blur(16px)', boxShadow: '0 10px 30px rgba(31,55,75,0.06)', display: 'flex', alignItems: 'center',
          flexWrap: 'wrap', justifyContent: 'center', gap: '24px',
        }}>
          <div style={{ position: 'relative', width: '220px', height: '220px', flexShrink: 0 }}>
            <svg width="220" height="220" viewBox="0 0 220 220" style={{ overflow: 'visible' }}>
              {radarRings.map((ring, i) => <polygon key={i} points={ring.points} fill="none" stroke="#DCECEF" strokeWidth="1" />)}
              {radarAxes.map((ax, i) => <line key={i} x1="110" y1="110" x2={ax.x} y2={ax.y} stroke="#E7EEF0" strokeWidth="1" />)}
              <polygon points={radarPoints} fill="rgba(46,85,112,0.16)" stroke="#2E5570" strokeWidth="2.2" />
              {radarDots.map((d, i) => (
                <g key={i} onMouseEnter={() => setHoverIdx(i)} onMouseLeave={() => setHoverIdx(null)} style={{ cursor: 'pointer' }}>
                  <circle cx={d.x} cy={d.y} r="10" fill="transparent" />
                  {indicators[i].completed ? (
                    <circle
                      cx={d.x} cy={d.y} r={hoverIdx === i ? '5.5' : '3.5'} fill="#2E5570" stroke="#fff"
                      strokeWidth={hoverIdx === i ? '1.5' : '0'} style={{ transition: 'r 0.15s ease' }}
                    />
                  ) : (
                    <circle
                      cx={d.x} cy={d.y} r={hoverIdx === i ? '5' : '3.5'} fill="#fff" stroke="#C3CACC"
                      strokeWidth="1.5" strokeDasharray="2,2" style={{ transition: 'r 0.15s ease' }}
                    />
                  )}
                </g>
              ))}
              {radarLabels.map((p, i) => {
                const dx = p.x - cx, dy = p.y - cy;
                const textAnchor = Math.abs(dx) < 2 ? 'middle' : dx > 0 ? 'start' : 'end';
                const dyOffset = Math.abs(dy) < 2 ? '0.35em' : dy > 0 ? '0.9em' : '-0.35em';
                return (
                  <text
                    key={i} x={p.x} y={p.y} dy={dyOffset} textAnchor={textAnchor}
                    onMouseEnter={() => setHoverIdx(i)} onMouseLeave={() => setHoverIdx(null)}
                    style={{ fontSize: '10.5px', fontWeight: 700, fill: hoverIdx === i ? '#2E5570' : '#B7C1C4', cursor: 'pointer', userSelect: 'none' }}
                  >
                    {i + 1}
                  </text>
                );
              })}
            </svg>
            {hoverIdx !== null && (
              <div style={{
                position: 'absolute', left: `${radarDots[hoverIdx].x}px`, top: `${radarDots[hoverIdx].y}px`,
                transform: 'translate(-50%, -130%)', background: '#161F24', color: '#fff', fontSize: '11.5px',
                fontWeight: 600, padding: '6px 10px', borderRadius: '8px', whiteSpace: 'nowrap', pointerEvents: 'none',
                boxShadow: '0 8px 20px rgba(22,31,36,0.28)', zIndex: 5,
              }}>
                {indicators[hoverIdx].label}: <strong>{indicators[hoverIdx].completed ? indicators[hoverIdx].score : indicators[hoverIdx].tier}</strong>
              </div>
            )}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1, minWidth: '220px' }}>
            {indicators.map((ind, idx) => (
              <div
                key={ind.key}
                onMouseEnter={() => setHoverIdx(idx)}
                onMouseLeave={() => setHoverIdx(null)}
                style={{
                  display: 'flex', alignItems: 'center', gap: '8px', padding: '3px 6px', borderRadius: '8px', cursor: 'pointer',
                  background: hoverIdx === idx ? 'rgba(46,85,112,0.08)' : 'transparent', transition: 'background 0.15s ease',
                  opacity: ind.completed ? 1 : 0.7,
                }}
              >
                <span style={{
                  width: '16px', height: '16px', borderRadius: '50%', background: ind.completed ? '#2E5570' : '#C3CACC', color: '#fff',
                  fontSize: '9px', fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
                }}>{idx + 1}</span>
                <span style={{ fontSize: '12px', color: ind.completed ? '#3B444A' : '#939EA3', fontStyle: ind.completed ? 'normal' : 'italic', flex: 1 }}>{ind.label}</span>
                <span style={{ fontSize: '12px', fontWeight: 700, color: ind.completed ? '#161F24' : '#939EA3' }}>{ind.completed ? ind.score : ind.tier}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{
        padding: '26px 30px', borderRadius: '22px', background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)',
        backdropFilter: 'blur(16px)', boxShadow: '0 10px 30px rgba(31,55,75,0.06)', marginBottom: '22px',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#161F24', margin: 0 }}>{t('results.indicatorBreakdown')}</h3>
          <button className="mm-btn" onClick={() => goTo('analytics')} style={{ border: 'none', background: 'none', color: '#2E5570', fontWeight: 700, fontSize: '13px', cursor: 'pointer' }}>
            {t('results.viewDetailedAnalytics')}
          </button>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {indicators.map((ind) => (
            <div key={ind.key} style={{ opacity: ind.completed ? 1 : 0.7 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '6px' }}>
                <span style={{ fontWeight: 600, color: '#161F24' }}>{ind.label}</span>
                <span style={{ fontWeight: 700, color: ind.color }}>{ind.completed ? `${ind.score} · ${ind.tier}` : ind.tier}</span>
              </div>
              <div style={{ height: '8px', borderRadius: '100px', background: '#EAF2F5', overflow: 'hidden' }}>
                <div style={{ height: '100%', width: ind.pct, background: ind.color, borderRadius: '100px' }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div style={{
        padding: '26px 30px', borderRadius: '22px', background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)',
        backdropFilter: 'blur(16px)', boxShadow: '0 10px 30px rgba(31,55,75,0.06)', marginBottom: '22px',
      }}>
        <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#161F24', margin: '0 0 4px' }}>{t('results.recommendedFieldTitle')}</h3>
        {fieldRecommendations?.available ? (
          <>
            <p style={{ fontSize: '12.5px', color: '#556269', margin: '0 0 16px' }}>{t('results.recommendedFieldSubtitle')}</p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {fieldRecommendations.fields.map((field) => (
                <div key={field.key}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 600, color: '#161F24' }}>{field.label}</span>
                    <span style={{ fontWeight: 700, color: '#2E5570' }}>{field.score}{t('results.fitScoreSuffix')}</span>
                  </div>
                  <div style={{ height: '8px', borderRadius: '100px', background: '#EAF2F5', overflow: 'hidden', marginBottom: '6px' }}>
                    <div style={{ height: '100%', width: `${field.score}%`, background: '#2E5570', borderRadius: '100px' }} />
                  </div>
                  <p style={{ fontSize: '12px', lineHeight: 1.55, color: '#556269', margin: 0 }}>{field.explanation}</p>
                </div>
              ))}
            </div>
          </>
        ) : (
          <p style={{ fontSize: '13px', color: '#939EA3', fontStyle: 'italic', margin: 0 }}>{t('results.notEnoughDataForField')}</p>
        )}
      </div>

      {mistakes && mistakes.length > 0 && (
        <div style={{
          padding: '26px 30px', borderRadius: '22px', background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)',
          backdropFilter: 'blur(16px)', boxShadow: '0 10px 30px rgba(31,55,75,0.06)', marginBottom: '22px',
        }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#161F24', margin: '0 0 4px' }}>{t('results.mistakesTitle')}</h3>
          <p style={{ fontSize: '12.5px', color: '#556269', margin: '0 0 18px' }}>{t('results.mistakesSubtitle')}</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {mistakes.map((group) => (
              <div key={group.indicatorKey}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '10px' }}>
                  <span style={{ fontSize: '13.5px', fontWeight: 700, color: '#1F374B' }}>{group.indicatorLabel}</span>
                  <span style={{ fontSize: '11.5px', fontWeight: 600, color: '#939EA3' }}>{t('results.mistakesCount')(group.count)}</span>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {group.items.map((item, idx) => (
                    <div key={idx} style={{
                      padding: '12px 16px', borderRadius: '14px', background: 'rgba(246,224,220,0.35)',
                      border: '1px solid rgba(189,91,76,0.18)',
                    }}>
                      <p style={{ fontSize: '12.5px', fontWeight: 600, color: '#161F24', margin: '0 0 6px', lineHeight: 1.5 }}>{item.prompt}</p>
                      <p style={{ fontSize: '12.5px', color: '#556269', margin: 0, lineHeight: 1.55 }}>{item.feedback}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ padding: '22px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.5)', border: '1px solid rgba(255,255,255,0.8)' }}>
        <h3 style={{ fontSize: '14.5px', fontWeight: 700, color: '#161F24', margin: '0 0 10px' }}>{t('results.whatThisMeans')}</h3>
        <p style={{ fontSize: '13.5px', lineHeight: 1.65, color: '#3B444A', margin: 0 }}>{overallExplanation}</p>
      </div>
    </div>
  );
}
