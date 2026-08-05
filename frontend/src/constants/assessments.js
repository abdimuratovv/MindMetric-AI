/**
 * Single source of truth for the 10 assessment cards — mirrors
 * apps.assessments.models.AssessmentAttempt.Type (backend) and its
 * MCQ_TYPES/CODING_TYPES/LIKERT_TYPES groupings.
 *
 * ASSESSMENT_TYPES drives card order on the selection screen; ASSESSMENT_PATTERN
 * drives which generalized screen component (Mcq/Coding/Likert) handles a given
 * type inside FocusedTestShell.
 */
export const ASSESSMENT_TYPES = [
  'math', 'logic', 'algorithmic', 'creative', 'teamwork',
  'patience', 'problem_solving', 'learning_speed', 'attention', 'iq',
];

export const ASSESSMENT_PATTERN = {
  math: 'mcq', logic: 'mcq', algorithmic: 'mcq', creative: 'mcq', problem_solving: 'mcq', attention: 'mcq', iq: 'mcq',
  teamwork: 'likert', patience: 'likert', learning_speed: 'likert',
};

/**
 * Icon/color per indicator — shared by the selection screen's cards, the
 * post-test completion overlay, and the achievements collection page, so a
 * badge always shows the same glyph as the test that earns it. Only
 * icon/color are UI content here; title/desc/duration come from i18n
 * (assessmentsMeta) and score/status come from the backend.
 */
export const ASSESSMENT_ICONS = {
  math: {
    iconBg: '#DDEAF1', iconColor: '#3E7EA6',
    iconPath: 'M5 3h14a1 1 0 011 1v16a1 1 0 01-1 1H5a1 1 0 01-1-1V4a1 1 0 011-1zM7 7h10M9 12h2M13 12h2M9 16h2M13 16h2',
  },
  logic: {
    iconBg: '#DCECEF', iconColor: '#2E5570',
    iconPath: 'M6 6a2 2 0 100 4 2 2 0 000-4zM18 6a2 2 0 100 4 2 2 0 000-4zM12 16a2 2 0 100 4 2 2 0 000-4zM7.5 9l3.5 5M16.5 9l-3.5 5',
  },
  algorithmic: {
    iconBg: '#DDEAF1', iconColor: '#3E7EA6',
    iconPath: 'M8 9l-4 3 4 3M16 9l4 3-4 3M13 6l-2 12',
  },
  creative: {
    iconBg: '#F5E9D3', iconColor: '#B8862F',
    iconPath: 'M9 18h6M10 21h4M12 3a6 6 0 00-3 11.2c.5.4.8 1 .8 1.8h4.4c0-.8.3-1.4.8-1.8A6 6 0 0012 3z',
  },
  teamwork: {
    iconBg: '#F6E0DC', iconColor: '#BD5B4C',
    iconPath: 'M8 11a3 3 0 100-6 3 3 0 000 6zM16 11a3 3 0 100-6 3 3 0 000 6zM2 21c0-3.5 2.7-6 6-6s6 2.5 6 6M14 15.5c2.8.3 5 2.7 5 5.5',
  },
  patience: {
    iconBg: '#DCECEF', iconColor: '#2E5570',
    iconPath: 'M7 3h10M7 21h10M7 3c0 4 5 5 5 8s-5 4-5 8M17 3c0 4-5 5-5 8s5 4 5 8',
  },
  problem_solving: {
    iconBg: '#F5E9D3', iconColor: '#B8862F',
    iconPath: 'M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z',
  },
  learning_speed: {
    iconBg: '#F6E0DC', iconColor: '#BD5B4C',
    iconPath: 'M13 3L4 14h6l-1 7 9-11h-6l1-7z',
  },
  attention: {
    iconBg: '#DCECEF', iconColor: '#2E5570',
    iconPath: 'M12 5c-7 0-10 7-10 7s3 7 10 7 10-7 10-7-3-7-10-7zM12 15a3 3 0 100-6 3 3 0 000 6z',
  },
  iq: {
    iconBg: '#DDEAF1', iconColor: '#3E7EA6',
    iconPath: 'M9 4a3 3 0 00-3 3 3 3 0 00-1 5.8 3 3 0 002.6 4.2H9v2h6v-2h1.4a3 3 0 002.6-4.2A3 3 0 0018 7a3 3 0 00-3-3 3 3 0 00-3 1 3 3 0 00-3-1z',
  },
};

/**
 * Bronze/silver/gold visual treatment for the achievement badges — a soft
 * background + a metallic-toned foreground, distinct from the analytical
 * tier chips (calculators._TIERS colors) elsewhere in the app so a badge
 * reads as a collectible, not a repeated stat.
 *
 * Bronze and gold sit close in hue (both warm orange/yellow), so they're
 * pushed deliberately apart: bronze toward a darker, more muted copper
 * (~30° hue) and gold toward a brighter, more saturated yellow (~48° hue,
 * meaningfully higher lightness) so gold reads as the "shinier" tier rather
 * than a duller version of bronze. See also ACHIEVEMENT_TIER_LEVEL below for
 * the color-independent cue.
 */
export const ACHIEVEMENT_TIER_COLORS = {
  bronze: { bg: '#F5E8DB', color: '#874C1D', ring: '#CD7F32' },
  silver: { bg: '#EEF0F1', color: '#6B7278', ring: '#A9B0B5' },
  gold: { bg: '#FBF1D2', color: '#AE8A13', ring: '#E2C75A' },
};

/**
 * How many of 3 pips a tier fills in the small level-meter drawn next to a
 * tier label (components/TierPips.jsx) — a redundant, color-independent
 * signal for bronze vs. gold, whose hues are close enough to be hard to
 * tell apart at a glance (or for colorblind users). Mirrors TIER_ORDER in
 * apps.scoring.achievements on the backend.
 */
export const ACHIEVEMENT_TIER_LEVEL = { bronze: 1, silver: 2, gold: 3 };

/**
 * One distinct looping CSS animation per indicator, keyed to what its icon
 * depicts (e.g. the hourglass flips, the eye blinks) — used only for the
 * *unlocked* badge icon on the achievements collection page and for the
 * badge reveal in CompletionOverlay. Keyframes live in index.html alongside
 * the app's other mm-* animations.
 */
export const ACHIEVEMENT_ICON_ANIMATIONS = {
  math: { name: 'mm-badge-math', duration: '2.6s' },
  logic: { name: 'mm-badge-logic', duration: '2.2s' },
  algorithmic: { name: 'mm-badge-algorithmic', duration: '2.8s' },
  creative: { name: 'mm-badge-creative', duration: '2.4s' },
  // teamwork has no entry here — it renders via <TeamworkBadgeIcon>, a
  // decomposed multi-part animation (see components/TeamworkBadgeIcon.jsx).
  patience: { name: 'mm-badge-patience', duration: '3.6s' },
  problem_solving: { name: 'mm-badge-problem-solving', duration: '3.2s' },
  learning_speed: { name: 'mm-badge-learning-speed', duration: '2.8s' },
  attention: { name: 'mm-badge-attention', duration: '4.2s' },
  iq: { name: 'mm-badge-iq', duration: '2.6s' },
};
