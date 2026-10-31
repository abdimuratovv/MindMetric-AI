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
          ? <ol lang={project.content_language}>{project[field].map((line, i) => <li key={i}>{line}</li>)}</ol>
          : <ul lang={project.content_language}>{project[field].map((line, i) => <li key={i}>{line}</li>)}</ul>}
      </section>)}</div>
    </details>)}
  </section>;
}
