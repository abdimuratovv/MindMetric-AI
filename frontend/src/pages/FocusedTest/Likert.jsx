import { useEffect, useState } from 'react';

import {
  answerLikert, getLikertItems, startLikert, submitLikert as apiSubmitLikert,
} from '../../api/assessments.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import CompletionOverlay from './CompletionOverlay.jsx';

/**
 * Generalized self-report screen shared by the three Likert-pattern
 * indicators (teamwork, patience, learning_speed). Each attempt is scoped to
 * exactly one BehavioralCategory, so `groups` is a 1-element array from the
 * backend — this component doesn't need to know that, it just maps over
 * whatever it's given.
 */
export default function Likert({ assessmentType, goTo, onProgress }) {
  const [groups, setGroups] = useState([]); // [{id, key, label, items: [{id, text}]}]
  const [answers, setAnswers] = useState({}); // { [itemId]: value(0-4) }
  const [error, setError] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [completion, setCompletion] = useState(null);
  const { t } = useLanguage();
  const SCALE_LABELS = t('likert.scale').map((title, i) => ({ short: String(i + 1), title }));
  const meta = t('assessmentsMeta.' + assessmentType);

  useEffect(() => {
    (async () => {
      await startLikert(assessmentType);
      setGroups(await getLikertItems(assessmentType));
    })();
  }, [assessmentType]);

  const totalItems = groups.reduce((n, g) => n + g.items.length, 0);
  useEffect(() => {
    onProgress({ pct: totalItems ? `${Math.round((Object.keys(answers).length / totalItems) * 100)}%` : '0%', timeRemainingSeconds: null });
  }, [answers, totalItems]); // eslint-disable-line react-hooks/exhaustive-deps

  const setAnswer = async (itemId, value) => {
    setAnswers((a) => ({ ...a, [itemId]: value }));
    setError(false);
    await answerLikert(assessmentType, itemId, value + 1); // scale_value is 1-5 server-side, value is 0-4 index
  };

  const submit = async () => {
    if (Object.keys(answers).length < totalItems) {
      setError(true);
      return;
    }
    setIsSubmitting(true);
    try {
      const result = await apiSubmitLikert(assessmentType);
      setCompletion(result);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (completion) {
    return (
      <CompletionOverlay
        indicatorKey={assessmentType}
        score={completion.score}
        achievement={completion.achievement}
        onContinue={() => goTo('selection')}
      />
    );
  }

  return (
    <div style={{ flex: 1, display: 'flex', justifyContent: 'center', padding: '40px 24px 60px' }}>
      <div style={{ width: '680px' }}>
        <h2 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '28px', color: '#161F24', margin: '0 0 8px' }}>
          {meta.title}
        </h2>
        <p style={{ fontSize: '13.5px', color: '#556269', margin: '0 0 26px' }}>
          {t('likert.subtitle')}
        </p>

        {error && (
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', padding: '12px 16px', borderRadius: '12px', background: '#F6E0DC', color: '#BD5B4C', fontSize: '13px', fontWeight: 600, marginBottom: '18px' }}>
            <span>⚠</span><span>{t('likert.errorAllRequired')}</span>
          </div>
        )}

        {groups.map((g) => (
          <div key={g.id} style={{ marginBottom: '26px' }}>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#2E5570', letterSpacing: '0.04em', marginBottom: '12px' }}>{g.label}</div>
            {g.items.map((it) => {
              const chosen = answers[it.id];
              return (
                <div key={it.id} style={{ padding: '18px 22px', borderRadius: '16px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', marginBottom: '10px' }}>
                  <div style={{ fontSize: '14px', color: '#161F24', fontWeight: 600, marginBottom: '12px' }}>{it.text}</div>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    {SCALE_LABELS.map((sc, vi) => (
                      <button key={vi} className="mm-btn" onClick={() => setAnswer(it.id, vi)} title={sc.title} style={{
                        flex: 1, padding: '9px 4px', borderRadius: '9px', cursor: 'pointer', fontSize: '11.5px', fontWeight: 700,
                        border: `1.5px solid ${chosen === vi ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
                        background: chosen === vi ? '#2E5570' : 'rgba(255,255,255,0.5)',
                        color: chosen === vi ? '#fff' : '#556269',
                      }}>{sc.short}</button>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        ))}

        <button
          className="mm-btn"
          disabled={isSubmitting}
          onClick={submit}
          style={{
            width: '100%', padding: '14px 0', borderRadius: '100px', border: 'none', cursor: 'pointer',
            background: '#2E5570', color: '#fff', fontWeight: 700, fontSize: '14.5px',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
          }}>
          {isSubmitting && <span className="mm-spinner" />}
          {t('likert.submit')}
        </button>
      </div>
    </div>
  );
}
