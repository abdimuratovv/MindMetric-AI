import TeamworkBadgeIcon from '../../components/TeamworkBadgeIcon.jsx';
import TierPips from '../../components/TierPips.jsx';
import { ACHIEVEMENT_ICON_ANIMATIONS, ACHIEVEMENT_TIER_COLORS, ASSESSMENT_ICONS } from '../../constants/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

/**
 * Shown right after an indicator's test is submitted (Mcq/Coding/Likert), on
 * top of everything else, before the student is routed back to the selection
 * screen. Always shows the score just earned on this one indicator; when the
 * submission crossed a new badge tier, `achievement` is set and a badge
 * reveal is shown alongside it — see StudentStateTracker.complete_attempt /
 * apps.scoring.achievements on the backend for the awarding rule.
 */
export default function CompletionOverlay({ indicatorKey, score, achievement, onContinue }) {
  const { t } = useLanguage();
  const icon = ASSESSMENT_ICONS[indicatorKey];
  const tierColors = achievement ? ACHIEVEMENT_TIER_COLORS[achievement.tier] : null;

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 50, display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'rgba(22,31,36,0.45)', backdropFilter: 'blur(6px)', animation: 'mm-fade-up 0.25s ease both',
    }}>
      <div style={{
        width: '420px', maxWidth: 'calc(100vw - 40px)', padding: '38px 34px', borderRadius: '26px',
        background: 'rgba(255,255,255,0.92)', border: '1px solid rgba(255,255,255,0.9)',
        boxShadow: '0 30px 70px rgba(22,31,36,0.28)', textAlign: 'center',
      }}>
        <div style={{ fontSize: '12px', fontWeight: 700, color: '#2E5570', letterSpacing: '0.04em', marginBottom: '6px' }}>
          {t('completion.title')}
        </div>

        <div style={{
          width: '64px', height: '64px', borderRadius: '18px', background: icon.iconBg, margin: '10px auto 18px',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke={icon.iconColor} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d={icon.iconPath}></path>
          </svg>
        </div>

        <div style={{ fontSize: '12px', fontWeight: 700, color: '#939EA3', letterSpacing: '0.04em', marginBottom: '2px' }}>
          {t('completion.scoreLabel')}
        </div>
        <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '52px', lineHeight: 1, color: '#1F374B', marginBottom: achievement ? '22px' : '28px' }}>
          {score ?? '—'}
        </div>

        {achievement && (
          <div style={{
            display: 'flex', alignItems: 'center', gap: '14px', padding: '16px 18px', borderRadius: '18px',
            background: tierColors.bg, border: `1.5px solid ${tierColors.ring}`, marginBottom: '26px', textAlign: 'left',
          }}>
            <div style={{
              width: '46px', height: '46px', borderRadius: '50%', background: '#fff', flexShrink: 0,
              display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 0 0 2px ${tierColors.ring}`,
            }}>
              {indicatorKey === 'teamwork' ? (
                <div style={{ animation: 'mm-badge-reveal 0.7s cubic-bezier(0.34,1.56,0.64,1) both' }}>
                  <TeamworkBadgeIcon size={22} color={tierColors.color} sparkleColor={tierColors.ring} />
                </div>
              ) : (
                <svg
                  width="22" height="22" viewBox="0 0 24 24" fill="none" stroke={tierColors.color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"
                  style={{
                    animation: `mm-badge-reveal 0.7s cubic-bezier(0.34,1.56,0.64,1) both, ${ACHIEVEMENT_ICON_ANIMATIONS[indicatorKey].name} ${ACHIEVEMENT_ICON_ANIMATIONS[indicatorKey].duration} ease-in-out 0.7s infinite`,
                  }}
                >
                  <path d={icon.iconPath}></path>
                </svg>
              )}
            </div>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: '11px', fontWeight: 700, color: tierColors.color, letterSpacing: '0.03em', marginBottom: '2px' }}>
                {t('completion.newBadge')}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '14.5px', fontWeight: 700, color: '#161F24' }}>
                <span>{achievement.name} · {achievement.tierLabel}</span>
                <TierPips tier={achievement.tier} color={tierColors.color} />
              </div>
            </div>
          </div>
        )}

        <button
          className="mm-btn"
          onClick={onContinue}
          style={{
            width: '100%', padding: '13px 0', borderRadius: '100px', border: 'none', cursor: 'pointer',
            background: '#2E5570', color: '#fff', fontWeight: 700, fontSize: '14px',
          }}
        >{t('completion.continue')}</button>
      </div>
    </div>
  );
}
