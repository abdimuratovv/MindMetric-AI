import { useEffect, useState } from 'react';

import { downloadStudentsCsv, getAdminKpis, getAdminStudents, getInstitutionSettings, getCohortDistribution, getFacultyActivity, getFieldDistribution, getStudentFilterOptions } from '../../api/admin.js';
import StudentFilters from '../../components/StudentFilters.jsx';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import { INITIAL_ADMIN_VIEW } from '../../state/useAppState.js';

const SHIMMER = {
  background: 'linear-gradient(90deg,#EDF2F3 0%,#F7F9FA 50%,#EDF2F3 100%)',
  backgroundSize: '800px 100%', animation: 'mm-shimmer 1.4s infinite linear',
};

const CARD = { padding: '24px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)' };
const TABLE_COLUMNS = '2fr 1fr 0.8fr 1.2fr 1fr 0.9fr';
const PAGE_SIZE = 10;
// Numbers and dates read best newest/highest first; text columns start A→Z.
const SORT_FIRST_DIRECTION = { name: 'asc', status: 'asc', score: 'desc', date: 'desc' };

const PAGER_BUTTON = (disabled) => ({
  padding: '8px 14px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.14)', background: 'rgba(255,255,255,0.8)',
  fontSize: '13px', fontFamily: 'Manrope', fontWeight: 600, color: disabled ? '#939EA3' : '#1F374B',
  cursor: disabled ? 'default' : 'pointer', opacity: disabled ? 0.6 : 1,
});

