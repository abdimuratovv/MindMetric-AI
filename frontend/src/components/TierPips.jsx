import { ACHIEVEMENT_TIER_LEVEL } from '../constants/assessments.js';

/**
 * Small 1/2/3-dot level meter for a bronze/silver/gold tier — a
 * color-independent reinforcement of the tier chip's color, since bronze and
 * gold sit close enough in hue to be hard to tell apart at a glance. Filled
 * dots use the tier's own color; the rest are drawn as hollow outlines of
 * the same color rather than a neutral gray, so the pip reads as "this
 * tier's meter" rather than a generic control.
 */
export default function TierPips({ tier, color, size = 4 }) {
  const filled = ACHIEVEMENT_TIER_LEVEL[tier];
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '2.5px', flexShrink: 0 }}>
      {[0, 1, 2].map((i) => (
        <span key={i} style={{
          width: `${size}px`, height: `${size}px`, borderRadius: '50%', boxSizing: 'border-box',
          border: `1.2px solid ${color}`,
          background: i < filled ? color : 'transparent',
          opacity: i < filled ? 1 : 0.4,
        }} />
      ))}
    </span>
  );
}
