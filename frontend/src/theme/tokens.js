/**
 * Design tokens — copied verbatim from MindMetric AI.dc.html's `colorTokens`
 * and `spacingScale` (renderVals(), lines ~1011-1017). Values must stay
 * byte-identical to the mockup; this file is the single place they're now
 * defined instead of being recomputed inline on every render.
 */
export const colorTokens = [
  { name: 'Navy', hex: '#1F374B' }, { name: 'Ocean', hex: '#2E5570' }, { name: 'Sky', hex: '#8FBCD9' },
  { name: 'Sky Pale', hex: '#DCECEF' }, { name: 'Sand', hex: '#F1EEE7' }, { name: 'Ink', hex: '#161F24' },
  { name: 'Ink Soft', hex: '#556269' }, { name: 'Amber', hex: '#B8862F' }, { name: 'Coral', hex: '#BD5B4C' },
  { name: 'Blue', hex: '#3E7EA6' }, { name: 'Bg Page', hex: '#F5F7F8' }, { name: 'Glass', hex: '#FFFFFF' },
];

export const spacingScale = [4, 8, 12, 16, 24, 32].map((px) => ({ px: `${px}px`, label: `${px}px` }));

/** Ported from the mockup's `polar()` helper (line 695) — used to draw the results radar chart. */
export function polar(angleDeg, radiusPx, cx, cy) {
  const rad = ((angleDeg - 90) * Math.PI) / 180;
  return { x: cx + radiusPx * Math.cos(rad), y: cy + radiusPx * Math.sin(rad) };
}
