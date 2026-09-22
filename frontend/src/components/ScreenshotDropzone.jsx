import { useEffect, useRef, useState } from 'react';

import { useLanguage } from '../i18n/LanguageContext.jsx';

export const MAX_ATTACHMENTS = 3;
// Kept well under the server's 1.5MB backstop (apps.support.models). A 4K
// screenshot lands around 150-250KB at these settings, which matters: the bytes
// go into Postgres, and students are often on campus wifi or mobile data.
const MAX_EDGE = 1600;
const QUALITY = 0.82;

/** Re-encodes a picked/pasted/dropped image to WebP at most MAX_EDGE on its long side. */
async function compress(file) {
  const bitmap = await createImageBitmap(file);
  const scale = Math.min(1, MAX_EDGE / Math.max(bitmap.width, bitmap.height));
  const canvas = document.createElement('canvas');
  canvas.width = Math.round(bitmap.width * scale);
  canvas.height = Math.round(bitmap.height * scale);
  canvas.getContext('2d').drawImage(bitmap, 0, 0, canvas.width, canvas.height);
  bitmap.close?.();

  const encode = (type) => new Promise((resolve) => canvas.toBlob(resolve, type, QUALITY));
  // toBlob resolves null for a type the browser can't encode — JPEG is the
  // universally supported fallback, and the server accepts both.
  const blob = (await encode('image/webp')) || (await encode('image/jpeg'));
  const extension = blob.type === 'image/webp' ? 'webp' : 'jpg';
  return new File([blob], `screenshot.${extension}`, { type: blob.type });
}

/**
 * Screenshot picker for the support composer: paste (the way a student actually
 * produces one — Win+Shift+S then Ctrl+V), drag-drop, or the file dialog.
 *
 * `items` are {id, file, url} — the parent owns the list so it can send the
 * files and clear them after a successful post.
 */
export default function ScreenshotDropzone({ items, onChange, disabled }) {
  const { t } = useLanguage();
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const inputRef = useRef(null);
  const itemsRef = useRef(items);
  itemsRef.current = items;

  const addFiles = async (candidates) => {
    const images = Array.from(candidates).filter((f) => f && f.type.startsWith('image/'));
    if (images.length === 0) return;
    if (itemsRef.current.length + images.length > MAX_ATTACHMENTS) {
      setError(t('support.tooManyFiles'));
      return;
    }
    setError(null);
    setBusy(true);
    try {
      const prepared = await Promise.all(images.map(async (file) => {
        const compressed = await compress(file);
        return { id: `${Date.now()}-${Math.random()}`, file: compressed, url: URL.createObjectURL(compressed) };
      }));
      onChange([...itemsRef.current, ...prepared]);
    } catch {
      setError(t('support.imageFailed'));
    } finally {
      setBusy(false);
    }
  };

  // Ctrl+V anywhere on the screen while the composer is mounted — a student
  // shouldn't have to find and focus the right box first. Only one dropzone is
  // ever mounted at a time (composer or open thread, never both).
  useEffect(() => {
    if (disabled) return undefined;
    const onPaste = (e) => {
      const files = Array.from(e.clipboardData?.items || [])
        .filter((item) => item.kind === 'file')
        .map((item) => item.getAsFile());
      if (files.length) {
        e.preventDefault();
        addFiles(files);
      }
    };
    document.addEventListener('paste', onPaste);
    return () => document.removeEventListener('paste', onPaste);
  }, [disabled]); // eslint-disable-line react-hooks/exhaustive-deps

  // Release the thumbnails' object URLs when the picker goes away.
  useEffect(() => () => itemsRef.current.forEach((item) => URL.revokeObjectURL(item.url)), []);

  const remove = (id) => {
    const target = items.find((item) => item.id === id);
    if (target) URL.revokeObjectURL(target.url);
    onChange(items.filter((item) => item.id !== id));
    setError(null);
  };

  const full = items.length >= MAX_ATTACHMENTS;

  return (
    <div>
      <div
        onDragOver={(e) => { e.preventDefault(); if (!disabled && !full) setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => { e.preventDefault(); setDragging(false); if (!disabled && !full) addFiles(e.dataTransfer.files); }}
        onClick={() => !disabled && !full && inputRef.current?.click()}
        style={{
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
          padding: '10px 12px', borderRadius: '12px', textAlign: 'center',
          border: `1px dashed ${dragging ? '#2E5570' : 'rgba(31,55,75,0.22)'}`,
          background: dragging ? 'rgba(46,85,112,0.08)' : 'rgba(255,255,255,0.5)',
          cursor: disabled || full ? 'default' : 'pointer', opacity: disabled || full ? 0.55 : 1,
          transition: 'border-color 0.15s ease, background 0.15s ease',
        }}
      >
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#556269" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          <path d="M3 5h18v14H3zM3 16l5-5 4 4 3-3 6 6" />
          <circle cx="8.5" cy="9" r="1.5" />
        </svg>
        <span style={{ fontSize: '12px', fontWeight: 600, color: '#556269' }}>
          {busy ? t('support.processingImage') : t('support.attachHint')}
        </span>
      </div>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        multiple
        onChange={(e) => { addFiles(e.target.files); e.target.value = ''; }}
        style={{ display: 'none' }}
      />

      {items.length > 0 && (
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '9px' }}>
          {items.map((item) => (
            <div key={item.id} style={{ position: 'relative' }}>
              <img src={item.url} alt="" style={{
                width: '62px', height: '62px', objectFit: 'cover', borderRadius: '10px',
                border: '1px solid rgba(31,55,75,0.12)', display: 'block',
              }} />
              <button
                className="mm-btn"
                onClick={() => remove(item.id)}
                aria-label={t('support.removeImage')}
                style={{
                  position: 'absolute', top: '-6px', right: '-6px', width: '20px', height: '20px',
                  borderRadius: '50%', border: 'none', background: '#1F374B', color: '#fff',
                  fontSize: '13px', lineHeight: 1, cursor: 'pointer', display: 'flex',
                  alignItems: 'center', justifyContent: 'center', padding: 0,
                }}>×</button>
              <div style={{ fontSize: '9.5px', color: '#939EA3', textAlign: 'center', marginTop: '2px' }}>
                {Math.round(item.file.size / 1024)} KB
              </div>
            </div>
          ))}
        </div>
      )}

      {error && <div style={{ fontSize: '11.5px', color: '#BD5B4C', marginTop: '6px' }}>{error}</div>}
    </div>
  );
}
