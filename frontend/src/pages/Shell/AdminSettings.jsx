import { useEffect, useState } from 'react';

import { getInstitutionSettings, updateInstitutionSettings } from '../../api/admin.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

const INPUT_STYLE = {
  width: '100%', boxSizing: 'border-box', padding: '11px 14px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.14)',
  fontSize: '14px', fontFamily: 'Manrope', outline: 'none', background: 'rgba(255,255,255,0.85)', color: '#161F24',
};
const LABEL_STYLE = { display: 'block', fontSize: '12.5px', fontWeight: 700, color: '#556269', marginBottom: '6px' };

/** Admin settings: the institution name and academic term shown in the dashboard header. */
export default function AdminSettings() {
  const { t } = useLanguage();
  const [form, setForm] = useState({ name: '', academicTerm: '' });
  const [loaded, setLoaded] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null); // {text, error}

  useEffect(() => {
    getInstitutionSettings()
      .then((data) => { setForm({ name: data.name, academicTerm: data.academicTerm }); setLoaded(true); })
      .catch(() => setMessage({ text: t('adminSettings.loadError'), error: true }));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const update = (key, value) => { setForm((f) => ({ ...f, [key]: value })); setMessage(null); };

  const save = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const data = await updateInstitutionSettings(form);
      setForm({ name: data.name, academicTerm: data.academicTerm });
      setMessage({ text: t('adminSettings.saved'), error: false });
    } catch (err) {
      setMessage({ text: err.message, error: true });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both', maxWidth: '560px' }}>
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
