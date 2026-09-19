import { useEffect, useState } from 'react';

import { getAdminKpis, getAdminStudents, getInstitutionSettings, getCohortDistribution, getFacultyActivity, getFieldDistribution, getStudentFilterOptions } from '../../api/admin.js';
import StudentFilters from '../../components/StudentFilters.jsx';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import { CARD, PAGER_BUTTON } from '../../components/adminStyles.js';
import { INITIAL_ADMIN_VIEW } from '../../state/useAppState.js';

const SHIMMER = {
  background: 'linear-gradient(90deg,#EDF2F3 0%,#F7F9FA 50%,#EDF2F3 100%)',
  backgroundSize: '800px 100%', animation: 'mm-shimmer 1.4s infinite linear',
};

const PREVIEW_ROWS = 5;
const PREVIEW_COLUMNS = '2fr 0.8fr 1.2fr 0.9fr';

/** Institution dashboard. The faculty/course/group filters narrow every widget on the page, not just the table. */
export default function AdminOverview({ onOpenStudent, onViewAll, view, setView }) {
  const [loading, setLoading] = useState(true);
  const [adminKpis, setAdminKpis] = useState([]);
  const [distributionBars, setDistributionBars] = useState([]);
  const [fieldDistributionBars, setFieldDistributionBars] = useState([]);
  const [facultyActivity, setFacultyActivity] = useState([]);
  const [recent, setRecent] = useState([]);
  const [filterOptions, setFilterOptions] = useState({ faculties: [], courses: [], groups: [] });
  const { filters } = view;
  const [institution, setInstitution] = useState({ name: '', academicTerm: '' });
  const { t, language } = useLanguage();

  useEffect(() => {
    getStudentFilterOptions().then(setFilterOptions);
    getInstitutionSettings().then(setInstitution).catch(() => {});
  }, []);

  // Dashboard widgets: reload when the filters (or language, for backend-localized labels) change.
  useEffect(() => {
    let cancelled = false;
    Promise.all([getAdminKpis(filters), getCohortDistribution(filters), getFieldDistribution(filters), getFacultyActivity(filters)])
      .then(([kpis, distribution, fieldDistribution, activity]) => {
        if (cancelled) return;
        setAdminKpis(kpis); setDistributionBars(distribution); setFieldDistributionBars(fieldDistribution);
        setFacultyActivity(activity); setLoading(false);
      });
    return () => { cancelled = true; };
  }, [filters, language]);

  // Latest results preview — the full roster lives on the Students screen.
  useEffect(() => {
    let cancelled = false;
    getAdminStudents({ ordering: '-date', page: 1, pageSize: PREVIEW_ROWS, ...filters })
      .then((data) => { if (!cancelled) setRecent(data.results); });
    return () => { cancelled = true; };
  }, [filters, language]);

  const updateFilter = (key, value) => setView((v) => ({ ...v, filters: { ...v.filters, [key]: value } }));
  const resetFilters = () => setView((v) => ({ ...v, filters: INITIAL_ADMIN_VIEW.filters }));
  const filtersActive = Object.values(filters).some(Boolean);

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('admin.title')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 20px' }}>{[institution.name, institution.academicTerm].filter(Boolean).join(' · ') || t('admin.subtitle')}</p>

      <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap', marginBottom: '20px' }}>
        <StudentFilters options={filterOptions} filters={filters} onChange={updateFilter} />
        {filtersActive && (
          <button type="button" onClick={resetFilters} style={{ ...PAGER_BUTTON(false), color: '#BD5B4C' }}>{t('admin.resetFilters')}</button>
        )}
      </div>

      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '16px', marginBottom: '20px' }}>
          {[1, 2, 3, 4].map((i) => <div key={i} style={{ height: '96px', borderRadius: '18px', ...SHIMMER }} />)}
        </div>
      ) : (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '16px', marginBottom: '20px' }}>
            {adminKpis.map((k, i) => (
              <div key={i} style={{ padding: '20px 22px', borderRadius: '18px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)' }}>
                <div style={{ fontSize: '12px', fontWeight: 600, color: '#939EA3', marginBottom: '8px' }}>{k.label}</div>
                <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24' }}>{k.value}</div>
                {k.delta && <div style={{ fontSize: '11.5px', fontWeight: 700, color: k.deltaColor, marginTop: '4px' }}>{k.delta}</div>}
              </div>
            ))}
          </div>

          <div style={{ ...CARD, padding: '22px 26px', marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', flexWrap: 'wrap', gap: '10px', marginBottom: '16px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', margin: 0 }}>{t('admin.recentAssessments')}</h3>
              <button type="button" onClick={onViewAll} style={{ border: 'none', background: 'none', color: '#2E5570', fontWeight: 700, fontSize: '13px', cursor: 'pointer', padding: 0 }}>{t('admin.viewAll')}</button>
            </div>
            <div style={{ overflowX: 'auto' }}>
              <div style={{ minWidth: '520px' }}>
                <div style={{ display: 'grid', gridTemplateColumns: PREVIEW_COLUMNS, gap: '10px', padding: '0 6px 10px', fontSize: '11.5px', fontWeight: 700, color: '#939EA3', borderBottom: '1px solid rgba(31,55,75,0.08)' }}>
                  <span>{t('admin.tableStudent')}</span><span>{t('admin.tableScore')}</span><span>{t('admin.tableLevel')}</span><span>{t('admin.tableDate')}</span>
                </div>
                {recent.map((s) => (
                  <div
                    key={s.id} role="button" tabIndex={0}
                    onClick={() => onOpenStudent(s.id)}
                    onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpenStudent(s.id); } }}
                    style={{ display: 'grid', gridTemplateColumns: PREVIEW_COLUMNS, gap: '10px', padding: '13px 6px', fontSize: '13px', color: '#3B444A', borderBottom: '1px solid rgba(31,55,75,0.05)', alignItems: 'center', cursor: 'pointer' }}
                  >
                    <span style={{ fontWeight: 600, color: '#161F24' }}>{s.name}</span>
                    <span style={{ fontWeight: 700, color: '#1F374B' }}>{s.score ?? '—'}</span>
                    <span>
                      {s.levelLabel
                        ? <span style={{ fontSize: '11px', fontWeight: 700, padding: '3px 10px', borderRadius: '100px', background: s.levelBg, color: s.levelColor }}>{s.levelLabel}</span>
                        : '—'}
                    </span>
                    <span style={{ color: '#939EA3' }}>{s.date ?? '—'}</span>
                  </div>
                ))}
              </div>
            </div>
            {recent.length === 0 && (
              <div style={{ padding: '32px 0', textAlign: 'center', color: '#939EA3', fontSize: '13px' }}>{t('admin.noRecent')}</div>
            )}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '20px' }}>
            <div style={CARD}>
              <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', margin: '0 0 18px' }}>{t('admin.distributionTitle')}</h3>
              <div style={{ display: 'flex', alignItems: 'flex-end', gap: '22px', height: '160px' }}>
                {distributionBars.map((b, i) => (
                  <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', flex: 1, height: '100%', justifyContent: 'flex-end' }}>
                    <div style={{ fontSize: '12px', fontWeight: 700, color: '#161F24' }}>{b.pctLabel} ({b.count})</div>
                    <div style={{ width: '100%', maxWidth: '52px', height: b.barHeight, borderRadius: '8px 8px 3px 3px', background: b.color }} />
                    <div style={{ fontSize: '11px', color: '#939EA3', fontWeight: 600, textAlign: 'center' }}>{b.label}</div>
                  </div>
                ))}
              </div>
            </div>
            <div style={CARD}>
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

          <div style={CARD}>
            <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', margin: '0 0 18px' }}>{t('admin.fieldDistributionTitle')}</h3>
            <div style={{ display: 'flex', alignItems: 'flex-end', gap: '18px', height: '160px' }}>
              {fieldDistributionBars.map((b, i) => (
                <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', flex: 1, height: '100%', justifyContent: 'flex-end' }}>
                  <div style={{ fontSize: '12px', fontWeight: 700, color: '#161F24' }}>{b.pctLabel} ({b.count})</div>
                  <div style={{ width: '100%', maxWidth: '52px', height: b.barHeight, borderRadius: '8px 8px 3px 3px', background: b.color }} />
                  <div style={{ fontSize: '10.5px', color: '#939EA3', fontWeight: 600, textAlign: 'center' }}>{b.label}</div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
