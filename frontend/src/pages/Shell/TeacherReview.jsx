import { useEffect, useState } from 'react';

import { getStudentFilterOptions } from '../../api/admin.js';
import { getTeacherStudentDetail, getTeacherStudents, submitReview as apiSubmitReview } from '../../api/teacher.js';
import StudentFilters from '../../components/StudentFilters.jsx';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

const SHIMMER = {
  background: 'linear-gradient(90deg,#EDF2F3 0%,#F7F9FA 50%,#EDF2F3 100%)',
  backgroundSize: '800px 100%', animation: 'mm-shimmer 1.4s infinite linear',
};

/** Ported verbatim from MindMetric AI.dc.html lines 275-370 (`isTeacherReview`). */
export default function TeacherReview() {
  const [loading, setLoading] = useState(true);
  const [teacherSearch, setTeacherSearch] = useState('');
  const [teacherStudents, setTeacherStudents] = useState([]);
  const [selectedStudentId, setSelectedStudentId] = useState(null);
  const [selectedStudent, setSelectedStudent] = useState(null);
  // Keyed by the rubric item's stable `key` (e.g. "code_readability"), not its
  // display label — the label is translated and would change with `language`,
  // which would silently orphan any score already picked under the old text.
  const [rubric, setRubric] = useState({});
  const [reviewComment, setReviewComment] = useState('');
  const [reviewSubmitted, setReviewSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [searchFocused, setSearchFocused] = useState(false);
  const [commentFocused, setCommentFocused] = useState(false);
  const [filters, setFilters] = useState({ faculty: '', course: '', group: '' });
  const [filterOptions, setFilterOptions] = useState({ faculties: [], courses: [], groups: [] });
  const { t, language } = useLanguage();

  useEffect(() => {
    getStudentFilterOptions().then(setFilterOptions);
  }, []);

  useEffect(() => {
    setLoading(true);
    getTeacherStudents(teacherSearch, filters).then((rows) => { setTeacherStudents(rows); setLoading(false); });
  }, [teacherSearch, filters, language]); // eslint-disable-line react-hooks/exhaustive-deps

  const updateFilter = (key, value) => setFilters((f) => ({ ...f, [key]: value }));

  const selectStudent = (id) => {
    setSelectedStudentId(id);
    setReviewComment('');
    setReviewSubmitted(false);
    setRubric({});
    getTeacherStudentDetail(id).then(setSelectedStudent);
  };

  // Re-fetch the open student's detail on a language switch so `rubricLabels`/
  // `indicatorTags` (server-localized) don't stay stuck in the old language.
  useEffect(() => {
    if (selectedStudentId != null) getTeacherStudentDetail(selectedStudentId).then(setSelectedStudent);
  }, [language]); // eslint-disable-line react-hooks/exhaustive-deps

  const submit = async () => {
    setIsSubmitting(true);
    try {
      await apiSubmitReview(selectedStudentId, rubric, reviewComment);
      setReviewSubmitted(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('teacherReview.title')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 22px' }}>{t('teacherReview.subtitle')}</p>

      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
          <div style={{ height: '420px', borderRadius: '20px', ...SHIMMER }} />
          <div style={{ height: '420px', borderRadius: '20px', ...SHIMMER }} />
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', alignItems: 'start' }}>
          <div style={{ borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)', overflow: 'hidden' }}>
            <div style={{ padding: '14px', borderBottom: '1px solid rgba(31,55,75,0.08)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <input
                value={teacherSearch}
                onChange={(e) => setTeacherSearch(e.target.value)}
                onFocus={() => setSearchFocused(true)}
                onBlur={() => setSearchFocused(false)}
                placeholder={t('common.searchStudents')}
                style={{
                  width: '100%', padding: '9px 12px', borderRadius: '10px',
                  border: `1px solid ${searchFocused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
                  boxShadow: searchFocused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
                  transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
                  fontFamily: 'Manrope', fontSize: '13px', outline: 'none', background: 'rgba(255,255,255,0.8)',
                }}
              />
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                <StudentFilters options={filterOptions} filters={filters} onChange={updateFilter} />
              </div>
            </div>
            {teacherStudents.length > 0 ? (
              <div style={{ maxHeight: '520px', overflowY: 'auto' }}>
                {teacherStudents.map((s) => (
                  <button key={s.id} className="mm-btn" onClick={() => selectStudent(s.id)} style={{
                    width: '100%', display: 'flex', alignItems: 'center', gap: '11px', padding: '13px 14px', border: 'none',
                    borderBottom: '1px solid rgba(31,55,75,0.06)', cursor: 'pointer', textAlign: 'left',
                    background: selectedStudentId === s.id ? 'rgba(46,85,112,0.08)' : 'transparent',
                  }}>
                    <div style={{ width: '34px', height: '34px', borderRadius: '50%', background: '#DCECEF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, color: '#1F374B', fontSize: '12px', flexShrink: 0 }}>
                      {s.initials}
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: '13px', fontWeight: 700, color: '#161F24' }}>{s.name}</div>
                      <div style={{ fontSize: '11.5px', color: '#939EA3' }}>{s.program}</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '13.5px', fontWeight: 700, color: '#1F374B' }}>{s.score}</div>
                      <span style={{ fontSize: '10px', fontWeight: 700, padding: '2px 8px', borderRadius: '100px', background: s.statusBg, color: s.statusColor }}>{s.statusLabel}</span>
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <div style={{ padding: '50px 24px', textAlign: 'center' }}>
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#939EA3" strokeWidth="1.5" style={{ marginBottom: '12px' }}>
                  <circle cx="11" cy="11" r="7"></circle><path d="M21 21l-4.3-4.3"></path>
                </svg>
                <div style={{ fontSize: '13.5px', fontWeight: 700, color: '#3B444A', marginBottom: '4px' }}>{t('teacherReview.noMatch')(teacherSearch)}</div>
                <div style={{ fontSize: '12px', color: '#939EA3' }}>{t('teacherReview.tryDifferent')}</div>
              </div>
            )}
          </div>

          {selectedStudent ? (
            <div style={{ borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)', padding: '28px 30px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px', marginBottom: '22px' }}>
                <div>
                  <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#161F24', margin: '0 0 4px' }}>{selectedStudent.name}</h2>
                  <p style={{ fontSize: '13px', color: '#556269', margin: 0 }}>{selectedStudent.program} · {selectedStudent.id}</p>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '38px', color: '#1F374B' }}>{selectedStudent.score}</div>
                  <div style={{ fontSize: '11.5px', color: '#939EA3', fontWeight: 600 }}>{t('teacherReview.automatedScore')}</div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '18px' }}>
                <span style={{ fontSize: '11.5px', fontWeight: 700, color: '#939EA3' }}>{t('teacherReview.recommendedField')}:</span>
                {selectedStudent.fieldRecommendations?.available ? (
                  <span style={{ fontSize: '12.5px', fontWeight: 700, padding: '5px 12px', borderRadius: '100px', background: '#DCECEF', color: '#1F374B' }}>
                    {selectedStudent.fieldRecommendations.fields[0].label} · {selectedStudent.fieldRecommendations.fields[0].score}{t('results.fitScoreSuffix')}
                  </span>
                ) : (
                  <span style={{ fontSize: '12.5px', color: '#939EA3', fontStyle: 'italic' }}>{t('teacherReview.noFieldYet')}</span>
                )}
              </div>

              <div style={{ display: 'flex', gap: '8px', marginBottom: '22px', flexWrap: 'wrap' }}>
                {selectedStudent.indicatorTags.map((tag, i) => (
                  <span key={i} style={tag.completed ? {
                    fontSize: '11.5px', fontWeight: 600, padding: '6px 12px', borderRadius: '100px', background: '#EAF2F5', color: '#2E5570',
                  } : {
                    fontSize: '11.5px', fontWeight: 600, padding: '6px 12px', borderRadius: '100px', background: 'transparent',
                    border: '1px dashed #C3CACC', color: '#939EA3',
                  }}>
                    {tag.label} {tag.completed ? tag.score : '—'}
                  </span>
                ))}
              </div>

              <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#161F24', margin: '0 0 12px' }}>{t('teacherReview.pedagogicalRubric')}</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '20px' }}>
                {selectedStudent.rubricLabels.map((item) => (
                  <div key={item.key}>
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#3B444A', marginBottom: '8px' }}>{item.label}</div>
                    <div style={{ display: 'flex', gap: '6px' }}>
                      {[1, 2, 3, 4, 5].map((v) => (
                        <button key={v} className="mm-btn" onClick={() => setRubric((r) => ({ ...r, [item.key]: v }))} style={{
                          flex: 1, padding: '8px 0', borderRadius: '9px', cursor: 'pointer', fontSize: '12.5px', fontWeight: 700,
                          border: `1px solid ${rubric[item.key] === v ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
                          background: rubric[item.key] === v ? '#2E5570' : 'rgba(255,255,255,0.5)',
                          color: rubric[item.key] === v ? '#fff' : '#556269',
                        }}>{v}</button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#161F24', margin: '0 0 8px' }}>{t('teacherReview.comments')}</h3>
              <textarea
                value={reviewComment}
                onChange={(e) => setReviewComment(e.target.value)}
                onFocus={() => setCommentFocused(true)}
                onBlur={() => setCommentFocused(false)}
                placeholder={t('teacherReview.commentPlaceholder')}
                style={{
                  width: '100%', minHeight: '90px', padding: '12px 14px', borderRadius: '12px',
                  border: `1px solid ${commentFocused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
                  boxShadow: commentFocused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
                  transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
                  fontFamily: 'Manrope', fontSize: '13px', outline: 'none', background: 'rgba(255,255,255,0.8)', resize: 'vertical', marginBottom: '18px',
                }}
              />

              {reviewSubmitted ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 16px', borderRadius: '12px', background: '#DCEFE2', color: '#1F4B39', fontWeight: 700, fontSize: '13px' }}>
                  {t('teacherReview.reviewSubmittedFor')(selectedStudent.name)}
                </div>
              ) : (
                <button
                  className="mm-btn"
                  disabled={isSubmitting}
                  onClick={submit}
                  style={{
                    width: '100%', padding: '13px 0', borderRadius: '100px', border: 'none', cursor: 'pointer',
                    background: '#2E5570', color: '#fff', fontWeight: 700, fontSize: '14px',
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
                  }}>
                  {isSubmitting && <span className="mm-spinner" />}
                  {t('teacherReview.submitReview')}
                </button>
              )}
            </div>
          ) : (
            <div style={{ borderRadius: '20px', background: 'rgba(255,255,255,0.4)', border: '1px dashed rgba(31,55,75,0.2)', padding: '70px 30px', textAlign: 'center' }}>
              <p style={{ fontSize: '14px', color: '#939EA3', margin: 0 }}>{t('teacherReview.selectPrompt')}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
