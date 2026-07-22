import { api } from './client.js';

/** Results screen — {{ overallScore }}/{{ band }}/{{ indicators }}. */
export const getResultsSummary = () => api.get('/results/summary/');

/** Detailed analytics screen — {{ indicatorsDetail }}. */
export const getResultsAnalytics = () => api.get('/results/analytics/');

/** Results screen's "typical mistakes" section — pedagogical feedback per wrong answer. */
export const getResultsMistakes = () => api.get('/results/mistakes/');
