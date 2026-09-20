import { useEffect, useState } from 'react';

import { getInstitutionSettings, updateInstitutionSettings } from '../../api/admin.js';
import { ASSESSMENT_TYPES } from '../../constants/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

const INPUT_STYLE = {
  width: '100%', boxSizing: 'border-box', padding: '11px 14px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.14)',
  fontSize: '14px', fontFamily: 'Manrope', outline: 'none', background: 'rgba(255,255,255,0.85)', color: '#161F24',
};
const NUMBER_STYLE = { ...INPUT_STYLE, width: '92px', padding: '9px 10px', textAlign: 'center' };
const LABEL_STYLE = { display: 'block', fontSize: '12.5px', fontWeight: 700, color: '#556269', marginBottom: '6px' };

/** Form state keeps the numbers as strings while typing; the API gets ints back. */
const mapValues = (config, fn) => Object.fromEntries(
  Object.entries(config).map(([key, fields]) => [key, Object.fromEntries(Object.entries(fields).map(([f, v]) => [f, fn(v)]))]),
);
const toForm = (config) => mapValues(config, String);
const toPayload = (config) => mapValues(config, Number);

/** Admin settings: the institution header (name, term) and each indicator's question count / time limit. */
export default function AdminSettings() {
  const { t } = useLanguage();
  const [form, setForm] = useState({ name: '', academicTerm: '' });
  const [config, setConfig] = useState({});
  const [limits, setLimits] = useState({});
  const [loaded, setLoaded] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null); // {text, error}

  useEffect(() => {
    getInstitutionSettings()
      .then((data) => {
        setForm({ name: data.name, academicTerm: data.academicTerm });
        setConfig(toForm(data.assessmentConfig));
        setLimits(data.assessmentLimits);
        setLoaded(true);
      })
      .catch(() => setMessage({ text: t('adminSettings.loadError'), error: true }));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const update = (key, value) => { setForm((f) => ({ ...f, [key]: value })); setMessage(null); };
  const updateConfig = (key, field, value) => {
    setConfig((c) => ({ ...c, [key]: { ...c[key], [field]: value } }));
    setMessage(null);
  };
  const resetConfig = () => {
    setConfig(Object.fromEntries(Object.entries(limits).map(([key, l]) => [
      key, Object.fromEntries(Object.entries(l.fields).map(([f, meta]) => [f, String(meta.default)])),
    ])));
    setMessage(null);
  };

  const outOfRange = (key, field, value) => {
    const meta = limits[key]?.fields[field];
    const n = Number(value);
    return !meta || value === '' || !Number.isInteger(n) || n < meta.min || n > meta.max;
  };

  const save = async (e) => {
    e.preventDefault();
    const invalid = Object.entries(config).some(([key, fields]) => Object.keys(fields).some((f) => outOfRange(key, f, fields[f])));
    if (invalid) { setMessage({ text: t('adminSettings.invalid'), error: true }); return; }
    setSaving(true);
    try {
      const data = await updateInstitutionSettings({ ...form, assessmentConfig: toPayload(config) });
      setForm({ name: data.name, academicTerm: data.academicTerm });
      setConfig(toForm(data.assessmentConfig));
      setMessage({ text: t('adminSettings.saved'), error: false });
    } catch (err) {
      setMessage({ text: err.message, error: true });
    } finally {
      setSaving(false);
    }
  };

  const numberField = (key, field, label) => {
    const meta = limits[key].fields[field];
    const bad = outOfRange(key, field, config[key][field]);
    return (
      <div key={field}>
        <label htmlFor={`cfg-${key}-${field}`} style={{ ...LABEL_STYLE, fontSize: '11.5px' }}>{label}</label>
        <input
          id={`cfg-${key}-${field}`} type="number" inputMode="numeric" min={meta.min} max={meta.max}
          value={config[key][field]} disabled={!loaded} onChange={(e) => updateConfig(key, field, e.target.value)}
          aria-invalid={bad} style={{ ...NUMBER_STYLE, borderColor: bad ? '#BD5B4C' : 'rgba(31,55,75,0.14)' }}
        />
        <div style={{ fontSize: '11px', color: '#939EA3', marginTop: '3px', textAlign: 'center' }}>{t('adminSettings.range')(meta.min, meta.max)}</div>
      </div>
    );
  };

  const indicatorRow = (key) => {
    const { fields, bank } = limits[key];
    const countLabel = key === 'teamwork' ? t('adminSettings.scenarios') : key === 'algorithmic' ? t('adminSettings.mcqPhase') : t('adminSettings.questions');
    const overBank = Number(config[key].questions) > bank;
    return (
      <div key={key} style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'flex-start', gap: '14px 18px', padding: '14px 16px', borderRadius: '14px', background: 'rgba(255,255,255,0.55)', border: '1px solid rgba(31,55,75,0.08)' }}>
        <div style={{ flex: '1 1 220px', minWidth: 0 }}>
          <div style={{ fontSize: '13.5px', fontWeight: 700, color: '#161F24', lineHeight: 1.35 }}>{t(`assessmentsMeta.${key}`).title}</div>
          <div style={{ fontSize: '11.5px', color: overBank ? '#BD5B4C' : '#939EA3', marginTop: '4px', fontWeight: overBank ? 700 : 500 }}>
            {overBank ? t('adminSettings.bankShort')(bank) : t('adminSettings.inBank')(bank)}
          </div>
        </div>
        {numberField(key, 'questions', countLabel)}
        {fields.codingTasks && numberField(key, 'codingTasks', t('adminSettings.codingTasks'))}
        {fields.minutes ? numberField(key, 'minutes', t('adminSettings.minutes')) : (
          <div style={{ alignSelf: 'center', fontSize: '12px', color: '#939EA3', fontWeight: 600, maxWidth: '110px' }}>{t('adminSettings.noTimer')}</div>
        )}
      </div>
    );
  };

  const configReady = loaded && Object.keys(limits).length > 0;

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both', maxWidth: '760px' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('adminSettings.title')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 24px' }}>{t('adminSettings.subtitle')}</p>
      <form onSubmit={save} style={{ padding: '24px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)', display: 'flex', flexDirection: 'column', gap: '18px' }}>
        <div>
          <label htmlFor="inst-name" style={LABEL_STYLE}>{t('adminSettings.nameLabel')}</label>
          <input id="inst-name" value={form.name} maxLength={160} disabled={!loaded} onChange={(e) => update('name', e.target.value)} placeholder={t('adminSettings.namePlaceholder')} style={INPUT_STYLE} />
        </div>
        <div>
          <label htmlFor="inst-term" style={LABEL_STYLE}>{t('adminSettings.termLabel')}</label>
          <input id="inst-term" value={form.academicTerm} maxLength={80} disabled={!loaded} onChange={(e) => update('academicTerm', e.target.value)} placeholder={t('adminSettings.termPlaceholder')} style={INPUT_STYLE} />
        </div>
        {configReady && (
          <div style={{ borderTop: '1px solid rgba(31,55,75,0.1)', paddingTop: '20px' }}>
            <h2 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '18px', color: '#161F24', margin: '0 0 4px' }}>{t('adminSettings.testsTitle')}</h2>
            <p style={{ fontSize: '13px', color: '#556269', margin: '0 0 14px', lineHeight: 1.5 }}>{t('adminSettings.testsHint')}</p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {ASSESSMENT_TYPES.filter((key) => config[key] && limits[key]).map(indicatorRow)}
            </div>
            <button type="button" onClick={resetConfig} style={{ marginTop: '12px', padding: '7px 14px', borderRadius: '8px', border: '1px solid rgba(31,55,75,0.18)', background: 'transparent', color: '#2E5570', fontFamily: 'Manrope', fontWeight: 700, fontSize: '12.5px', cursor: 'pointer' }}>
              {t('adminSettings.reset')}
            </button>
          </div>
        )}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <button type="submit" disabled={!loaded || saving} style={{ padding: '10px 22px', borderRadius: '10px', border: 'none', background: '#1F374B', color: '#fff', fontFamily: 'Manrope', fontWeight: 700, fontSize: '13.5px', cursor: !loaded || saving ? 'default' : 'pointer', opacity: !loaded || saving ? 0.6 : 1 }}>
            {t('adminSettings.save')}
          </button>
          {message && <span role="status" style={{ fontSize: '13px', fontWeight: 600, color: message.error ? '#BD5B4C' : '#2E7052' }}>{message.text}</span>}
        </div>
      </form>
    </div>
  );
}
