import { useEffect, useRef, useState } from 'react';

import { useLanguage } from '../i18n/LanguageContext.jsx';
import AttachmentImage from './AttachmentImage.jsx';
import ScreenshotDropzone from './ScreenshotDropzone.jsx';

// Same hand-rolled formatter as Results.jsx/Achievements.jsx — browsers' bundled
// ICU data has no Uzbek month names, so Intl would silently render "M07"-style
// placeholders on the uz side.
const MONTH_ABBR = {
  ru: ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'],
  uz: ['yan', 'fev', 'mar', 'apr', 'may', 'iyun', 'iyul', 'avg', 'sen', 'okt', 'noy', 'dek'],
};

export function formatStamp(iso, lang) {
  const d = new Date(iso);
  const time = `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
  return `${d.getDate()} ${MONTH_ABBR[lang][d.getMonth()]}, ${time}`;
}

export const BODY_MAX_LENGTH = 2000;

/**
 * One support conversation, rendered identically for both sides — the student's
 * "Yordam" screen and the admin inbox mount the same component, so the two
 * never drift apart. Which side a bubble sits on comes from the server's
 * `message.mine` flag rather than the viewer's role (see
 * apps.support.serializers.serialize_message).
 *
 * `headerExtra` is where the admin inbox injects its queue controls (resolve,
 * assignee) — the student side passes nothing.
 */
export default function SupportThreadView({ thread, onSend, sending, error, headerExtra, disabled }) {
  const { t, language } = useLanguage();
  const [draft, setDraft] = useState('');
  const [attachments, setAttachments] = useState([]);
  const [focused, setFocused] = useState(false);
  const listRef = useRef(null);

  // Jump to the newest message whenever the open thread changes or grows.
  useEffect(() => {
    const list = listRef.current;
    if (list) list.scrollTop = list.scrollHeight;
  }, [thread?.id, thread?.messages?.length]);

  if (!thread) return null;

  // A screenshot on its own is a valid message — the server allows an empty
  // body when files are attached (apps.support.serializers).
  const canSend = Boolean(draft.trim() || attachments.length) && !sending && !disabled;

  const submit = async () => {
    if (!canSend) return;
    const ok = await onSend(draft.trim(), attachments.map((item) => item.file));
    // Keep the text and images on failure so a dropped request doesn't cost the
    // student everything they typed — they can retry with the same draft.
    if (ok) {
      setDraft('');
      attachments.forEach((item) => URL.revokeObjectURL(item.url));
      setAttachments([]);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: 0 }}>
      <div style={{ padding: '16px 18px', borderBottom: '1px solid rgba(31,55,75,0.08)' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '180px' }}>
            <div style={{ fontSize: '15px', fontWeight: 700, color: '#161F24', lineHeight: 1.35 }}>{thread.subject}</div>
            <div style={{ fontSize: '11.5px', color: '#939EA3', marginTop: '3px' }}>
              {thread.categoryLabel} · {formatStamp(thread.createdAt, language)}
            </div>
          </div>
          <span style={{
            fontSize: '10.5px', fontWeight: 700, padding: '4px 10px', borderRadius: '100px',
            background: thread.statusBg, color: thread.statusColor, whiteSpace: 'nowrap',
          }}>{thread.statusLabel}</span>
        </div>
        {headerExtra}
      </div>

      <div ref={listRef} style={{
        flex: 1, minHeight: '220px', maxHeight: '430px', overflowY: 'auto',
        padding: '18px', display: 'flex', flexDirection: 'column', gap: '12px',
      }}>
        {thread.messages.map((m) => (
          <div key={m.id} style={{ display: 'flex', justifyContent: m.mine ? 'flex-end' : 'flex-start' }}>
            <div style={{ maxWidth: '78%' }}>
              <div style={{
                padding: '10px 13px', borderRadius: m.mine ? '14px 14px 4px 14px' : '14px 14px 14px 4px',
                background: m.mine ? '#1F374B' : 'rgba(255,255,255,0.92)',
                border: m.mine ? 'none' : '1px solid rgba(31,55,75,0.1)',
                color: m.mine ? '#fff' : '#161F24', fontSize: '13.5px', lineHeight: 1.5,
                whiteSpace: 'pre-wrap', wordBreak: 'break-word',
                display: m.body ? 'block' : 'none',
              }}>{m.body}</div>
              {m.attachments?.length > 0 && (
                <div style={{
                  display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: m.body ? '6px' : 0,
                  justifyContent: m.mine ? 'flex-end' : 'flex-start',
                }}>
                  {m.attachments.map((a) => <AttachmentImage key={a.id} attachment={a} />)}
                </div>
              )}
              <div style={{
                fontSize: '10.5px', color: '#939EA3', marginTop: '4px',
                textAlign: m.mine ? 'right' : 'left',
              }}>
                {m.mine ? t('support.you') : m.authorName} · {formatStamp(m.createdAt, language)}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ padding: '14px 18px 16px', borderTop: '1px solid rgba(31,55,75,0.08)' }}>
        <textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value.slice(0, BODY_MAX_LENGTH))}
          onKeyDown={onKeyDown}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          disabled={disabled}
          rows={3}
          placeholder={t('support.replyPlaceholder')}
          style={{
            width: '100%', boxSizing: 'border-box', padding: '11px 13px', borderRadius: '12px', resize: 'vertical',
            border: `1px solid ${focused ? '#2E5570' : 'rgba(31,55,75,0.14)'}`,
            boxShadow: focused ? '0 0 0 3px rgba(46,85,112,0.14)' : 'none',
            transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
            fontFamily: 'Manrope', fontSize: '13.5px', outline: 'none', background: 'rgba(255,255,255,0.85)', color: '#161F24',
          }}
        />
        <div style={{ marginTop: '9px' }}>
          <ScreenshotDropzone items={attachments} onChange={setAttachments} disabled={disabled || sending} />
        </div>
        {error && <div style={{ fontSize: '12px', color: '#BD5B4C', marginTop: '6px' }}>{error}</div>}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px', marginTop: '9px' }}>
          <span style={{ fontSize: '11px', color: '#939EA3' }}>{t('support.enterHint')}</span>
          <button className="mm-btn" onClick={submit} disabled={!canSend} style={{
            padding: '9px 18px', borderRadius: '100px', border: 'none',
            background: canSend ? '#1F374B' : 'rgba(31,55,75,0.25)',
            color: '#fff', fontWeight: 700, fontSize: '13px', fontFamily: 'Manrope',
            cursor: canSend ? 'pointer' : 'default',
          }}>{sending ? t('support.sending') : t('support.send')}</button>
        </div>
      </div>
    </div>
  );
}
