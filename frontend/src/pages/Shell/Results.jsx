import { useEffect, useState } from 'react';

import { getResultsMistakes, getResultsSummary } from '../../api/results.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import ResultsReport from './ResultsReport.jsx';

// Formatted by hand rather than via toLocaleDateString('uz-Latn-UZ', …): browsers'
// bundled ICU data has no Uzbek month names and silently falls back to "M07"-style
// placeholders. Russian has full Intl support, but a shared formatter keeps both
// languages consistent and doesn't depend on the runtime's locale data at all.
const MONTH_ABBR = {
  ru: ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'],
  uz: ['yan', 'fev', 'mar', 'apr', 'may', 'iyun', 'iyul', 'avg', 'sen', 'okt', 'noy', 'dek'],
};

function formatDate(date, lang) {
  return `${date.getDate()} ${MONTH_ABBR[lang][date.getMonth()]} ${date.getFullYear()}`;
}

/** Ported verbatim from MindMetric AI.dc.html lines 171-234 (`isResults`). */
export default function Results({ user, goTo }) {
  const [data, setData] = useState(null);
  const [mistakes, setMistakes] = useState(null);
  const { t, language } = useLanguage();

  useEffect(() => { getResultsSummary().then(setData); }, [language]);
  useEffect(() => { getResultsMistakes().then((res) => setMistakes(res.mistakes)); }, [language]);

  if (!data) return null;

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 4px' }}>
        {t('results.title')}
      </h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 26px' }}>
        {t('results.assessedOn')(user?.name, user?.program, formatDate(new Date(), language))}
      </p>

      <ResultsReport data={data} mistakes={mistakes} onViewAnalytics={() => goTo('analytics')} />
    </div>
  );
}
