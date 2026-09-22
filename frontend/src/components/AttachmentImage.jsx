import { useEffect, useState } from 'react';

import { fetchBlobUrl } from '../api/client.js';
import { useLanguage } from '../i18n/LanguageContext.jsx';

/**
 * One support screenshot inside a message bubble.
 *
 * The bytes are permission-checked per request, so they're fetched with the JWT
 * and rendered from an object URL rather than pointed at with a plain src —
 * see api/client.js fetchBlobUrl and apps.support.views.AttachmentView.
 * Clicking opens it full size, since a 62px thumbnail is useless for the thing
 * screenshots are for: reading what went wrong.
 */
export default function AttachmentImage({ attachment }) {
  const { t } = useLanguage();
  const [url, setUrl] = useState(null);
  const [failed, setFailed] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let objectUrl = null;
    let cancelled = false;
    fetchBlobUrl(attachment.url)
      .then((next) => {
        objectUrl = next;
        if (cancelled) URL.revokeObjectURL(next);
        else setUrl(next);
      })
      .catch(() => { if (!cancelled) setFailed(true); });
    return () => {
      cancelled = true;
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [attachment.url]);

  useEffect(() => {
    if (!open) return undefined;
    const onKey = (e) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [open]);

  if (failed) {
    return <div style={{ fontSize: '11.5px', color: '#BD5B4C' }}>{t('support.imageUnavailable')}</div>;
  }

  return (
    <>
      <button
        className="mm-btn"
        onClick={() => url && setOpen(true)}
        aria-label={t('support.openImage')}
        style={{
          padding: 0, border: '1px solid rgba(31,55,75,0.12)', borderRadius: '10px', overflow: 'hidden',
          background: 'rgba(31,55,75,0.05)', cursor: url ? 'zoom-in' : 'default', display: 'block',
          width: '120px', height: '86px',
        }}
      >
        {url && <img src={url} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} />}
      </button>

      {open && (
        <div
          onClick={() => setOpen(false)}
          style={{
            position: 'fixed', inset: 0, zIndex: 80, background: 'rgba(22,31,36,0.82)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '28px', cursor: 'zoom-out',
          }}
        >
          <img src={url} alt="" style={{ maxWidth: '100%', maxHeight: '100%', borderRadius: '10px', display: 'block' }} />
        </div>
      )}
    </>
  );
}
