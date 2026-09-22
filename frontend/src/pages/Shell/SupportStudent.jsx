import { useEffect, useState } from 'react';

import {
  createSupportThread,
  getSupportOptions,
  getSupportThread,
  getSupportThreads,
  sendSupportMessage,
} from '../../api/support.js';
import ScreenshotDropzone from '../../components/ScreenshotDropzone.jsx';
import SupportThreadView, { formatStamp } from '../../components/SupportThreadView.jsx';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import { useThreadMessagePolling } from '../../state/useSupportPolling.js';

const PANEL = {
  borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)',
  backdropFilter: 'blur(14px)', overflow: 'hidden',
};
const INPUT_STYLE = {
  width: '100%', boxSizing: 'border-box', padding: '11px 13px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.14)',
  fontSize: '13.5px', fontFamily: 'Manrope', outline: 'none', background: 'rgba(255,255,255,0.85)', color: '#161F24',
};
const LABEL_STYLE = { display: 'block', fontSize: '12px', fontWeight: 700, color: '#556269', marginBottom: '6px' };
const SUBJECT_MAX_LENGTH = 140;
const BODY_MAX_LENGTH = 2000;

const EMPTY_FORM = { category: 'bug', subject: '', body: '', assigneeId: '' };

/**
 * The student's side of the written support channel: their own reports on the
 * left, the open conversation (or the composer for a new one) on the right.
 *
 * Deliberately reachable only from the shell — FocusedTestShell renders outside
 * AppShell (see App.jsx), so a student sitting an assessment can't message an
 * admin mid-test, which would undermine the assessment's integrity.
 */
