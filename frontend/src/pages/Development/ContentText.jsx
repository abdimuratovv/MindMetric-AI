// Render only fenced code and plain text. Never interpret source content as HTML.
export default function ContentText({ text }) {
  return String(text ?? '').split(/(```[^\n]*\n[\s\S]*?```)/g).map((part, index) => {
    const block = /^```[^\n]*\n([\s\S]*?)```$/.exec(part);
    return block
      ? <pre className="dev-code" key={index}><code>{block[1].replace(/\n$/, '')}</code></pre>
      : <span className="dev-content-text" key={index}>{part}</span>;
  });
}
