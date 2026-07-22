import { useEffect, useState } from 'react';

import { getAdminKpis, getAdminStudents, getCohortDistribution, getFacultyActivity, getFieldDistribution } from '../../api/admin.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

const SHIMMER = {
  background: 'linear-gradient(90deg,#EDF2F3 0%,#F7F9FA 50%,#EDF2F3 100%)',
  backgroundSize: '800px 100%', animation: 'mm-shimmer 1.4s infinite linear',
};

/** Ported verbatim from MindMetric AI.dc.html lines 372-444 (`isAdmin`). */
export default function AdminOverview() {
  const [loading, setLoading] = useState(true);
  const [adminKpis, setAdminKpis] = useState([]);
  const [distributionBars, setDistributionBars] = useState([]);
  const [fieldDistributionBars, setFieldDistributionBars] = useState([]);
  const [facultyActivity, setFacultyActivity] = useState([]);
  const [adminSearch, setAdminSearch] = useState('');
  const [adminStudents, setAdminStudents] = useState([]);
  const [searchFocused, setSearchFocused] = useState(false);
  const { t, language } = useLanguage();

  useEffect(() => {
    setLoading(true);
    Promise.all([getAdminKpis(), getCohortDistribution(), getFieldDistribution(), getFacultyActivity(), getAdminStudents(adminSearch)])
      .then(([kpis, distribution, fieldDistribution, activity, students]) => {
        setAdminKpis(kpis); setDistributionBars(distribution); setFieldDistributionBars(fieldDistribution);
        setFacultyActivity(activity); setAdminStudents(students);
        setLoading(false);
      });
  }, [language]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (loading) return;
    getAdminStudents(adminSearch).then(setAdminStudents);
  }, [adminSearch]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('admin.title')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 24px' }}>{t('admin.cohortLine')}</p>

      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '16px', marginBottom: '20px' }}>
          {[1, 2, 3, 4].map((i) => <div key={i} style={{ height: '96px', borderRadius: '18px', ...SHIMMER }} />)}
        </div>
      ) : (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '16px', marginBottom: '20px' }}>
            {adminKpis.map((k, i) => (
              <div key={i} style={{ padding: '20px 22px', borderRadius: '18px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)' }}>
                <div style={{ fontSize: '12px', fontWeight: 600, color: '#939EA3', marginBottom: '8px' }}>{k.label}</div>
                <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24' }}>{k.value}</div>
                <div style={{ fontSize: '11.5px', fontWeight: 700, color: k.deltaColor, marginTop: '4px' }}>{k.delta}</div>
              </div>
            ))}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1.3fr 1fr', gap: '20px', marginBottom: '20px' }}>
            <div style={{ padding: '24px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)' }}>
              <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', margin: '0 0 18px' }}>{t('admin.distributionTitle')}</h3>
              <div style={{ display: 'flex', alignItems: 'flex-end', gap: '22px', height: '160px' }}>
                {distributionBars.map((b, i) => (
                  <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', flex: 1, height: '100%', justifyContent: 'flex-end' }}>
                    <div style={{ fontSize: '12px', fontWeight: 700, color: '#161F24' }}>{b.pctLabel}</div>
                    <div style={{ width: '100%', maxWidth: '52px', height: b.barHeight, borderRadius: '8px 8px 3px 3px', background: b.color }} />
                    <div style={{ fontSize: '11px', color: '#939EA3', fontWeight: 600, textAlign: 'center' }}>{b.label}</div>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ padding: '24px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)' }}>
              <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', margin: '0 0 16px' }}>{t('admin.facultyActivityTitle')}</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {facultyActivity.map((f, i) => (
                  <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '13px', color: '#3B444A', fontWeight: 600 }}>{f.name}</span>
                    <span style={{ fontSize: '12.5px', color: '#939EA3' }}>{t('admin.reviewedCount')(f.count)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div style={{ padding: '24px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)', marginBottom: '20px' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', margin: '0 0 18px' }}>{t('admin.fieldDistributionTitle')}</h3>
            <div style={{ display: 'flex', alignItems: 'flex-end', gap: '18px', height: '160px' }}>
              {fieldDistributionBars.map((b, i) => (
                <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', flex: 1, height: '100%', justifyContent: 'flex-end' }}>
                  <div style={{ fontSize: '12px', fontWeight: 700, color: '#161F24' }}>{b.pctLabel}</div>
                  <div style={{ width: '100%', maxWidth: '52px', height: b.barHeight, borderRadius: '8px 8px 3px 3px', background: b.color }} />
                  <div style={{ fontSize: '10.5px', color: '#939EA3', fontWeight: 600, textAlign: 'center' }}>{b.label}</div>
                </div>
              ))}
            </div>
          </div>

          <div style={{ padding: '22px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', margin: 0 }}>{t('admin.recentAssessments')}</h3>
              <input
                value={adminSearch}
                onChange={(e) => setAdminSearch(e.target.value)}
                onFocus={() => setSearchFocused(true)}
                onBlur={() => setSearchFocused(false)}
                placeholder={t('common.searchStudents')}
                style={{
                  padding: '9px 14px', borderRadius: '10px',
                  border: `1px solid ${searchFocused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
                  boxShadow: searchFocused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
                  transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
                  fontSize: '13px', fontFamily: 'Manrope', outline: 'none', background: 'rgba(255,255,255,0.8)', width: '220px',
                }}
              />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1.4fr 0.9fr 1fr 1fr', gap: '10px', padding: '0 6px 10px', fontSize: '11.5px', fontWeight: 700, color: '#939EA3', borderBottom: '1px solid rgba(31,55,75,0.08)' }}>
              <span>{t('admin.tableStudent')}</span><span>{t('admin.tableProgram')}</span><span>{t('admin.tableScore')}</span><span>{t('admin.tableStatus')}</span><span>{t('admin.tableDate')}</span>
            </div>
            {adminStudents.map((s, i) => (
              <div key={i} style={{ display: 'grid', gridTemplateColumns: '2fr 1.4fr 0.9fr 1fr 1fr', gap: '10px', padding: '13px 6px', fontSize: '13px', color: '#3B444A', borderBottom: '1px solid rgba(31,55,75,0.05)', alignItems: 'center' }}>
                <span style={{ fontWeight: 600, color: '#161F24' }}>{s.name}</span>
                <span>{s.program}</span>
                <span style={{ fontWeight: 700, color: '#1F374B' }}>{s.score}</span>
                <span><span style={{ fontSize: '11px', fontWeight: 700, padding: '3px 10px', borderRadius: '100px', background: s.statusBg, color: s.statusColor }}>{s.statusLabel}</span></span>
                <span style={{ color: '#939EA3' }}>{s.date}</span>
              </div>
            ))}
            {adminStudents.length === 0 && (
              <div style={{ padding: '40px 0', textAlign: 'center', color: '#939EA3', fontSize: '13px' }}>{t('admin.noMatch')(adminSearch)}</div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