export default function SupportStudent() {
  const { t, language } = useLanguage();
  const [threads, setThreads] = useState([]);
  const [options, setOptions] = useState({ categories: [], admins: [] });
  const [selectedId, setSelectedId] = useState(null);
  const [thread, setThread] = useState(null);
  const [composing, setComposing] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [attachments, setAttachments] = useState([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const [loaded, setLoaded] = useState(false);

  // Labels (category/status) are translated server-side, so a language switch
  // has to refetch rather than re-render — same as TeacherReview.jsx.
  useEffect(() => { getSupportOptions().then(setOptions).catch(() => {}); }, [language]);

  const loadThreads = () => getSupportThreads().then(setThreads).catch(() => {});

  useEffect(() => {
    getSupportThreads()
      .then((rows) => {
        setThreads(rows);
        setLoaded(true);
        // A first-time student lands straight in the composer instead of on an
        // empty list they'd have to figure out.
        if (rows.length === 0) setComposing(true);
      })
      .catch(() => setLoaded(true));
  }, [language]);

  useEffect(() => {
    if (selectedId == null) return;
    getSupportThread(selectedId).then(setThread).catch(() => {});
  }, [selectedId, language]);

  // An admin's reply lands here without a refresh - see state/useSupportPolling.
  // The new messages are painted straight away, then the thread and the list
  // are refetched because the reply also moved the status ("answered") and the
  // row's preview, both of which are decided server-side.
  const appendMessages = (incoming) => {
    setThread((current) => (current ? {
      ...current,
      messages: [...current.messages, ...incoming.filter((r) => !current.messages.some((m) => m.id === r.id))],
    } : current));
    if (selectedId != null) getSupportThread(selectedId).then(setThread).catch(() => {});
    loadThreads();
  };

  useThreadMessagePolling({
    threadId: thread?.id ?? null,
    lastMessageId: thread?.messages?.length ? thread.messages[thread.messages.length - 1].id : null,
    onMessages: appendMessages,
  });

  const openThread = (id) => {
    setComposing(false);
    setError(null);
    setSelectedId(id);
    // Clear the unread dot locally the moment it's opened; the server clears
    // its counter on the same request.
    setThreads((rows) => rows.map((r) => (r.id === id ? { ...r, unread: 0 } : r)));
  };

  const clearAttachments = () => {
    setAttachments((current) => { current.forEach((item) => URL.revokeObjectURL(item.url)); return []; });
  };

  const startComposing = () => {
    setComposing(true);
    setSelectedId(null);
    setThread(null);
    setForm(EMPTY_FORM);
    clearAttachments();
    setError(null);
  };

  const updateForm = (key, value) => { setForm((f) => ({ ...f, [key]: value })); setError(null); };

  // The subject already carries the context, so a screenshot with no typed
  // description is a complete report on its own.
  const canSubmitNew = Boolean(form.subject.trim()) && Boolean(form.body.trim() || attachments.length) && !sending;

  const submitNew = async () => {
    if (!canSubmitNew) return;
    setSending(true);
    setError(null);
    try {
      const created = await createSupportThread(form, attachments.map((item) => item.file));
      setThreads((rows) => [created, ...rows]);
      setThread(created);
      setSelectedId(created.id);
      setComposing(false);
      setForm(EMPTY_FORM);
      clearAttachments();
    } catch (e) {
      setError(e.message);
    } finally {
      setSending(false);
    }
  };

  const reply = async (body, files) => {
    setSending(true);
    setError(null);
    try {
      const message = await sendSupportMessage(thread.id, body, files);
      setThread((current) => ({ ...current, messages: [...current.messages, message] }));
      // A reply reopens a resolved thread and changes the row's preview — both
      // are decided server-side (an image-only message has no text to preview),
      // so refetch rather than patching the local copies from here.
      await loadThreads();
      setThread(await getSupportThread(thread.id));
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    } finally {
      setSending(false);
    }
  };

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('support.studentTitle')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 22px', maxWidth: '640px' }}>{t('support.studentSubtitle')}</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', alignItems: 'start' }}>
        <div style={PANEL}>
          <div style={{ padding: '14px', borderBottom: '1px solid rgba(31,55,75,0.08)' }}>
            <button className="mm-btn" onClick={startComposing} style={{
              width: '100%', padding: '11px 14px', borderRadius: '12px', border: 'none', cursor: 'pointer',
              background: composing ? '#1F374B' : 'rgba(46,85,112,0.12)', color: composing ? '#fff' : '#1F374B',
              fontFamily: 'Manrope', fontWeight: 700, fontSize: '13.5px',
            }}>{t('support.newThread')}</button>
          </div>

          {threads.length > 0 ? (
            <div style={{ maxHeight: '520px', overflowY: 'auto' }}>
              {threads.map((row) => (
                <button key={row.id} className="mm-btn" onClick={() => openThread(row.id)} style={{
                  width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'stretch', gap: '5px',
                  padding: '13px 14px', border: 'none', borderBottom: '1px solid rgba(31,55,75,0.06)',
                  cursor: 'pointer', textAlign: 'left',
                  background: selectedId === row.id ? 'rgba(46,85,112,0.08)' : 'transparent',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ flex: 1, minWidth: 0, fontSize: '13px', fontWeight: 700, color: '#161F24', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {row.subject}
                    </span>
                    {row.unread > 0 && (
                      <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#3F9C6D', flexShrink: 0 }} />
                    )}
                  </div>
                  <div style={{ fontSize: '11.5px', color: '#939EA3', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {row.preview}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '7px', flexWrap: 'wrap' }}>
                    <span style={{ fontSize: '10px', fontWeight: 700, padding: '2px 8px', borderRadius: '100px', background: row.statusBg, color: row.statusColor }}>
                      {row.statusLabel}
                    </span>
                    <span style={{ fontSize: '10.5px', color: '#939EA3' }}>{formatStamp(row.lastMessageAt, language)}</span>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            loaded && (
              <div style={{ padding: '26px 18px', textAlign: 'center' }}>
                <div style={{ fontSize: '13px', fontWeight: 700, color: '#161F24' }}>{t('support.emptyTitle')}</div>
                <div style={{ fontSize: '12px', color: '#939EA3', marginTop: '4px' }}>{t('support.emptyHint')}</div>
              </div>
            )
          )}
        </div>

        <div style={PANEL}>
          {composing ? (
            <div style={{ padding: '18px' }}>
              <div style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', marginBottom: '16px' }}>{t('support.newThread')}</div>

              <label style={LABEL_STYLE}>{t('support.categoryLabel')}</label>
              <div style={{ display: 'flex', gap: '7px', flexWrap: 'wrap', marginBottom: '16px' }}>
                {options.categories.map((c) => (
                  <button key={c.key} className="mm-btn" onClick={() => updateForm('category', c.key)} style={{
                    padding: '7px 13px', borderRadius: '100px', cursor: 'pointer', fontFamily: 'Manrope',
                    fontSize: '12.5px', fontWeight: 700,
                    border: `1px solid ${form.category === c.key ? '#1F374B' : 'rgba(31,55,75,0.14)'}`,
                    background: form.category === c.key ? '#1F374B' : 'rgba(255,255,255,0.7)',
                    color: form.category === c.key ? '#fff' : '#556269',
                  }}>{c.label}</button>
                ))}
              </div>

              <label style={LABEL_STYLE} htmlFor="mm-support-subject">{t('support.subjectLabel')}</label>
              <input
                id="mm-support-subject"
                value={form.subject}
                onChange={(e) => updateForm('subject', e.target.value.slice(0, SUBJECT_MAX_LENGTH))}
                placeholder={t('support.subjectPlaceholder')}
                style={{ ...INPUT_STYLE, marginBottom: '16px' }}
              />

              <label style={LABEL_STYLE} htmlFor="mm-support-admin">{t('support.assigneeLabel')}</label>
              <select
                id="mm-support-admin"
                value={form.assigneeId}
                onChange={(e) => updateForm('assigneeId', e.target.value)}
                style={{ ...INPUT_STYLE, marginBottom: '6px' }}
              >
                {/* Default is the shared queue: a thread addressed to one absent
                    admin would otherwise wait for that person alone. */}
                <option value="">{t('support.anyAdmin')}</option>
                {options.admins.map((a) => <option key={a.id} value={a.id}>{a.name}</option>)}
              </select>
              <div style={{ fontSize: '11px', color: '#939EA3', marginBottom: '16px' }}>{t('support.assigneeHint')}</div>

              <label style={LABEL_STYLE} htmlFor="mm-support-body">{t('support.bodyLabel')}</label>
              <textarea
                id="mm-support-body"
                value={form.body}
                onChange={(e) => updateForm('body', e.target.value.slice(0, BODY_MAX_LENGTH))}
                rows={6}
                placeholder={t('support.bodyPlaceholder')}
                style={{ ...INPUT_STYLE, resize: 'vertical' }}
              />
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '10px', marginTop: '6px' }}>
                <span style={{ fontSize: '11px', color: '#939EA3' }}>{form.body.length} / {BODY_MAX_LENGTH}</span>
              </div>

              <label style={{ ...LABEL_STYLE, marginTop: '16px' }}>{t('support.screenshotsLabel')}</label>
              <ScreenshotDropzone items={attachments} onChange={setAttachments} disabled={sending} />

              {error && <div style={{ fontSize: '12px', color: '#BD5B4C', marginTop: '10px' }}>{error}</div>}

              <div style={{ display: 'flex', gap: '9px', marginTop: '16px' }}>
                <button className="mm-btn" onClick={submitNew} disabled={!canSubmitNew} style={{
                  padding: '11px 20px', borderRadius: '100px', border: 'none', fontFamily: 'Manrope', fontWeight: 700, fontSize: '13px',
                  background: canSubmitNew ? '#1F374B' : 'rgba(31,55,75,0.25)',
                  color: '#fff', cursor: canSubmitNew ? 'pointer' : 'default',
                }}>{sending ? t('support.sending') : t('support.submitThread')}</button>
                {threads.length > 0 && (
                  <button className="mm-btn" onClick={() => setComposing(false)} style={{
                    padding: '11px 20px', borderRadius: '100px', border: '1px solid rgba(31,55,75,0.14)',
                    background: 'rgba(255,255,255,0.8)', color: '#556269', fontFamily: 'Manrope', fontWeight: 700,
                    fontSize: '13px', cursor: 'pointer',
                  }}>{t('support.cancel')}</button>
                )}
              </div>
            </div>
          ) : thread ? (
            <SupportThreadView
              thread={thread}
              onSend={reply}
              sending={sending}
              error={error}
              headerExtra={
                <div style={{ fontSize: '11.5px', color: '#939EA3', marginTop: '8px' }}>
                  {thread.assignee ? t('support.handledBy')(thread.assignee.name) : t('support.inSharedQueue')}
                </div>
              }
            />
          ) : (
            <div style={{ padding: '44px 24px', textAlign: 'center' }}>
              <div style={{ fontSize: '13.5px', color: '#556269' }}>{t('support.selectPrompt')}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
