import ContentText from './ContentText.jsx';

export function StudyFiles({ files, c }) {
  if (!files?.length) return null;
  function download(file) {
    const url = URL.createObjectURL(new Blob([file.content], { type: 'text/plain;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url; link.download = file.filename; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  return <section className="dev-panel dev-study-files"><h3>{c.studyFilesTitle}</h3>
    {files.map((file) => <div key={file.key} lang={file.content_language}><p>{file.title}</p>
      <button className="dev-button dev-button-secondary" onClick={() => download(file)}>{c.downloadFile}: {file.filename}</button>
    </div>)}
  </section>;
}

export function CourseNotation({ rules, language, c, open, onToggle }) {
  if (!rules?.length) return null;
  return <details className="dev-panel dev-notation" open={open} onToggle={(event) => onToggle(event.currentTarget.open)}>
    <summary>{c.notationTitle}</summary><p className="dev-note">{c.notationNote}</p>
    <ul lang={language}>{rules.map((rule, index) => <li key={index}>{rule}</li>)}</ul>
  </details>;
}

export function MiniProjects({ projects, expanded, onToggle, c }) {
  if (!projects?.length) return null;
  return <section className="dev-projects" aria-labelledby="development-projects-heading">
    <div className="dev-projects-heading"><p className="dev-eyebrow">{c.applyKnowledge}</p>
      <h3 id="development-projects-heading">{c.projectsTitle}</h3><p className="dev-note">{c.projectsNote}</p>
    </div>
    {projects.map((project, index) => <details className="dev-panel dev-project" key={project.key}
      open={expanded.includes(project.key)} onToggle={(event) => onToggle(project.key, event.currentTarget.open)}>
      <summary><span className="dev-project-number">{String(index + 1).padStart(2, '0')}</span>
        <span lang={project.content_language}>{project.title}</span></summary>
      <p className="dev-project-brief" lang={project.content_language}>{project.brief}</p>
      <div className="dev-project-sections">{['constraints', 'steps', 'deliverables', 'rubric'].map((field) => <section key={field}>
        <h4>{c[`project_${field}`]}</h4>{field === 'steps'
          ? <ol lang={project.content_language}>{project[field].map((line, i) => <li key={i}><ContentText text={line} /></li>)}</ol>
          : <ul lang={project.content_language}>{project[field].map((line, i) => <li key={i}><ContentText text={line} /></li>)}</ul>}
      </section>)}</div>
    </details>)}
  </section>;
}
