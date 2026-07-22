import { useEffect, useState } from 'react';

import { getAchievements } from '../../api/achievements.js';
import TeamworkBadgeIcon from '../../components/TeamworkBadgeIcon.jsx';
import { ACHIEVEMENT_ICON_ANIMATIONS, ACHIEVEMENT_TIER_COLORS, ASSESSMENT_ICONS } from '../../constants/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

const MONTH_ABBR = {
  ru: ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'],
  uz: ['yan', 'fev', 'mar', 'apr', 'may', 'iyun', 'iyul', 'avg', 'sen', 'okt', 'noy', 'dek'],
};

function formatDate(iso, lang) {
  const d = new Date(iso);
  return `${d.getDate()} ${MONTH_ABBR[lang][d.getMonth()]} ${d.getFullYear()}`;
}

/**
 * The student's gamification "collection" — one tile per indicator (10
 * total), earned badges shown in full color with their tier ring, locked
 * ones dimmed with the badge name still visible as a teaser. Backed by
 * GET /api/achievements/ (apps.scoring.views.AchievementListView).
 */
export default function Achievements() {
  const [data, setData] = useState(null);
  const { t, language } = useLanguage();

  useEffect(() => { getAchievements().then(setData); }, [language]);

  if (!data) return null;

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 4px' }}>
            {t('achievements.title')}
          </h1>
          <p style={{ fontSize: '14px', color: '#556269', margin: 0 }}>{t('achievements.subtitle')}</p>
        </div>
        <span style={{
          padding: '9px 18px', borderRadius: '100px', fontWeight: 700, fontSize: '13px',
          background: 'rgba(46,85,112,0.12)', color: '#1F374B', whiteSpace: 'nowrap',
        }}>
          {t('achievements.progress')(data.earnedCount, data.totalCount)}
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(240px,1fr))', gap: '18px' }}>
        {data.badges.map((b) => {
          const icon = ASSESSMENT_ICONS[b.key];
          const tierColors = b.locked ? null : ACHIEVEMENT_TIER_COLORS[b.tier];
          return (
            <div key={b.key} style={{
              padding: '24px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)',
              border: `1px solid ${b.locked ? 'rgba(255,255,255,0.85)' : tierColors.ring}`,
              backdropFilter: 'blur(16px)', boxShadow: '0 10px 30px rgba(31,55,75,0.06)',
              display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', gap: '12px',
              opacity: b.locked ? 0.6 : 1,
            }}>
              <div style={{
                width: '58px', height: '58px', borderRadius: '50%', flexShrink: 0,
                background: b.locked ? '#EDF1F1' : '#fff',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: b.locked ? 'none' : `0 0 0 3px ${tierColors.ring}`,
              }}>
                {!b.locked && b.key === 'teamwork' ? (
                  <TeamworkBadgeIcon size={26} color={icon.iconColor} />
                ) : (
                  <svg
                    className={b.locked ? undefined : 'mm-badge-icon'}
                    width="26" height="26" viewBox="0 0 24 24" fill="none"
                    stroke={b.locked ? '#B7C1C4' : icon.iconColor} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"
                    style={b.locked ? undefined : { animation: `${ACHIEVEMENT_ICON_ANIMATIONS[b.key].name} ${ACHIEVEMENT_ICON_ANIMATIONS[b.key].duration} ease-in-out infinite` }}
                  >
                    <path d={icon.iconPath}></path>
                  </svg>
                )}
              </div>

              <div>
                <div style={{ fontSize: '15px', fontWeight: 700, color: b.locked ? '#939EA3' : '#161F24', marginBottom: '3px' }}>
                  {b.name}
                </div>
                <div style={{ fontSize: '11.5px', color: '#939EA3' }}>{b.label}</div>
              </div>

              <span style={{
                padding: '5px 14px', borderRadius: '100px', fontWeight: 700, fontSize: '11.5px',
                background: b.locked ? '#EDF1F1' : tierColors.bg, color: b.locked ? '#939EA3' : tierColors.color,
              }}>
                {b.locked ? t('achievements.locked') : b.tierLabel}
              </span>

              {!b.locked && (
                <div style={{ fontSize: '11px', color: '#939EA3' }}>
                  {t('achievements.earnedOn')(formatDate(b.earnedAt, language))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
