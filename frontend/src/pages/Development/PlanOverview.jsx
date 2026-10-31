export default function PlanOverview({ plan, c, busy, onOpen }) {
  if (!plan) return null;
  const completed = plan.modules.filter((module) => module.stage === 'completed').length;
  return <section className="dev-plan" aria-labelledby="development-plan-heading">
    <div className="dev-plan-heading"><div><p className="dev-eyebrow">{c.planEyebrow}</p>
      <h2 id="development-plan-heading">{c.planTitle}</h2>
      <p className="dev-note">{plan.check_active ? c.planDuringCheck : c.planNote}</p>
    </div><div className="dev-plan-completion"><strong>{completed}<span> / {plan.modules.length}</span></strong>
      <span>{c.modulesCompleted}</span><progress value={completed} max={plan.modules.length || 1} aria-label={c.modulesCompleted} />
    </div></div>
    {plan.recommended.length ? <div className="dev-priorities">{plan.recommended.map((module, index) => <article className="dev-priority" key={module.key}>
      <span className="dev-priority-number" aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
      <div><p className="dev-eyebrow">{c.module} / 1.{module.order}</p><h3 lang={module.content_language}>{module.title}</h3>
        <p>{module.recommendation.reason}</p>
        {module.recommendation.evidence_count > 0 && <p className="dev-note">{c.relatedAnswers}: {module.recommendation.evidence_count}</p>}
        <button className="dev-button" disabled={busy} onClick={() => onOpen(module)}>
          {module.recommendation.action === 'resume' ? c.resume : module.recommendation.action === 'review' ? c.reviewTopic : c.verifyTopic} →
        </button>
      </div>
    </article>)}</div> : <p className="dev-note">{c.noPriorities}</p>}
    {!plan.check_active && <p className="dev-note dev-evidence-note">{c.evidenceRule.replace('{count}', plan.minimum_diagnostic_responses)}</p>}
  </section>;
}
