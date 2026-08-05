import { useEffect, useState } from 'react';

import {
  createLikertItem, createMcqQuestion, deleteLikertItem, deleteMcqQuestion,
  getQuestionBank, updateLikertItem, updateMcqQuestion,
} from '../../api/admin.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

const SHIMMER = {
  background: 'linear-gradient(90deg,#EDF2F3 0%,#F7F9FA 50%,#EDF2F3 100%)',
  backgroundSize: '800px 100%', animation: 'mm-shimmer 1.4s infinite linear',
};

const CARD = { borderRadius: '18px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)', overflow: 'hidden' };

const FIELD_LABEL = { fontSize: '10.5px', fontWeight: 700, color: '#939EA3', letterSpacing: '0.03em', marginBottom: '4px', display: 'block' };
const INPUT = {
  width: '100%', padding: '8px 10px', borderRadius: '8px', border: '1px solid rgba(31,55,75,0.18)',
  fontFamily: 'Manrope', fontSize: '12.5px', background: '#fff', outline: 'none', boxSizing: 'border-box',
};
const PILL_BTN = { fontSize: '11px', fontWeight: 700, border: 'none', borderRadius: '100px', padding: '4px 12px', cursor: 'pointer' };

const emptyMcqDraft = () => ({
  questionType: 'single',
  categoryRu: '', categoryUz: '',
  promptRu: '', promptUz: '',
  optionsRu: ['', ''], optionsUz: ['', ''],
  correctIndices: [],
  difficulty: '0',
});
const emptyLikertDraft = () => ({ textRu: '', textUz: '', reverseScored: false });

/**
 * Admin-only view over every indicator's full question/answer bank, with
 * inline editing, creation, and deletion — replaces the old static
 * design-system reference screen.
 */
