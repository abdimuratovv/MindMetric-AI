import { useEffect, useState } from 'react';

import {
  getSupportOptions,
  getSupportThread,
  getSupportThreads,
  sendSupportMessage,
  updateSupportThread,
} from '../../api/support.js';
import { SELECT_STYLE } from '../../components/adminStyles.js';
import SupportThreadView, { formatStamp } from '../../components/SupportThreadView.jsx';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import { useThreadMessagePolling } from '../../state/useSupportPolling.js';

const PANEL = {
  borderRadius: '20px', background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(255,255,255,0.85)',
  backdropFilter: 'blur(14px)', overflow: 'hidden',
};

const OWNER_TABS = ['all', 'unassigned', 'me'];

/**
 * The admin side of the written support channel — the same two-pane shape as
 * TeacherReview.jsx (queue on the left, work surface on the right), so the two
 * admin queues read as one surface.
 */
export default function SupportInbox({ user }) {
  const { t, language } = useLanguage();
  const [rows, setRows] = useState([]);
  const [options, setOptions] = useState({ categories: [], statuses: [], admins: [] });
  const [filters, setFilters] = useState({ assignee: 'all', status: '', category: '', search: '' });
  const [selectedId, setSelectedId] = useState(null);
  const [thread, setThread] = useState(null);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const [searchFocused, setSearchFocused] = useState(false);

  useEffect(() => { getSupportOptions().then(setOptions).catch(() => {}); }, [language]);

  const loadRows = () => getSupportThreads(filters).then(setRows).catch(() => {});

  useEffect(() => { loadRows(); }, [filters, language]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (selectedId == null) return;
    getSupportThread(selectedId).then(setThread).catch(() => {});
  }, [selectedId, language]);

  // A student's follow-up appears without leaving the thread; the queue row is
  // refreshed alongside it so its status badge keeps up.
  const appendMessages = (incoming) => {
    setThread((current) => (current ? {
      ...current,
      messages: [...current.messages, ...incoming.filter((r) => !current.messages.some((m) => m.id === r.id))],
    } : current));
    // A student's follow-up reopens the thread, so the open header and the
    // queue row both need the server's new status, not just the message.
    if (selectedId != null) getSupportThread(selectedId).then(setThread).catch(() => {});
    loadRows();
  };

  useThreadMessagePolling({
    threadId: thread?.id ?? null,
    lastMessageId: thread?.messages?.length ? thread.messages[thread.messages.length - 1].id : null,
    onMessages: appendMessages,
  });

  const openThread = (id) => {
    setError(null);
    setSelectedId(id);
    setRows((current) => current.map((r) => (r.id === id ? { ...r, unread: 0 } : r)));
  };

  const updateFilter = (key, value) => setFilters((f) => ({ ...f, [key]: value }));

  const reply = async (body, files) => {
    setSending(true);
    setError(null);
    try {
      const message = await sendSupportMessage(thread.id, body, files);
      setThread((current) => ({ ...current, messages: [...current.messages, message] }));
      // The reply flips the thread to "answered" and claims an unassigned one
      // server-side (apps.support.views._append_message) — refetch the queue so
      // the list reflects that instead of guessing at the new state here.
      await loadRows();
      const refreshed = await getSupportThread(thread.id);
      setThread(refreshed);
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    } finally {
      setSending(false);
    }
  };

  const patchThread = async (payload) => {
    setError(null);
    try {
      setThread(await updateSupportThread(thread.id, payload));
      await loadRows();
    } catch (e) {
      setError(e.message);
    }
  };

  const isResolved = thread?.status === 'resolved';
  const mine = thread?.assignee?.id === user?.id;

  return (
    <div style={{ animation: 'mm-fade-up 0.4s ease both' }}>
      <h1 style={{ fontFamily: "'Montserrat',sans-serif", fontWeight: 700, fontSize: '30px', color: '#161F24', margin: '0 0 6px' }}>{t('support.inboxTitle')}</h1>
      <p style={{ fontSize: '14px', color: '#556269', margin: '0 0 22px', maxWidth: '660px' }}>{t('support.inboxSubtitle')}</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px', alignItems: 'start' }}>
        <div style={PANEL}>
          <div style={{ padding: '14px', borderBottom: '1px solid rgba(31,55,75,0.08)', display: 'flex', flexDirection: 'column', gap: '9px' }}>
            <div style={{ display: 'flex', gap: '5px' }}>
              {OWNER_TABS.map((key) => (
                <button key={key} className="mm-btn" onClick={() => updateFilter('assignee', key)} style={{
                  flex: 1, padding: '7px 10px', borderRadius: '9px', border: 'none', cursor: 'pointer',
                  fontFamily: 'Manrope', fontSize: '12px', fontWeight: 700,
                  background: filters.assignee === key ? 'rgba(46,85,112,0.14)' : 'rgba(255,255,255,0.7)',
                  color: filters.assignee === key ? '#1F374B' : '#939EA3',
                }}>{t(`support.owner.${key}`)}</button>
              ))}
            </div>
            <input
              value={filters.search}
              onChange={(e) => updateFilter('search', e.target.value)}
              onFocus={() => setSearchFocused(true)}
              onBlur={() => setSearchFocused(false)}
              placeholder={t('support.searchPlaceholder')}
              style={{
                width: '100%', boxSizing: 'border-box', padding: '9px 12px', borderRadius: '10px',
                border: `1px solid ${searchFocused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
                boxShadow: searchFocused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
                transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
                fontFamily: 'Manrope', fontSize: '13px', outline: 'none', background: 'rgba(255,255,255,0.8)',
              }}
            />
            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
              <select value={filters.status} onChange={(e) => updateFilter('status', e.target.value)} style={{ ...SELECT_STYLE, flex: 1 }}>
                <option value="">{t('support.allStatuses')}</option>
                {options.statuses.map((s) => <option key={s.key} value={s.key}>{s.label}</option>)}
              </select>
              <select value={filters.category} onChange={(e) => updateFilter('category', e.target.value)} style={{ ...SELECT_STYLE, flex: 1 }}>
                <option value="">{t('support.allCategories')}</option>
                {options.categories.map((c) => <option key={c.key} value={c.key}>{c.label}</option>)}
              </select>
            </div>
          </div>

          {rows.length > 0 ? (
            <div style={{ maxHeight: '560px', overflowY: 'auto' }}>
              {rows.map((row) => (
                <button key={row.id} className="mm-btn" onClick={() => openThread(row.id)} style={{
                  width: '100%', display: 'flex', gap: '11px', padding: '13px 14px', border: 'none',
                  borderBottom: '1px solid rgba(31,55,75,0.06)', cursor: 'pointer', textAlign: 'left',
                  background: selectedId === row.id ? 'rgba(46,85,112,0.08)' : 'transparent',
                }}>
                  <div style={{
                    width: '34px', height: '34px', borderRadius: '50%', background: '#DCECEF', display: 'flex',
                    alignItems: 'center', justifyContent: 'center', fontWeight: 700, color: '#1F374B', fontSize: '12px', flexShrink: 0,
                  }}>{row.student.initials}</div>
                  <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', gap: '3px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ flex: 1, minWidth: 0, fontSize: '13px', fontWeight: 700, color: '#161F24', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {row.subject}
                      </span>
                      {row.unread > 0 && <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#3F9C6D', flexShrink: 0 }} />}
                    </div>
                    <div style={{ fontSize: '11.5px', color: '#939EA3', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {row.student.name} · {row.preview}
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '7px', flexWrap: 'wrap' }}>
                      <span style={{ fontSize: '10px', fontWeight: 700, padding: '2px 8px', borderRadius: '100px', background: row.statusBg, color: row.statusColor }}>
                        {row.statusLabel}
                      </span>
                      <span style={{ fontSize: '10px', fontWeight: 700, padding: '2px 8px', borderRadius: '100px', background: 'rgba(31,55,75,0.07)', color: '#556269' }}>
                        {row.categoryLabel}
                      </span>
                      <span style={{ fontSize: '10.5px', color: '#939EA3' }}>{formatStamp(row.lastMessageAt, language)}</span>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div style={{ padding: '30px 18px', textAlign: 'center' }}>
              <div style={{ fontSize: '13px', fontWeight: 700, color: '#161F24' }}>{t('support.inboxEmptyTitle')}</div>
              <div style={{ fontSize: '12px', color: '#939EA3', marginTop: '4px' }}>{t('support.inboxEmptyHint')}</div>
            </div>
          )}
        </div>

        <div style={PANEL}>
          {thread ? (
            <SupportThreadView
              thread={thread}
              onSend={reply}
              sending={sending}
              error={error}
              headerExtra={
                <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '8px', marginTop: '12px' }}>
                  <span style={{ fontSize: '11.5px', color: '#939EA3', flex: 1, minWidth: '140px' }}>
                    {thread.student.name}{thread.student.program ? ` · ${thread.student.program}` : ''}
                    <br />
                    {thread.assignee ? t('support.handledBy')(thread.assignee.name) : t('support.inSharedQueue')}
                  </span>
                  {!mine && (
                    <button className="mm-btn" onClick={() => patchThread({ assignee_id: user.id })} style={{
                      padding: '7px 13px', borderRadius: '100px', border: '1px solid rgba(31,55,75,0.14)',
                      background: 'rgba(255,255,255,0.8)', color: '#1F374B', fontFamily: 'Manrope',
                      fontWeight: 700, fontSize: '12px', cursor: 'pointer',
                    }}>{t('support.assignToMe')}</button>
                  )}
                  <button
                    className="mm-btn"
                    onClick={() => patchThread({ status: isResolved ? 'open' : 'resolved' })}
                    style={{
                      padding: '7px 13px', borderRadius: '100px', border: 'none', cursor: 'pointer',
                      background: isResolved ? 'rgba(31,55,75,0.1)' : '#3F9C6D',
                      color: isResolved ? '#1F374B' : '#fff', fontFamily: 'Manrope', fontWeight: 700, fontSize: '12px',
                    }}>{isResolved ? t('support.reopen') : t('support.resolve')}</button>
                </div>
              }
            />
          ) : (
            <div style={{ padding: '54px 24px', textAlign: 'center' }}>
              <div style={{ fontSize: '13.5px', color: '#556269' }}>{t('support.inboxSelectPrompt')}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
