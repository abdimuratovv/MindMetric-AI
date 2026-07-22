import { api } from './client.js';

/** Welcome screen — {{ welcomeStats }}. No auth required. */
export const getPublicStats = () => api.get('/public/stats/');
