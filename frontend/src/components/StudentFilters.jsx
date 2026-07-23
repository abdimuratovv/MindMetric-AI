import { useLanguage } from '../i18n/LanguageContext.jsx';

const SELECT_STYLE = {
  padding: '9px 12px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.14)',
  fontSize: '13px', fontFamily: 'Manrope', outline: 'none', background: 'rgba(255,255,255,0.8)', color: '#161F24',
};

/**
 * Faculty/course/group roster filter — shared by AdminOverview and
 * TeacherReview (both list students and both benefit from the same
 * narrowing). Options come from GET /api/admin/student-filter-options/
 * (distinct values already in use, since those fields are free text).
 */
export default function StudentFilters({ options, filters, onChange }) {
  const { t } = useLanguage();

  return (
    <>
      <select value={filters.faculty} onChange={(e) => onChange('faculty', e.target.value)} style={SELECT_STYLE}>
        <option value="">{t('studentFilters.allFaculties')}</option>
        {options.faculties.map((f) => <option key={f} value={f}>{f}</option>)}
      </select>
      <select value={filters.course} onChange={(e) => onChange('course', e.target.value)} style={SELECT_STYLE}>
        <option value="">{t('studentFilters.allCourses')}</option>
        {options.courses.map((c) => <option key={c} value={c}>{c}</option>)}
      </select>
      <select value={filters.group} onChange={(e) => onChange('group', e.target.value)} style={SELECT_STYLE}>
        <option value="">{t('studentFilters.allGroups')}</option>
        {options.groups.map((g) => <option key={g} value={g}>{g}</option>)}
      </select>
    </>
  );
}
