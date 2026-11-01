export default function ClusterCatalogue({ modules, clusters, selectedCluster, onSelect, c, busy, onOpen }) {
  // Older servers expose only the academic catalogue.
  const choices = clusters?.length ? clusters : [{ id: 1, title: c.academicCluster, module_count: modules.length }];
  const active = choices.find((cluster) => cluster.id === selectedCluster) || choices[0];
  const visible = modules.filter((module) => (module.cluster || 1) === active.id);
  return <section className="dev-catalogue" aria-label={c.catalogue}>
    <nav className="dev-cluster-selector" aria-label={c.clusterSelector}>
      {choices.map((cluster) => <button type="button" key={cluster.id} data-cluster={cluster.id}
        disabled={busy}
        aria-pressed={cluster.id === active.id} aria-controls="development-cluster-topics"
        onClick={() => onSelect(cluster.id)}>
        <span className="dev-cluster-number" aria-hidden="true">{String(cluster.id).padStart(2, '0')}</span>
        <span><strong>{cluster.title}</strong><small>{cluster.module_count} {c.topics}</small></span>
      </button>)}
    </nav>
    <div id="development-cluster-topics" data-cluster={active.id}>
      <section className="dev-intro" aria-labelledby="development-cluster-heading">
        <p className="dev-eyebrow">{c.clusterLabel} {String(active.id).padStart(2, '0')} / {active.title}</p>
        <h2 id="development-cluster-heading">{active.id === 3 ? c.personalOverview : active.id === 2 ? c.algorithmicOverview : c.overview}</h2>
        <p>{active.id === 3 ? c.personalDescription : active.id === 2 ? c.algorithmicDescription : c.description}</p>
        <div className="dev-symbols" aria-hidden="true">{active.id === 2
          ? <>if <span>→</span> for <span>→</span> return</>
          : active.id === 3 ? <>debug <span>→</span> review <span>→</span> learn</>
          : <>a² <span>+</span> √x <span>→</span> x = ?</>}</div>
      </section>
      {visible.length === 0 && <p>{c.empty}</p>}
      <div className="dev-module-grid">{visible.map((module) => <article className="dev-panel dev-module" key={module.key}>
        <p className="dev-eyebrow">{c.module} / {module.topic_number || `1.${module.order}`}</p>
        <h2 lang={module.content_language}>{module.title}</h2>
        <p lang={module.content_language}>{module.skill_titles?.join(' · ')}</p><p>{c.precheckReady}</p>
        <p className="dev-language">{module.content_language === 'ru' ? c.languageRu : c.language}</p>
        {module.stage && <span className="dev-chip">{c[module.stage]}</span>}
        <p className="dev-note">{module.recommendation?.reason}</p>
        <button className="dev-button" disabled={busy} onClick={() => onOpen(module)}>{module.enrollment_id ? c.resume : c.start} →</button>
      </article>)}</div>
    </div>
  </section>;
}