export default function QuestionBank() {
  const [loading, setLoading] = useState(true);
  const [groups, setGroups] = useState([]);
  const [openKey, setOpenKey] = useState(null);

  const [editing, setEditing] = useState(null); // { groupKey, id }
  const [draft, setDraft] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);

  const [creatingGroupKey, setCreatingGroupKey] = useState(null);
  const [newDraft, setNewDraft] = useState(null);
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState(null);

  const [confirmingDelete, setConfirmingDelete] = useState(null); // `${groupKey}-${id}`
  const [deleting, setDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState(null); // { key, message }

  const { t, language } = useLanguage();

  useEffect(() => {
    setLoading(true);
    getQuestionBank().then((data) => {
      setGroups(data);
      setLoading(false);
    });
  }, [language]);

  function startEdit(group, q) {
    setSaveError(null);
    setEditing({ groupKey: group.key, id: q.id });
    if (group.type === 'mcq') {
      setDraft({
        categoryRu: q.categoryRu, categoryUz: q.categoryUz,
        promptRu: q.promptRu, promptUz: q.promptUz,
        optionsRu: [...q.optionsRu], optionsUz: [...q.optionsUz],
        correctIndices: [...q.correctIndices],
        difficulty: String(q.difficulty),
      });
    } else {
      setDraft({ textRu: q.textRu, textUz: q.textUz, reverseScored: q.reverseScored });
    }
  }

  function cancelEdit() {
    setEditing(null);
    setDraft(null);
    setSaveError(null);
  }

  function setOptionText(lang, index, value) {
    setDraft((prev) => {
      const key = lang === 'ru' ? 'optionsRu' : 'optionsUz';
      const next = [...prev[key]];
      next[index] = value;
      return { ...prev, [key]: next };
    });
  }

  function toggleCorrect(questionType, index) {
    setDraft((prev) => {
      if (questionType === 'single') return { ...prev, correctIndices: [index] };
      const has = prev.correctIndices.includes(index);
      const next = has ? prev.correctIndices.filter((i) => i !== index) : [...prev.correctIndices, index].sort((a, b) => a - b);
      return { ...prev, correctIndices: next };
    });
  }

  async function saveEdit(group, q) {
    setSaving(true);
    setSaveError(null);
    try {
      let updated;
      if (group.type === 'mcq') {
        updated = await updateMcqQuestion(q.id, {
          category_ru: draft.categoryRu, category_uz: draft.categoryUz,
          prompt_ru: draft.promptRu, prompt_uz: draft.promptUz,
          options_ru: draft.optionsRu, options_uz: draft.optionsUz,
          correct_indices: draft.correctIndices,
          difficulty: Number(draft.difficulty) || 0,
        });
      } else {
        updated = await updateLikertItem(q.id, {
          text_ru: draft.textRu, text_uz: draft.textUz, reverse_scored: draft.reverseScored,
        });
      }
      setGroups((prev) => prev.map((g) => (
        g.key !== group.key ? g : { ...g, questions: g.questions.map((row) => (row.id === q.id ? updated : row)) }
      )));
      setEditing(null);
      setDraft(null);
    } catch (err) {
      setSaveError(err.message || t('questionBank.saveError'));
    } finally {
      setSaving(false);
    }
  }

  function startCreate(group) {
    setCreateError(null);
    setCreatingGroupKey(group.key);
    setNewDraft(group.type === 'mcq' ? emptyMcqDraft() : emptyLikertDraft());
  }

  function cancelCreate() {
    setCreatingGroupKey(null);
    setNewDraft(null);
    setCreateError(null);
  }

  function addNewOption() {
    setNewDraft((p) => ({ ...p, optionsRu: [...p.optionsRu, ''], optionsUz: [...p.optionsUz, ''] }));
  }

  function removeNewOption(index) {
    setNewDraft((p) => ({
      ...p,
      optionsRu: p.optionsRu.filter((_, i) => i !== index),
      optionsUz: p.optionsUz.filter((_, i) => i !== index),
      correctIndices: p.correctIndices.filter((i) => i !== index).map((i) => (i > index ? i - 1 : i)),
    }));
  }

  function setNewOptionText(lang, index, value) {
    setNewDraft((p) => {
      const key = lang === 'ru' ? 'optionsRu' : 'optionsUz';
      const next = [...p[key]];
      next[index] = value;
      return { ...p, [key]: next };
    });
  }

  function toggleNewCorrect(index) {
    setNewDraft((p) => {
      if (p.questionType === 'single') return { ...p, correctIndices: [index] };
      const has = p.correctIndices.includes(index);
      const next = has ? p.correctIndices.filter((i) => i !== index) : [...p.correctIndices, index].sort((a, b) => a - b);
      return { ...p, correctIndices: next };
    });
  }

  function setNewQuestionType(type) {
    setNewDraft((p) => {
      if (type === 'essay') return { ...p, questionType: type, optionsRu: [], optionsUz: [], correctIndices: [] };
      const optionsRu = p.optionsRu.length ? p.optionsRu : ['', ''];
      const optionsUz = p.optionsUz.length ? p.optionsUz : ['', ''];
      return { ...p, questionType: type, optionsRu, optionsUz };
    });
  }

  async function submitCreate(group) {
    setCreating(true);
    setCreateError(null);
    try {
      let created;
      if (group.type === 'mcq') {
        created = await createMcqQuestion({
          indicator_key: group.key,
          category_ru: newDraft.categoryRu, category_uz: newDraft.categoryUz,
          question_type: newDraft.questionType,
          prompt_ru: newDraft.promptRu, prompt_uz: newDraft.promptUz,
          options_ru: newDraft.optionsRu, options_uz: newDraft.optionsUz,
          correct_indices: newDraft.correctIndices,
          difficulty: Number(newDraft.difficulty) || 0,
        });
      } else {
        created = await createLikertItem({
          indicator_key: group.key,
          text_ru: newDraft.textRu, text_uz: newDraft.textUz, reverse_scored: newDraft.reverseScored,
        });
      }
      setGroups((prev) => prev.map((g) => (
        g.key !== group.key ? g : { ...g, questions: [...g.questions, created], questionCount: g.questionCount + 1 }
      )));
      setCreatingGroupKey(null);
      setNewDraft(null);
    } catch (err) {
      setCreateError(err.message || t('questionBank.createError'));
    } finally {
      setCreating(false);
    }
  }

  async function performDelete(group, q) {
    setDeleting(true);
    setDeleteError(null);
    try {
      if (group.type === 'mcq') await deleteMcqQuestion(q.id);
      else await deleteLikertItem(q.id);
      setGroups((prev) => prev.map((g) => (
        g.key !== group.key ? g : { ...g, questions: g.questions.filter((row) => row.id !== q.id), questionCount: g.questionCount - 1 }
      )));
      setConfirmingDelete(null);
    } catch (err) {
      setDeleteError({ key: `${group.key}-${q.id}`, message: err.message || t('questionBank.deleteError') });
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both', maxWidth: '960px' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('questionBank.title')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 28px' }}>{t('questionBank.subtitle')}</p>

      {loading ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {[1, 2, 3, 4].map((i) => <div key={i} style={{ height: '64px', borderRadius: '18px', ...SHIMMER }} />)}
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {groups.map((g) => {
            const open = openKey === g.key;
            return (
              <div key={g.key} style={CARD}>
                <button
                  className="mm-btn"
                  onClick={() => setOpenKey(open ? null : g.key)}
                  style={{
                    width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    padding: '18px 22px', background: 'none', border: 'none', cursor: 'pointer', textAlign: 'left',
                  }}
                >
                  <div>
                    <div style={{ fontSize: '15px', fontWeight: 700, color: '#161F24' }}>{g.label}</div>
                    <div style={{ fontSize: '12px', color: '#939EA3', marginTop: '2px' }}>
                      {g.type === 'mcq' ? t('questionBank.typeMcq') : t('questionBank.typeLikert')} · {t('questionBank.questionCount')(g.questionCount)}
                    </div>
                  </div>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#556269" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                    style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.15s ease', flexShrink: 0 }}>
                    <path d="M6 9l6 6 6-6" />
                  </svg>
                </button>

                {open && (
                  <div style={{ padding: '0 22px 20px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {g.questions.length === 0 && creatingGroupKey !== g.key && (
                      <div style={{ padding: '20px 0', textAlign: 'center', color: '#939EA3', fontSize: '13px' }}>{t('questionBank.empty')}</div>
                    )}
                    {g.questions.map((q, i) => {
                      const isEditing = editing && editing.groupKey === g.key && editing.id === q.id;
                      const rowKey = `${g.key}-${q.id}`;
                      const isConfirmingDelete = confirmingDelete === rowKey;
                      return (
                        <div key={q.id} style={{ padding: '16px 18px', borderRadius: '14px', background: 'rgba(255,255,255,0.55)', border: '1px solid rgba(31,55,75,0.08)' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px', marginBottom: '8px' }}>
                            <span style={{ fontSize: '11.5px', fontWeight: 700, color: '#939EA3' }}>
                              #{i + 1}{g.type === 'mcq' && q.category ? ` · ${q.category}` : ''}
                            </span>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                              {g.type === 'mcq' && !isEditing && (
                                <span style={{ fontSize: '10.5px', fontWeight: 700, color: '#3E7EA6' }}>{t('questionBank.difficultyLabel')}: {q.difficulty.toFixed(2)}</span>
                              )}
                              {!isEditing && !isConfirmingDelete && (
                                <>
                                  <button className="mm-btn" onClick={() => startEdit(g, q)} style={{ ...PILL_BTN, color: '#2E5570', background: 'rgba(46,85,112,0.1)' }}>
                                    {t('questionBank.edit')}
                                  </button>
                                  <button className="mm-btn" onClick={() => { setConfirmingDelete(rowKey); setDeleteError(null); }} style={{ ...PILL_BTN, color: '#BD5B4C', background: 'rgba(189,91,76,0.1)' }}>
                                    {t('questionBank.delete')}
                                  </button>
                                </>
                              )}
                              {isConfirmingDelete && (
                                <>
                                  <span style={{ fontSize: '11px', fontWeight: 700, color: '#BD5B4C' }}>{t('questionBank.deleteConfirm')}</span>
                                  <button className="mm-btn" disabled={deleting} onClick={() => performDelete(g, q)} style={{ ...PILL_BTN, color: '#fff', background: '#BD5B4C' }}>
                                    {deleting ? t('questionBank.deleting') : t('questionBank.deleteConfirmYes')}
                                  </button>
                                  <button className="mm-btn" disabled={deleting} onClick={() => setConfirmingDelete(null)} style={{ ...PILL_BTN, color: '#556269', background: 'rgba(31,55,75,0.06)' }}>
                                    {t('questionBank.deleteConfirmNo')}
                                  </button>
                                </>
                              )}
                            </div>
                          </div>

                          {deleteError && deleteError.key === rowKey && (
                            <div style={{ fontSize: '11.5px', color: '#BD5B4C', fontWeight: 600, marginBottom: '8px' }}>{deleteError.message}</div>
                          )}

                          {!isEditing && (
                            <>
                              <div style={{ fontSize: '13.5px', color: '#161F24', fontWeight: 600, marginBottom: g.type === 'mcq' && q.type !== 'essay' ? '10px' : 0 }}>
                                {q.prompt}
                              </div>

                              {g.type === 'mcq' && q.type === 'essay' && (
                                <div style={{ fontSize: '12px', color: '#939EA3', fontStyle: 'italic' }}>{t('questionBank.essayNote')}</div>
                              )}

                              {g.type === 'mcq' && q.type !== 'essay' && (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                                  {q.options.map((opt, oi) => {
                                    const correct = q.correctIndices.includes(oi);
                                    return (
                                      <div key={oi} style={{
                                        display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '8px',
                                        padding: '7px 10px', borderRadius: '8px', background: correct ? '#DCEFE2' : 'rgba(31,55,75,0.04)',
                                      }}>
                                        <span style={{ fontSize: '12.5px', color: correct ? '#1F4B39' : '#3B444A', fontWeight: correct ? 700 : 400 }}>{opt}</span>
                                        {correct && <span style={{ fontSize: '10px', fontWeight: 700, color: '#1F4B39', flexShrink: 0 }}>✓ {t('questionBank.correctAnswerBadge')}</span>}
                                      </div>
                                    );
                                  })}
                                </div>
                              )}

                              {g.type === 'likert' && (
                                <div style={{ fontSize: '11.5px', color: '#939EA3' }}>
                                  {t('questionBank.likertScaleNote')}
                                  {q.reverseScored && <span style={{ marginLeft: '8px', fontWeight: 700, color: '#B8862F' }}>· {t('questionBank.reverseScoredBadge')}</span>}
                                </div>
                              )}
                            </>
                          )}

                          {isEditing && g.type === 'mcq' && (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                                <div>
                                  <label style={FIELD_LABEL}>{t('questionBank.categoryRuLabel')}</label>
                                  <input style={INPUT} value={draft.categoryRu} onChange={(e) => setDraft((p) => ({ ...p, categoryRu: e.target.value }))} />
                                </div>
                                <div>
                                  <label style={FIELD_LABEL}>{t('questionBank.categoryUzLabel')}</label>
                                  <input style={INPUT} value={draft.categoryUz} onChange={(e) => setDraft((p) => ({ ...p, categoryUz: e.target.value }))} />
                                </div>
                              </div>
                              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                                <div>
                                  <label style={FIELD_LABEL}>{t('questionBank.promptRuLabel')}</label>
                                  <textarea rows={2} style={{ ...INPUT, resize: 'vertical' }} value={draft.promptRu} onChange={(e) => setDraft((p) => ({ ...p, promptRu: e.target.value }))} />
                                </div>
                                <div>
                                  <label style={FIELD_LABEL}>{t('questionBank.promptUzLabel')}</label>
                                  <textarea rows={2} style={{ ...INPUT, resize: 'vertical' }} value={draft.promptUz} onChange={(e) => setDraft((p) => ({ ...p, promptUz: e.target.value }))} />
                                </div>
                              </div>

                              {q.type !== 'essay' && (
                                <div style={{ overflowX: 'auto' }}>
                                  <div style={{ display: 'grid', gridTemplateColumns: '28px 1fr 1fr', gap: '8px', marginBottom: '4px', minWidth: '320px' }}>
                                    <span />
                                    <label style={FIELD_LABEL}>{t('questionBank.optionsRuLabel')}</label>
                                    <label style={FIELD_LABEL}>{t('questionBank.optionsUzLabel')}</label>
                                  </div>
                                  {draft.optionsRu.map((_, oi) => (
                                    <div key={oi} style={{ display: 'grid', gridTemplateColumns: '28px 1fr 1fr', gap: '8px', marginBottom: '6px', alignItems: 'center', minWidth: '320px' }}>
                                      <input
                                        type={q.type === 'multi' ? 'checkbox' : 'radio'}
                                        checked={draft.correctIndices.includes(oi)}
                                        onChange={() => toggleCorrect(q.type, oi)}
                                        title={t('questionBank.correctColumnLabel')}
                                      />
                                      <input style={INPUT} value={draft.optionsRu[oi]} onChange={(e) => setOptionText('ru', oi, e.target.value)} />
                                      <input style={INPUT} value={draft.optionsUz[oi]} onChange={(e) => setOptionText('uz', oi, e.target.value)} />
                                    </div>
                                  ))}
                                </div>
                              )}

                              <div style={{ maxWidth: '160px' }}>
                                <label style={FIELD_LABEL}>{t('questionBank.difficultyLabel')}</label>
                                <input type="number" step="0.05" style={INPUT} value={draft.difficulty} onChange={(e) => setDraft((p) => ({ ...p, difficulty: e.target.value }))} />
                              </div>
                            </div>
                          )}

                          {isEditing && g.type === 'likert' && (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                                <div>
                                  <label style={FIELD_LABEL}>{t('questionBank.promptRuLabel')}</label>
                                  <textarea rows={2} style={{ ...INPUT, resize: 'vertical' }} value={draft.textRu} onChange={(e) => setDraft((p) => ({ ...p, textRu: e.target.value }))} />
                                </div>
                                <div>
                                  <label style={FIELD_LABEL}>{t('questionBank.promptUzLabel')}</label>
                                  <textarea rows={2} style={{ ...INPUT, resize: 'vertical' }} value={draft.textUz} onChange={(e) => setDraft((p) => ({ ...p, textUz: e.target.value }))} />
                                </div>
                              </div>
                              <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: '#3B444A', cursor: 'pointer' }}>
                                <input type="checkbox" checked={draft.reverseScored} onChange={(e) => setDraft((p) => ({ ...p, reverseScored: e.target.checked }))} />
                                {t('questionBank.reverseScoredToggle')}
                              </label>
                            </div>
                          )}

                          {isEditing && (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '12px' }}>
                              <button className="mm-btn" disabled={saving} onClick={() => saveEdit(g, q)} style={{
                                fontSize: '12px', fontWeight: 700, color: '#fff', background: '#2E5570',
                                border: 'none', borderRadius: '100px', padding: '8px 18px', cursor: 'pointer',
                              }}>{saving ? t('questionBank.saving') : t('questionBank.save')}</button>
                              <button className="mm-btn" disabled={saving} onClick={cancelEdit} style={{
                                fontSize: '12px', fontWeight: 600, color: '#556269', background: 'rgba(31,55,75,0.06)',
                                border: 'none', borderRadius: '100px', padding: '8px 18px', cursor: 'pointer',
                              }}>{t('questionBank.cancel')}</button>
                              {saveError && <span style={{ fontSize: '11.5px', color: '#BD5B4C', fontWeight: 600 }}>{saveError}</span>}
                            </div>
                          )}
                        </div>
                      );
                    })}

                    {creatingGroupKey === g.key ? (
                      <div style={{ padding: '16px 18px', borderRadius: '14px', background: 'rgba(46,85,112,0.06)', border: '1px dashed rgba(46,85,112,0.35)' }}>
                        {g.type === 'mcq' ? (
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                            <div>
                              <label style={FIELD_LABEL}>{t('questionBank.questionTypeLabel')}</label>
                              <select style={{ ...INPUT, maxWidth: '260px' }} value={newDraft.questionType} onChange={(e) => setNewQuestionType(e.target.value)}>
                                <option value="single">{t('questionBank.typeSingleOption')}</option>
                                <option value="multi">{t('questionBank.typeMultiOption')}</option>
                                <option value="essay">{t('questionBank.typeEssayOption')}</option>
                              </select>
                            </div>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                              <div>
                                <label style={FIELD_LABEL}>{t('questionBank.categoryRuLabel')}</label>
                                <input style={INPUT} value={newDraft.categoryRu} onChange={(e) => setNewDraft((p) => ({ ...p, categoryRu: e.target.value }))} />
                              </div>
                              <div>
                                <label style={FIELD_LABEL}>{t('questionBank.categoryUzLabel')}</label>
                                <input style={INPUT} value={newDraft.categoryUz} onChange={(e) => setNewDraft((p) => ({ ...p, categoryUz: e.target.value }))} />
                              </div>
                            </div>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                              <div>
                                <label style={FIELD_LABEL}>{t('questionBank.promptRuLabel')}</label>
                                <textarea rows={2} style={{ ...INPUT, resize: 'vertical' }} value={newDraft.promptRu} onChange={(e) => setNewDraft((p) => ({ ...p, promptRu: e.target.value }))} />
                              </div>
                              <div>
                                <label style={FIELD_LABEL}>{t('questionBank.promptUzLabel')}</label>
                                <textarea rows={2} style={{ ...INPUT, resize: 'vertical' }} value={newDraft.promptUz} onChange={(e) => setNewDraft((p) => ({ ...p, promptUz: e.target.value }))} />
                              </div>
                            </div>

                            {newDraft.questionType !== 'essay' && (
                              <div style={{ overflowX: 'auto' }}>
                                <div style={{ display: 'grid', gridTemplateColumns: '28px 1fr 1fr 28px', gap: '8px', marginBottom: '4px', minWidth: '340px' }}>
                                  <span />
                                  <label style={FIELD_LABEL}>{t('questionBank.optionsRuLabel')}</label>
                                  <label style={FIELD_LABEL}>{t('questionBank.optionsUzLabel')}</label>
                                  <span />
                                </div>
                                {newDraft.optionsRu.map((_, oi) => (
                                  <div key={oi} style={{ display: 'grid', gridTemplateColumns: '28px 1fr 1fr 28px', gap: '8px', marginBottom: '6px', alignItems: 'center', minWidth: '340px' }}>
                                    <input
                                      type={newDraft.questionType === 'multi' ? 'checkbox' : 'radio'}
                                      checked={newDraft.correctIndices.includes(oi)}
                                      onChange={() => toggleNewCorrect(oi)}
                                      title={t('questionBank.correctColumnLabel')}
                                    />
                                    <input style={INPUT} value={newDraft.optionsRu[oi]} onChange={(e) => setNewOptionText('ru', oi, e.target.value)} />
                                    <input style={INPUT} value={newDraft.optionsUz[oi]} onChange={(e) => setNewOptionText('uz', oi, e.target.value)} />
                                    <button
                                      className="mm-btn" type="button" title={t('questionBank.removeOptionLabel')}
                                      onClick={() => removeNewOption(oi)}
                                      disabled={newDraft.optionsRu.length <= 2}
                                      style={{ border: 'none', background: 'none', color: newDraft.optionsRu.length <= 2 ? '#C7CFCD' : '#BD5B4C', cursor: newDraft.optionsRu.length <= 2 ? 'not-allowed' : 'pointer', fontSize: '16px', lineHeight: 1 }}
                                    >×</button>
                                  </div>
                                ))}
                                <button className="mm-btn" type="button" onClick={addNewOption} style={{ fontSize: '11.5px', fontWeight: 700, color: '#2E5570', background: 'none', border: 'none', cursor: 'pointer', padding: 0, marginTop: '2px' }}>
                                  {t('questionBank.addOption')}
                                </button>
                              </div>
                            )}

                            <div style={{ maxWidth: '160px' }}>
                              <label style={FIELD_LABEL}>{t('questionBank.difficultyLabel')}</label>
                              <input type="number" step="0.05" style={INPUT} value={newDraft.difficulty} onChange={(e) => setNewDraft((p) => ({ ...p, difficulty: e.target.value }))} />
                            </div>
                          </div>
                        ) : (
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                              <div>
                                <label style={FIELD_LABEL}>{t('questionBank.promptRuLabel')}</label>
                                <textarea rows={2} style={{ ...INPUT, resize: 'vertical' }} value={newDraft.textRu} onChange={(e) => setNewDraft((p) => ({ ...p, textRu: e.target.value }))} />
                              </div>
                              <div>
                                <label style={FIELD_LABEL}>{t('questionBank.promptUzLabel')}</label>
                                <textarea rows={2} style={{ ...INPUT, resize: 'vertical' }} value={newDraft.textUz} onChange={(e) => setNewDraft((p) => ({ ...p, textUz: e.target.value }))} />
                              </div>
                            </div>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: '#3B444A', cursor: 'pointer' }}>
                              <input type="checkbox" checked={newDraft.reverseScored} onChange={(e) => setNewDraft((p) => ({ ...p, reverseScored: e.target.checked }))} />
                              {t('questionBank.reverseScoredToggle')}
                            </label>
                          </div>
                        )}

                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '12px' }}>
                          <button className="mm-btn" disabled={creating} onClick={() => submitCreate(g)} style={{
                            fontSize: '12px', fontWeight: 700, color: '#fff', background: '#2E5570',
                            border: 'none', borderRadius: '100px', padding: '8px 18px', cursor: 'pointer',
                          }}>{creating ? t('questionBank.creating') : t('questionBank.create')}</button>
                          <button className="mm-btn" disabled={creating} onClick={cancelCreate} style={{
                            fontSize: '12px', fontWeight: 600, color: '#556269', background: 'rgba(31,55,75,0.06)',
                            border: 'none', borderRadius: '100px', padding: '8px 18px', cursor: 'pointer',
                          }}>{t('questionBank.cancel')}</button>
                          {createError && <span style={{ fontSize: '11.5px', color: '#BD5B4C', fontWeight: 600 }}>{createError}</span>}
                        </div>
                      </div>
                    ) : (
                      <button className="mm-btn" onClick={() => startCreate(g)} style={{
                        alignSelf: 'flex-start', fontSize: '12.5px', fontWeight: 700, color: '#2E5570', background: 'rgba(46,85,112,0.1)',
                        border: 'none', borderRadius: '100px', padding: '9px 16px', cursor: 'pointer',
                      }}>{t('questionBank.addQuestion')}</button>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
