import { useLanguage } from '../../i18n/LanguageContext.jsx';

export default function ClusterRecommendation({ guidance, onOpen }) {
  const { language } = useLanguage();
  if (!guidance?.available) return null;
  const ru = language === 'ru';
  return <section className="cluster-recommendation" aria-label={ru ? 'Рекомендация по развитию' : 'Rivojlanish tavsiyasi'}
    style={{ padding: '24px', borderRadius: '22px', background: '#EDF2F8', border: '1px solid #D0DDE8', marginBottom: '22px', overflowWrap: 'anywhere' }}>
    <p style={{ margin: '0 0 12px', color: '#556269' }}>{ru ? 'Ваш следующий шаг' : 'Siz uchun keyingi qadam'}</p>
    {guidance.clusters.filter((row) => row.recommended).map((row) => <article key={row.id} data-recommended-cluster={row.id} style={{ marginBottom: '18px' }}>
      <h2 style={{ fontSize: '20px', margin: '0 0 8px', color: '#1F374B' }}>{row.headline}</h2>
      <strong>{row.title}</strong>
      <p style={{ lineHeight: 1.6 }}>{row.reason}</p>
      <ul style={{ paddingLeft: '20px', lineHeight: 1.8 }}>{row.indicators.map((indicator) =>
        <li key={indicator.key}>{indicator.label}: <strong>{indicator.score}/100</strong></li>)}</ul>
      {onOpen && <button type="button" className="mm-btn" onClick={() => onOpen(row.id)} style={{
        background: '#2E5570', color: '#fff', padding: '12px 18px', border: 0, borderRadius: '10px', cursor: 'pointer', maxWidth: '100%', whiteSpace: 'normal',
      }}>{ru ? 'Перейти к кластеру' : 'Tavsiya etilgan klasterga o‘tish'} →</button>}
    </article>)}
    <p style={{ fontSize: '13px', lineHeight: 1.6 }}>{guidance.note}</p>
    <p style={{ fontSize: '13px', marginBottom: 0 }}>{guidance.clusters.map((row) => `${['', 'I', 'II', 'III'][row.id]}: ${row.score}/100`).join(' · ')}</p>
  </section>;
}
