export default function SkillProgress({ skills, c, lessons = [], onSelectLesson }) {
  if (!skills?.length) return null;
  const statuses = { review: c.skillReview, observed_success: c.skillObserved, insufficient: c.skillInsufficient, not_assessed: c.skillUnknown };
  const sources = { diagnostic: c.sourceDiagnostic, precheck: c.precheck, postcheck: c.postcheck, none: c.sourceNone };
  return <section className="dev-panel dev-skill-progress" aria-labelledby="skill-progress-heading">
    <h3 id="skill-progress-heading">{c.skillProgress}</h3>
    <ul>{skills.map((skill) => {
      const lessonIndex = lessons.findIndex((lesson) => lesson.skill_key === skill.key);
      return <li key={skill.key}>
        <div><strong lang="uz">{skill.title}</strong><p className="dev-note">
          {sources[skill.source]}{skill.source !== 'none' && ` · ${skill.count} ${c.answerCount}`}
          {skill.status === 'insufficient' && skill.minimum_count ? ` · ${c.minimum}: ${skill.minimum_count}` : ''}
        </p></div>
        <div className="dev-skill-action"><span className={`dev-skill-status dev-skill-${skill.status}`}>{statuses[skill.status]}</span>
          {skill.status === 'review' && lessonIndex >= 0 && <button className="dev-link" onClick={() => onSelectLesson(lessonIndex)}>{c.openLesson} →</button>}
        </div>
      </li>;
    })}</ul>
    {skills.some((skill) => skill.provisional && skill.count > 0) && <p className="dev-note">{c.singleQuestionNote}</p>}
  </section>;
}