/** Institution dashboard. The faculty/course/group filters narrow every widget on the page, not just the table. */
export default function AdminOverview({ onOpenStudent, view, setView }) {
  const [loading, setLoading] = useState(true);
  const [adminKpis, setAdminKpis] = useState([]);
  const [distributionBars, setDistributionBars] = useState([]);
  const [fieldDistributionBars, setFieldDistributionBars] = useState([]);
  const [facultyActivity, setFacultyActivity] = useState([]);
  const [students, setStudents] = useState({ results: [], total: 0, page: 1, pageSize: PAGE_SIZE });
  const [searchFocused, setSearchFocused] = useState(false);
  const [filterOptions, setFilterOptions] = useState({ faculties: [], courses: [], groups: [] });
  const { search: adminSearch, filters, sort, page } = view;
  const [institution, setInstitution] = useState({ name: '', academicTerm: '' });
  const [exporting, setExporting] = useState(false);
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

  // Student table: additionally reacts to search, sorting and paging.
  useEffect(() => {
    let cancelled = false;
    const ordering = sort.direction === 'desc' ? `-${sort.field}` : sort.field;
    getAdminStudents({ search: adminSearch, ordering, page, pageSize: PAGE_SIZE, ...filters })
      .then((data) => { if (!cancelled) setStudents(data); });
    return () => { cancelled = true; };
  }, [filters, adminSearch, sort, page, language]);

  const updateFilter = (key, value) => setView((v) => ({ ...v, filters: { ...v.filters, [key]: value }, page: 1 }));
  const resetFilters = () => setView((v) => ({ ...v, filters: INITIAL_ADMIN_VIEW.filters, page: 1 }));
  const updateSearch = (value) => setView((v) => ({ ...v, search: value, page: 1 }));
  const setPage = (next) => setView((v) => ({ ...v, page: next }));
  const toggleSort = (field) => setView((v) => ({
    ...v,
    sort: v.sort.field === field
      ? { field, direction: v.sort.direction === 'asc' ? 'desc' : 'asc' }
      : { field, direction: SORT_FIRST_DIRECTION[field] },
    page: 1,
  }));

  const exportCsv = async () => {
    setExporting(true);
    try {
      await downloadStudentsCsv({ search: adminSearch, ordering: sort.direction === 'desc' ? `-${sort.field}` : sort.field, ...filters });
    } catch {
      // Nothing useful to show for a failed download beyond re-enabling the button.
    } finally {
      setExporting(false);
    }
  };

  const filtersActive = Object.values(filters).some(Boolean);
  const pageCount = Math.max(1, Math.ceil(students.total / students.pageSize));

  const sortHeader = (field, label) => (
    <button
      type="button" onClick={() => toggleSort(field)}
      style={{ all: 'unset', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '4px', color: sort.field === field ? '#1F374B' : '#939EA3' }}
    >
      {label}<span aria-hidden="true">{sort.field === field ? (sort.direction === 'asc' ? '▲' : '▼') : ''}</span>
    </button>
  );

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
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', flexWrap: 'wrap' }}>
                <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', margin: 0 }}>{t('admin.recentAssessments')}</h3>
                <span style={{ fontSize: '12.5px', color: '#939EA3' }}>{t('admin.totalStudents')(students.total)}</span>
              </div>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
              <button type="button" onClick={exportCsv} disabled={exporting || students.total === 0} style={PAGER_BUTTON(exporting || students.total === 0)}>{t('admin.exportCsv')}</button>
              <input
                value={adminSearch}
                onChange={(e) => updateSearch(e.target.value)}
                onFocus={() => setSearchFocused(true)}
                onBlur={() => setSearchFocused(false)}
                placeholder={t('common.searchStudents')}
                style={{
                  padding: '9px 14px', borderRadius: '10px',
                  border: `1px solid ${searchFocused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
                  boxShadow: searchFocused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
                  transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
                  fontSize: '13px', fontFamily: 'Manrope', outline: 'none', background: 'rgba(255,255,255,0.8)',
                  width: '220px', maxWidth: '100%',
                }}
              />
              </div>
            </div>
            <div style={{ overflowX: 'auto' }}>
              <div style={{ minWidth: '700px' }}>
                <div style={{ display: 'grid', gridTemplateColumns: TABLE_COLUMNS, gap: '10px', padding: '0 6px 10px', fontSize: '11.5px', fontWeight: 700, color: '#939EA3', borderBottom: '1px solid rgba(31,55,75,0.08)' }}>
                  {sortHeader('name', t('admin.tableStudent'))}
                  <span>{t('admin.tableGroup')}</span>
                  {sortHeader('score', t('admin.tableScore'))}
                  <span>{t('admin.tableLevel')}</span>
                  {sortHeader('status', t('admin.tableStatus'))}
                  {sortHeader('date', t('admin.tableDate'))}
                </div>
                {students.results.map((s, i) => (
                  <div
                    key={s.id ?? i} role="button" tabIndex={0}
                    onClick={() => onOpenStudent(s.id)}
                    onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpenStudent(s.id); } }}
                    style={{ display: 'grid', gridTemplateColumns: TABLE_COLUMNS, gap: '10px', padding: '13px 6px', fontSize: '13px', color: '#3B444A', borderBottom: '1px solid rgba(31,55,75,0.05)', alignItems: 'center', cursor: 'pointer' }}
                  >
                    <span style={{ fontWeight: 600, color: '#161F24' }}>{s.name}</span>
                    <span>{s.group || s.program || '—'}</span>
                    <span style={{ fontWeight: 700, color: '#1F374B' }}>{s.score ?? '—'}</span>
                    <span>
                      {s.levelLabel
                        ? <span style={{ fontSize: '11px', fontWeight: 700, padding: '3px 10px', borderRadius: '100px', background: s.levelBg, color: s.levelColor }}>{s.levelLabel}</span>
                        : '—'}
                    </span>
                    <span><span style={{ fontSize: '11px', fontWeight: 700, padding: '3px 10px', borderRadius: '100px', background: s.statusBg, color: s.statusColor }}>{s.statusLabel}</span></span>
                    <span style={{ color: '#939EA3' }}>{s.date ?? '—'}</span>
                  </div>
                ))}
              </div>
            </div>
            {students.results.length === 0 && (
              <div style={{ padding: '40px 0', textAlign: 'center', color: '#939EA3', fontSize: '13px' }}>{t('admin.noMatch')(adminSearch)}</div>
            )}
            {pageCount > 1 && (
              <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: '12px', marginTop: '16px' }}>
                <span style={{ fontSize: '12.5px', color: '#939EA3' }}>{t('admin.pageInfo')(students.page, pageCount)}</span>
                <button type="button" disabled={students.page <= 1} onClick={() => setPage(students.page - 1)} style={PAGER_BUTTON(students.page <= 1)}>{t('admin.pagePrev')}</button>
                <button type="button" disabled={students.page >= pageCount} onClick={() => setPage(students.page + 1)} style={PAGER_BUTTON(students.page >= pageCount)}>{t('admin.pageNext')}</button>
              </div>
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
