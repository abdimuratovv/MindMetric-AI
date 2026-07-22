import { api } from './client.js';

/** Achievements/profile collection screen — all 10 badge slots, earned + locked. */
export const getAchievements = () => api.get('/achievements/');
