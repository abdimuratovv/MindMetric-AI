import { useEffect, useRef, useState } from 'react';

import { getSupportMessagesAfter, getSupportUnread } from '../api/support.js';

// No WebSockets in this stack (same constraint as apps.videocalls), so the
// support channel keeps itself fresh by short polling. Two different cadences:
// an open conversation should feel close to live, while the shell-wide badge
// only has to notice a reply within half a minute.
const THREAD_POLL_INTERVAL_MS = 6000;
const UNREAD_POLL_INTERVAL_MS = 25000;

/**
 * setInterval that stops while the tab is hidden and resumes when it comes
 * back. Without this, every backgrounded tab keeps hitting the API — the
 * backend runs on Render's free instance, so idle tabs are a real cost.
 */
function useVisibleInterval(callback, delay, enabled) {
  const saved = useRef(callback);
  saved.current = callback;

  useEffect(() => {
    if (!enabled) return undefined;
    let id = null;
    const start = () => { if (id === null) id = setInterval(() => saved.current(), delay); };
    const stop = () => { if (id !== null) { clearInterval(id); id = null; } };
    const sync = () => (document.visibilityState === 'hidden' ? stop() : start());

    sync();
    document.addEventListener('visibilitychange', sync);
    return () => { stop(); document.removeEventListener('visibilitychange', sync); };
  }, [delay, enabled]);
}

/**
 * Polls the open conversation for messages newer than `lastMessageId` and hands
 * the new ones to `onMessages`. Only the delta crosses the wire, so a long
 * thread doesn't get refetched every few seconds.
 */
export function useThreadMessagePolling({ threadId, lastMessageId, onMessages }) {
  const lastRef = useRef(lastMessageId);
  lastRef.current = lastMessageId;
  const handlerRef = useRef(onMessages);
  handlerRef.current = onMessages;

  useVisibleInterval(() => {
    if (threadId == null || lastRef.current == null) return;
    getSupportMessagesAfter(threadId, lastRef.current)
      .then((rows) => { if (rows.length) handlerRef.current(rows); })
      .catch(() => {});
  }, THREAD_POLL_INTERVAL_MS, threadId != null);
}

/**
 * Unread message count for the sidebar badge. `refreshKey` changes whenever the
 * shell navigates, so opening the support screen clears the dot immediately
 * instead of waiting out the interval.
 */
export function useSupportUnread(refreshKey) {
  const [unread, setUnread] = useState(0);

  const load = () => getSupportUnread().then((data) => setUnread(data.messages)).catch(() => {});

  useEffect(() => { load(); }, [refreshKey]); // eslint-disable-line react-hooks/exhaustive-deps
  useVisibleInterval(load, UNREAD_POLL_INTERVAL_MS, true);

  return unread;
}
