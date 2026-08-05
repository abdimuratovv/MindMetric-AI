/**
 * Special-cased "Jamoa yulduzi" (teamwork) badge icon — decomposed into
 * separate paths (unlike every other ASSESSMENT_ICONS entry, which is one
 * static path) so the two teammates can shrink apart and a third, larger
 * figure can rise up between them with sparkles, matching the badge's name
 * literally: a "team star" emerges from the team. Only rendered for the
 * unlocked teamwork badge (Achievements.jsx) and its unlock reveal
 * (CompletionOverlay.jsx) — the locked/static state still uses the plain
 * combined iconPath from constants/assessments.js like every other badge.
 */
export default function TeamworkBadgeIcon({ size = 26, color, sparkleColor = color }) {
  return (
    <svg className="mm-badge-icon" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" style={{ overflow: 'visible' }}>
      <path d="M8 11a3 3 0 100-6 3 3 0 000 6zM2 21c0-3.5 2.7-6 6-6s6 2.5 6 6" style={{ transformOrigin: '6px 14px', animation: 'mm-badge-teamwork-a 3.4s ease-in-out infinite' }} />
      <path d="M16 11a3 3 0 100-6 3 3 0 000 6zM14 15.5c2.8.3 5 2.7 5 5.5" style={{ transformOrigin: '16px 14px', animation: 'mm-badge-teamwork-b 3.4s ease-in-out infinite' }} />
      <path d="M12 7.8a1.8 1.8 0 100-3.6 1.8 1.8 0 000 3.6zM9.5 14c0-2 1.1-3.3 2.5-3.3s2.5 1.3 2.5 3.3" style={{ transformOrigin: '12px 11px', animation: 'mm-badge-teamwork-c 3.4s ease-in-out infinite' }} />
      <path d="M8.6 3.6l0.5 1.5 1.5 0.5-1.5 0.5-0.5 1.5-0.5-1.5-1.5-0.5 1.5-0.5z" fill={sparkleColor} stroke="none" style={{ transformOrigin: '8.6px 5.6px', animation: 'mm-badge-teamwork-spark1 3.4s ease-in-out infinite' }} />
      <path d="M15.6 3.9l0.45 1.35 1.35 0.45-1.35 0.45-0.45 1.35-0.45-1.35-1.35-0.45 1.35-0.45z" fill={sparkleColor} stroke="none" style={{ transformOrigin: '15.6px 5.65px', animation: 'mm-badge-teamwork-spark2 3.4s ease-in-out infinite' }} />
    </svg>
  );
}
