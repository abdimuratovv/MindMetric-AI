import { useEffect, useState } from 'react';

import { getAdminStudentDetail } from '../../api/admin.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import ResultsReport from './ResultsReport.jsx';

const CARD = {
  padding: '22px 26px', borderRadius: '22px', background: 'rgba(255,255,255,0.62)', border: '1px solid rgba(255,255,255,0.85)',
  backdropFilter: 'blur(16px)', boxShadow: '0 10px 30px rgba(31,55,75,0.06)', marginBottom: '22px',
};

/** Admin view of a single student: profile + review state, then the same report the student sees. */
export default function AdminStudentDetail({ studentId, onBack }) {
  const { t, language } = useLanguage();
  const [detail, setDetail] = useState(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setFailed(false);
    getAdminStudentDetail(studentId)
      .then((data) => { if (!cancelled) setDetail(data); })
      .catch(() => { if (!cancelled) setFailed(true); });
    return () => { cancelled = true; };
  }, [studentId, language]);

  const backButton = (
    <button className="mm-btn" onClick={onBack} style={{ border: 'none', background: 'none', color: '#2E5570', fontWeight: 700, fontSize: '13px', cursor: 'pointer', padding: 0, marginBottom: '14px' }}>
      {t('adminStudent.back')}
    </button>
  );

  if (failed) {
    return <div>{backButton}<p style={{ fontSize: '14px', color: '#BD5B4C' }}>{t('adminStudent.loadError')}</p></div>;
  }
  if (!detail) return <div>{backButton}</div>;

  const { student, review, summary, mistakes } = detail;
  const facts = [
    ['faculty', student.faculty], ['course', student.course], ['group', student.group],
    ['specialization', student.specialization], ['email', student.email], ['lastActivity', student.lastActivity],
  ].filter(([, value]) => value);

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      {backButton}
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{student.name}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 24px' }}>{student.program}</p>

      <div style={CARD}>
        <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#161F24', margin: '0 0 14px' }}>{t('adminStudent.profileTitle')}</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '14px 24px' }}>
          {facts.map(([key, value]) => (
            <div key={key}>
              <div style={{ fontSize: '11.5px', fontWeight: 700, color: '#939EA3', marginBottom: '3px' }}>{t(`adminStudent.${key}`)}</div>
              <div style={{ fontSize: '13.5px', fontWeight: 600, color: '#161F24', wordBreak: 'break-word' }}>{value}</div>
            </div>
          ))}
        </div>
      </div>

      <div style={CARD}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap', marginBottom: '12px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#161F24', margin: 0 }}>{t('adminStudent.reviewTitle')}</h3>
          <span style={{ fontSize: '11px', fontWeight: 700, padding: '3px 10px', borderRadius: '100px', background: review.statusBg, color: review.statusColor }}>{review.statusLabel}</span>
        </div>
        {(review.reviewerName || review.submittedAt) && (
          <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', fontSize: '12.5px', color: '#556269', marginBottom: '12px' }}>
            {review.reviewerName && <span>{t('adminStudent.reviewer')}: <strong>{review.reviewerName}</strong></span>}
            {review.submittedAt && <span>{t('adminStudent.reviewedOn')}: <strong>{review.submittedAt}</strong></span>}
          </div>
        )}
        {review.comment
          ? <p style={{ fontSize: '13.5px', lineHeight: 1.6, color: '#3B444A', margin: 0, whiteSpace: 'pre-wrap' }}>{review.comment}</p>
          : <p style={{ fontSize: '13px', color: '#939EA3', fontStyle: 'italic', margin: 0 }}>{t('adminStudent.noComment')}</p>}
      </div>

      <ResultsReport data={summary} mistakes={mistakes} />
    </div>
  );
}
