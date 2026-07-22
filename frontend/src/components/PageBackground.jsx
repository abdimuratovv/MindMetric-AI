/**
 * The outer wrapper + two decorative blurred blobs that sit behind every
 * screen — ported verbatim from MindMetric AI.dc.html lines 24-27, which sit
 * outside all four `sc-if` blocks and so render unconditionally regardless
 * of `screen`.
 */
export default function PageBackground({ children }) {
  return (
    <div style={{ position: 'relative', minHeight: '100vh', width: '100%', overflowX: 'hidden', background: '#F5F7F8' }}>
      <div style={{
        position: 'fixed', top: '-140px', right: '-120px', width: '480px', height: '480px', borderRadius: '50%',
        background: 'radial-gradient(circle at 30% 30%, rgba(143,188,217,0.55), rgba(143,188,217,0) 70%)',
        filter: 'blur(10px)', animation: 'mm-blob 22s ease-in-out infinite', pointerEvents: 'none', zIndex: 0,
      }} />
      <div style={{
        position: 'fixed', bottom: '-180px', left: '-140px', width: '520px', height: '520px', borderRadius: '50%',
        background: 'radial-gradient(circle at 60% 60%, rgba(220,236,239,0.9), rgba(220,236,239,0) 70%)',
        filter: 'blur(6px)', animation: 'mm-blob 26s ease-in-out infinite reverse', pointerEvents: 'none', zIndex: 0,
      }} />
      {children}
    </div>
  );
}
