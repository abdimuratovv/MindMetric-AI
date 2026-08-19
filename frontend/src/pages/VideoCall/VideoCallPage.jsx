import { Room, RoomEvent, Track } from 'livekit-client';
import { useEffect, useRef, useState } from 'react';

import { endCall } from '../../api/videocalls.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

/**
 * Full-screen LiveKit room UI — same tier as FocusedTestShell (no sidebar).
 * `call` is `{ callId, roomName, livekitUrl, token }` from enterCall()
 * (see api/videocalls.js's startCall/joinCall responses).
 */
export default function VideoCallPage({ call, onLeave }) {
  const { t } = useLanguage();
  const [status, setStatus] = useState('connecting'); // connecting | connected | error
  const [micOn, setMicOn] = useState(true);
  const [camOn, setCamOn] = useState(true);
  const [remoteName, setRemoteName] = useState('');
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const remoteAudioRef = useRef(null);
  const roomRef = useRef(null);

  useEffect(() => {
    if (!call) return undefined;
    let cancelled = false;
    // Connect failures also fire RoomEvent.Disconnected — this flag tells
    // that handler apart from a real post-connect hangup, so a bad/unreachable
    // LiveKit URL shows the error state instead of silently bouncing back.
    let hasConnected = false;
    const room = new Room();
    roomRef.current = room;

    room.on(RoomEvent.TrackSubscribed, (track, _publication, participant) => {
      if (track.kind === Track.Kind.Video) track.attach(remoteVideoRef.current);
      else if (track.kind === Track.Kind.Audio) track.attach(remoteAudioRef.current);
      setRemoteName(participant.name || participant.identity);
    });
    room.on(RoomEvent.TrackUnsubscribed, (track) => track.detach());
    room.on(RoomEvent.Disconnected, () => { if (!cancelled && hasConnected) onLeave(); });

    (async () => {
      try {
        await room.connect(call.livekitUrl, call.token);
        hasConnected = true;
      } catch {
        if (!cancelled) setStatus('error');
        return;
      }

      if (!cancelled) setStatus('connected');

      // Camera/mic failures (permission denied, no device) shouldn't be
      // treated as a connection error — the call is live either way, just
      // without local video/audio until the user grants access and retries
      // via the mic/camera buttons.
      try {
        const camPub = await room.localParticipant.setCameraEnabled(true);
        if (camPub?.track) camPub.track.attach(localVideoRef.current);
      } catch {
        if (!cancelled) setCamOn(false);
      }
      try {
        await room.localParticipant.setMicrophoneEnabled(true);
      } catch {
        if (!cancelled) setMicOn(false);
      }
    })();

    return () => {
      cancelled = true;
      endCall(call.callId).catch(() => {});
      room.disconnect();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [call?.roomName]);

  const toggleMic = async () => {
    const next = !micOn;
    await roomRef.current?.localParticipant.setMicrophoneEnabled(next);
    setMicOn(next);
  };

  const toggleCam = async () => {
    const next = !camOn;
    const pub = await roomRef.current?.localParticipant.setCameraEnabled(next);
    if (next && pub?.track) pub.track.attach(localVideoRef.current);
    setCamOn(next);
  };

  const leave = () => onLeave();

  if (!call) return null;

  const controlBtn = (active) => ({
    width: '52px', height: '52px', borderRadius: '50%', border: 'none', cursor: 'pointer',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    background: active ? 'rgba(255,255,255,0.14)' : '#BD5B4C', color: '#fff',
  });

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 50, background: '#12181D',
      display: 'flex', flexDirection: 'column', animation: 'mm-fade-up 0.3s ease both',
    }}>
      <div style={{
        padding: '16px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        color: '#fff', fontFamily: 'Manrope',
      }}>
        <div style={{ fontWeight: 700, fontSize: '14px' }}>
          {status === 'connecting' && t('videoCall.connecting')}
          {status === 'connected' && (remoteName ? t('videoCall.inCallWith')(remoteName) : t('videoCall.waitingForOther'))}
          {status === 'error' && t('videoCall.connectError')}
        </div>
      </div>

      <div style={{ flex: 1, position: 'relative', margin: '0 24px 16px', borderRadius: '20px', overflow: 'hidden', background: '#1B242B' }}>
        <video ref={remoteVideoRef} autoPlay playsInline style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        <audio ref={remoteAudioRef} autoPlay />
        {!remoteName && status !== 'error' && (
          <div style={{
            position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'rgba(255,255,255,0.55)', fontFamily: 'Manrope', fontSize: '13.5px',
          }}>
            {t('videoCall.waitingForOther')}
          </div>
        )}
        <div style={{
          position: 'absolute', bottom: '16px', right: '16px', width: '160px', height: '110px',
          borderRadius: '14px', overflow: 'hidden', background: '#0E1418', border: '1px solid rgba(255,255,255,0.18)',
        }}>
          <video ref={localVideoRef} autoPlay muted playsInline style={{ width: '100%', height: '100%', objectFit: 'cover', display: camOn ? 'block' : 'none' }} />
          {!camOn && (
            <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'rgba(255,255,255,0.4)', fontSize: '11px', fontFamily: 'Manrope' }}>
              {t('videoCall.cameraOff')}
            </div>
          )}
        </div>
      </div>

      <div style={{ padding: '18px 0 30px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
        <button className="mm-btn" onClick={toggleMic} style={controlBtn(micOn)} title={micOn ? t('videoCall.muteMic') : t('videoCall.unmuteMic')}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
            {micOn
              ? <path d="M12 15a3 3 0 003-3V6a3 3 0 00-6 0v6a3 3 0 003 3zM19 11a7 7 0 01-14 0M12 18v3" />
              : <path d="M3 3l18 18M12 15a3 3 0 003-3V6a3 3 0 00-5.6-1.5M9 9v3a3 3 0 004.2 2.75M19 11a7 7 0 01-1.4 4.2M12 18v3" />}
          </svg>
        </button>
        <button className="mm-btn" onClick={toggleCam} style={controlBtn(camOn)} title={camOn ? t('videoCall.turnCameraOff') : t('videoCall.turnCameraOn')}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
            {camOn
              ? <path d="M23 7l-7 5 7 5V7zM14 5H3a2 2 0 00-2 2v10a2 2 0 002 2h11a2 2 0 002-2V7a2 2 0 00-2-2z" />
              : <path d="M3 3l18 18M1 5.5V17a2 2 0 002 2h11.5M14 5H3a2 2 0 00-.7.13M23 7l-5.4 3.86" />}
          </svg>
        </button>
        <button className="mm-btn" onClick={leave} style={{
          padding: '0 26px', height: '52px', borderRadius: '100px', border: 'none', cursor: 'pointer',
          background: '#BD5B4C', color: '#fff', fontWeight: 700, fontSize: '13.5px', fontFamily: 'Manrope',
        }}>
          {t('videoCall.endCall')}
        </button>
      </div>
    </div>
  );
}
