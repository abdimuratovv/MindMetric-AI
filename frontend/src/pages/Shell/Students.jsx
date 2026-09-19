import { useEffect, useState } from 'react';

import { downloadStudentsCsv, getAdminStudents, getStudentFilterOptions } from '../../api/admin.js';
import { CARD, PAGER_BUTTON, SELECT_STYLE } from '../../components/adminStyles.js';
import StudentFilters from '../../components/StudentFilters.jsx';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import { INITIAL_STUDENTS_VIEW } from '../../state/useAppState.js';

const TABLE_COLUMNS = '2fr 0.9fr 0.7fr 1.2fr 1.1fr 1fr 0.9fr';
const PAGE_SIZES = [10, 25, 50];
const LEVEL_KEYS = ['foundational', 'developing', 'high', 'none'];
const STATUS_KEYS = ['pending', 'flagged', 'reviewed'];
// Numbers and dates read best highest/newest first; text columns start A→Z.
const SORT_FIRST_DIRECTION = { name: 'asc', status: 'asc', score: 'desc', progress: 'desc', date: 'desc' };

/**
 * Full student roster: everyone registered (including students with no results yet),
 * with faculty/course/group + level + review-status filters, search, sorting, paging
 * and CSV export. Rows open the per-student report.
 */
export default function Students({ onOpenStudent, view, setView }) {
  const { t, language } = useLanguage();
  const [students, setStudents] = useState({ results: [], total: 0, page: 1, pageSize: view.pageSize });
  const [loaded, setLoaded] = useState(false);
  const [filterOptions, setFilterOptions] = useState({ faculties: [], courses: [], groups: [] });
  const [searchFocused, setSearchFocused] = useState(false);
  const [exporting, setExporting] = useState(false);
  const { search, filters, level, status, sort, page, pageSize } = view;
  const ordering = sort.direction === 'desc' ? `-${sort.field}` : sort.field;

  useEffect(() => { getStudentFilterOptions().then(setFilterOptions); }, []);

  useEffect(() => {
    let cancelled = false;
    getAdminStudents({ search, ordering, page, pageSize, level, status, ...filters })
      .then((data) => { if (!cancelled) { setStudents(data); setLoaded(true); } });
    return () => { cancelled = true; };
  }, [search, ordering, page, pageSize, level, status, filters, language]);

  const patch = (changes) => setView((v) => ({ ...v, ...changes, page: 1 }));
  const updateFilter = (key, value) => patch({ filters: { ...filters, [key]: value } });
  const resetFilters = () => patch({ filters: INITIAL_STUDENTS_VIEW.filters, level: '', status: '' });
  const toggleSort = (field) => patch({
    sort: sort.field === field
      ? { field, direction: sort.direction === 'asc' ? 'desc' : 'asc' }
      : { field, direction: SORT_FIRST_DIRECTION[field] },
  });
  const setPage = (next) => setView((v) => ({ ...v, page: next }));

  const exportCsv = async () => {
    setExporting(true);
    try {
      await downloadStudentsCsv({ search, ordering, level, status, ...filters });
    } catch {
      // A failed download has nothing useful to show beyond re-enabling the button.
    } finally {
      setExporting(false);
    }
  };

  const filtersActive = Boolean(level || status || Object.values(filters).some(Boolean));
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
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('students.title')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 20px' }}>{t('students.subtitle')}</p>

      <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap', marginBottom: '20px' }}>
        <StudentFilters options={filterOptions} filters={filters} onChange={updateFilter} />
        <select value={level} onChange={(e) => patch({ level: e.target.value })} style={SELECT_STYLE} aria-label={t('students.levelAll')}>
          <option value="">{t('students.levelAll')}</option>
          {LEVEL_KEYS.map((k) => <option key={k} value={k}>{t(`students.level.${k}`)}</option>)}
        </select>
        <select value={status} onChange={(e) => patch({ status: e.target.value })} style={SELECT_STYLE} aria-label={t('students.statusAll')}>
          <option value="">{t('students.statusAll')}</option>
          {STATUS_KEYS.map((k) => <option key={k} value={k}>{t(`students.status.${k}`)}</option>)}
        </select>
        {filtersActive && (
          <button type="button" onClick={resetFilters} style={{ ...PAGER_BUTTON(false), color: '#BD5B4C' }}>{t('admin.resetFilters')}</button>
        )}
      </div>

      <div style={{ ...CARD, padding: '22px 26px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', marginBottom: '16px' }}>
          <span style={{ fontSize: '13px', fontWeight: 700, color: '#161F24' }}>{t('admin.totalStudents')(students.total)}</span>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
            <button type="button" onClick={exportCsv} disabled={exporting || students.total === 0} style={PAGER_BUTTON(exporting || students.total === 0)}>{t('admin.exportCsv')}</button>
            <input
              value={search}
              onChange={(e) => patch({ search: e.target.value })}
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
          <div style={{ minWidth: '820px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: TABLE_COLUMNS, gap: '10px', padding: '0 6px 10px', fontSize: '11.5px', fontWeight: 700, color: '#939EA3', borderBottom: '1px solid rgba(31,55,75,0.08)' }}>
              {sortHeader('name', t('admin.tableStudent'))}
              <span>{t('admin.tableGroup')}</span>
              {sortHeader('score', t('admin.tableScore'))}
              <span>{t('admin.tableLevel')}</span>
              {sortHeader('progress', t('students.tableProgress'))}
              {sortHeader('status', t('admin.tableStatus'))}
              {sortHeader('date', t('admin.tableDate'))}
            </div>
            {students.results.map((s) => (
              <div
                key={s.id} role="button" tabIndex={0}
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
                <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ flex: 1, maxWidth: '64px', height: '6px', borderRadius: '100px', background: '#EAF2F5', overflow: 'hidden' }}>
                    <span style={{ display: 'block', height: '100%', width: `${(100 * s.progress) / s.progressTotal}%`, background: '#2E5570', borderRadius: '100px' }} />
                  </span>
                  <span style={{ fontSize: '12px', color: '#556269' }}>{s.progress} / {s.progressTotal}</span>
                </span>
                <span><span style={{ fontSize: '11px', fontWeight: 700, padding: '3px 10px', borderRadius: '100px', background: s.statusBg, color: s.statusColor }}>{s.statusLabel}</span></span>
                <span style={{ color: '#939EA3' }}>{s.date ?? '—'}</span>
              </div>
            ))}
          </div>
        </div>
        {loaded && students.results.length === 0 && (
          <div style={{ padding: '40px 0', textAlign: 'center', color: '#939EA3', fontSize: '13px' }}>{t('admin.noMatch')(search)}</div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginTop: '16px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12.5px', color: '#939EA3' }}>
            {t('students.perPage')}
            <select value={pageSize} onChange={(e) => patch({ pageSize: Number(e.target.value) })} style={SELECT_STYLE}>
              {PAGE_SIZES.map((n) => <option key={n} value={n}>{n}</option>)}
            </select>
          </label>
          {pageCount > 1 && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ fontSize: '12.5px', color: '#939EA3' }}>{t('admin.pageInfo')(students.page, pageCount)}</span>
              <button type="button" disabled={students.page <= 1} onClick={() => setPage(students.page - 1)} style={PAGER_BUTTON(students.page <= 1)}>{t('admin.pagePrev')}</button>
              <button type="button" disabled={students.page >= pageCount} onClick={() => setPage(students.page + 1)} style={PAGER_BUTTON(students.page >= pageCount)}>{t('admin.pageNext')}</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
