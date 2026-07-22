import { createContext, useContext, useMemo, useState } from 'react';

import { translations } from './translations.js';

export const LANGUAGES = ['ru', 'uz'];
export const DEFAULT_LANGUAGE = 'ru';
const STORAGE_KEY = 'mindmetric_language';

/** Read once at module init so api/client.js (outside the React tree) can attach
 * the same X-Language header without needing a hook. */
export function getStoredLanguage() {
  const stored = localStorage.getItem(STORAGE_KEY);
  return LANGUAGES.includes(stored) ? stored : DEFAULT_LANGUAGE;
}

const LanguageContext = createContext(null);

function resolve(dict, path) {
  return path.split('.').reduce((node, key) => (node == null ? undefined : node[key]), dict);
}

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(getStoredLanguage);

  const setLanguage = (next) => {
    if (!LANGUAGES.includes(next) || next === language) return;
    localStorage.setItem(STORAGE_KEY, next);
    setLanguageState(next);
  };

  const value = useMemo(() => ({
    language,
    setLanguage,
    // t('auth.welcomeBack') -> string; t('auth.signInAs')('Student') -> string,
    // for the handful of strings that interpolate a value.
    t: (path) => {
      const value = resolve(translations[language], path);
      if (value === undefined) return path;
      return value;
    },
  }), [language]);

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useLanguage must be used within a LanguageProvider');
  return ctx;
}
