import { useEffect, useRef, useState } from 'react';

import {
  answerDevelopmentQuestion, completeDevelopmentLesson, enrollDevelopment, finishDevelopmentSession,
  getDevelopmentCapabilities, getDevelopmentEnrollment, getDevelopmentHint, getDevelopmentPlan, startDevelopmentSession,
} from '../../api/development.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import LanguageSwitcher from '../../components/LanguageSwitcher.jsx';
import PlanOverview from './PlanOverview.jsx';
import SkillProgress from './SkillProgress.jsx';
import { developmentCopy } from './copy.js';
import './development.css';

const steps = ['precheck', 'study', 'practice', 'postcheck', 'completed'];

export default function DevelopmentPage({ user, goTo }) {
  const { language } = useLanguage();
  const c = developmentCopy[language];
  const [modules, setModules] = useState([]);
  const [plan, setPlan] = useState(null);
  const [available, setAvailable] = useState(false);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [enrollment, setEnrollment] = useState(null);
  const [session, setSession] = useState(null);
  const [lessonIndex, setLessonIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [hint, setHint] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [loadVersion, setLoadVersion] = useState(0);
  const [expandedExamples, setExpandedExamples] = useState([]);
  const pending = useRef(null);
  const questionHeading = useRef(null);
  const lessonHeading = useRef(null);
  const currentLanguage = useRef(language);
  currentLanguage.current = language;
  const selectedKey = `mindmetric-development:${user.id}`;
  const submissionKey = (id) => `${selectedKey}:submission:${id}`;

  const applyEnrollment = (data, preserved = {}) => {
    setEnrollment(data);
    setSession(data.active_session);
    const previous = data.active_session?.last_feedback;
    setFeedback(previous && previous.exercise_key === preserved.feedbackKey ? previous : null);
    setHint(data.active_session?.question?.hint || '');
    const preferred = preserved.lessonKey || data.focus_lesson_keys?.find((key) => !data.completed_lesson_keys.includes(key));
    setLessonIndex(Math.max(0, data.lessons.findIndex((lesson) => lesson.key === preferred)));
    sessionStorage.setItem(selectedKey, String(data.id));
  };

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        const caps = await getDevelopmentCapabilities();
        if (cancelled) return;
        setAvailable(caps.available);
        if (!caps.available) return;
        const result = await getDevelopmentPlan();
        if (cancelled) return;
        setModules(result.modules);
        setPlan(result);
        const saved = sessionStorage.getItem(selectedKey);
        if (saved && /^\d+$/.test(saved)) {
          let data;
          try { data = await getDevelopmentEnrollment(saved); }
          catch (err) {
            if (err.status === 404) sessionStorage.removeItem(selectedKey);
            else throw err;
          }
          if (!cancelled && data) applyEnrollment(data, {
            lessonKey: enrollment?.lessons[lessonIndex]?.key,
            feedbackKey: feedback?.exercise_key,
          });
        }
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [selectedKey, language, loadVersion]);

  useEffect(() => {
    if (!session) return;
    let saved = null;
    try { saved = JSON.parse(sessionStorage.getItem(submissionKey(session.id))); } catch { /* discard invalid local draft */ }
    if (saved && saved.exercise_key === session.question?.key && typeof saved.idempotency_key === 'string'
      && saved.response && typeof (saved.response.value ?? saved.response.option_id) === 'string') {
      pending.current = saved;
      setAnswer(saved.response.value ?? saved.response.option_id ?? '');
    } else {
      pending.current = null;
      sessionStorage.removeItem(submissionKey(session.id));
      setAnswer('');
    }
    setHint(session.question?.hint || '');
    questionHeading.current?.focus();
  }, [session?.id, session?.question?.key]);

  const perform = async (action) => {
    const actionLanguage = language;
    setBusy(true);
    setError('');
    try { await action(); } catch (err) { setError(err.message); } finally {
      setBusy(false);
      if (currentLanguage.current !== actionLanguage) setLoadVersion((old) => old + 1);
    }
  };

  const start = (purpose) => perform(async () => {
    const data = await startDevelopmentSession(enrollment.id, purpose);
    setSession(data);
    setEnrollment((old) => ({ ...old, lessons: [] }));
    setFeedback(null);
  });

  const openModule = (module) => perform(async () => {
    const data = module.enrollment_id ? await getDevelopmentEnrollment(module.enrollment_id) : await enrollDevelopment(module.key);
    applyEnrollment(data);
  });

  const selectLesson = (index) => {
    setLessonIndex(index);
    requestAnimationFrame(() => lessonHeading.current?.focus());
  };

  const submit = (event) => {
    event.preventDefault();
    if (busy) return;
    perform(async () => {
      if (!pending.current) {
        pending.current = {
          exercise_key: session.question.key, idempotency_key: crypto.randomUUID(),
          response: session.question.format === 'numeric' ? { value: answer } : { option_id: answer },
        };
        sessionStorage.setItem(submissionKey(session.id), JSON.stringify(pending.current));
      }
      let result;
      try {
        result = await answerDevelopmentQuestion(session.id, pending.current);
      } catch (err) {
        if (err.status === 400) {
          sessionStorage.removeItem(submissionKey(session.id));
          pending.current = null;
        }
        throw err;
      }
      sessionStorage.removeItem(submissionKey(session.id));
      pending.current = null;
      setSession(result.session);
      setFeedback(result.feedback || null);
      setHint('');
      setAnswer('');
    });
  };

  const leaveModule = () => {
    sessionStorage.removeItem(selectedKey);
    setEnrollment(null); setSession(null); setFeedback(null); setError('');
    setLoadVersion((old) => old + 1);
  };

  const stage = session ? session.purpose : enrollment?.stage;
  const currentStep = steps.indexOf(stage);
  const finishedSteps = enrollment ? {
    precheck: enrollment.precheck_score !== null,
    study: enrollment.required_lesson_keys?.length
      ? enrollment.required_lesson_keys.every((key) => enrollment.completed_lesson_keys.includes(key))
      : enrollment.completed_lesson_keys.length >= enrollment.lesson_count,
    practice: enrollment.practice_completed,
    postcheck: enrollment.postcheck_score !== null,
    completed: enrollment.stage === 'completed',
  } : {};
  const question = session?.question;
  const contentLanguage = enrollment?.module.content_language || 'uz';
  const contentLabel = (lang) => lang === 'ru' ? c.languageRu : c.language;

  return <div className="mm-dev">
    <header className="dev-heading">
      <div><p className="dev-eyebrow">{c.eyebrow}</p><h1>{c.title}</h1><p>{c.intro}</p></div>
      <div className="dev-heading-actions"><LanguageSwitcher compact /><button className="dev-link" onClick={() => enrollment ? leaveModule() : goTo('selection')} disabled={busy}>
        ← {enrollment ? c.catalogue : c.back}
      </button></div>
    </header>

    {error && <div className="dev-error" role="alert"><p>{error}</p>
      <button className="dev-link" disabled={busy} onClick={() => {
        if (enrollment) perform(async () => applyEnrollment(await getDevelopmentEnrollment(enrollment.id)));
        else setLoadVersion((old) => old + 1);
      }}>{c.refresh}</button>
    </div>}
    {loading ? <p role="status">{c.loading}</p> : !available ? <div className="dev-panel"><p>{c.unavailable}</p></div> : <>
      {!enrollment ? <>
        <PlanOverview plan={plan} c={c} busy={busy} onOpen={openModule} />
        <section className="dev-intro"><p className="dev-eyebrow">{c.cluster}</p><h2>{c.overview}</h2>
          <p>{c.description}</p><div className="dev-symbols" aria-hidden="true">a² <span>+</span> √x <span>→</span> x = ?</div>
        </section>
        {modules.length === 0 && <p>{c.empty}</p>}
        <div className="dev-module-grid">{modules.map((module) => <article className="dev-panel dev-module" key={module.key}>
          <p className="dev-eyebrow">{c.module} / 1.{module.order}</p><h2 lang={module.content_language}>{module.title}</h2>
          <p lang={module.content_language}>{module.skill_titles?.join(' · ')}</p><p>{c.precheckReady}</p>
          <p className="dev-language">{contentLabel(module.content_language)}</p>
          {module.stage && <span className="dev-chip">{c[module.stage]}</span>}
          <p className="dev-note">{module.recommendation?.reason}</p>
          <button className="dev-button" disabled={busy} onClick={() => openModule(module)}>{module.enrollment_id ? c.resume : c.start} →</button>
        </article>)}</div>
      </> : <>
        <div className="dev-module-title"><h2 lang={contentLanguage}>{enrollment.module.title}</h2><span className="dev-language">{contentLabel(contentLanguage)}</span></div>
        <ol className="dev-steps" aria-label={c.overview}>{steps.map((key, index) => <li key={key}
          aria-current={index === currentStep ? 'step' : undefined} className={finishedSteps[key] ? 'is-done' : ''}>
          <span>{finishedSteps[key] ? '✓' : String(index + 1).padStart(2, '0')}</span>{c[key]}</li>)}</ol>

        {session ? <section className="dev-panel dev-exercise" aria-busy={busy}>
          <div className="dev-exercise-top"><span className="dev-eyebrow">{c[session.purpose]}</span>
            <span>{session.answered} {c.of} {session.total}</span></div>
          <progress max={session.total} value={session.answered} aria-label={c[session.purpose]} />
          <p className="dev-note">{c[`${session.purpose}Note`]}</p>
          {session.purpose === 'practice' && session.number > 1 && <p className="dev-note">{c.rehearsalNote}</p>}
          {feedback ? <div className={`dev-feedback ${feedback.correct ? 'is-correct' : ''}`} aria-live="polite">
            <h3>{feedback.correct ? c.correct : c.incorrect}</h3><p className="dev-math" lang={feedback.content_language || contentLanguage}>{feedback.prompt}</p>
            <p lang={feedback.content_language || contentLanguage}>{feedback.explanation}</p><ol lang={feedback.content_language || contentLanguage}>{feedback.solution_steps.map((line, i) => <li key={i}>{line}</li>)}</ol>
            <p><strong>{c.correctAnswer}: </strong><span className="dev-math" lang={feedback.content_language || contentLanguage}>{feedback.answer}</span></p>
            {feedback.hint_used && <p>{c.hintUsed}</p>}
            <button className="dev-button" onClick={() => setFeedback(null)}>{c.next} →</button>
          </div> : question ? <form onSubmit={submit}>
            <h3 className="dev-question dev-math" ref={questionHeading} tabIndex={-1} lang={question.content_language}>{question.prompt}</h3>
            {question.format === 'numeric' ? <label className="dev-answer-label">{c.answer}
              <input autoComplete="off" type="text" inputMode="text" maxLength={80} required value={answer}
                disabled={busy || Boolean(pending.current)} onChange={(event) => setAnswer(event.target.value)} placeholder={c.answerPlaceholder} />
            </label> : <fieldset disabled={busy || Boolean(pending.current)}><legend>{c.choose}</legend>
              {question.options.map((option) => <label className={`dev-option ${answer === option.id ? 'is-selected' : ''}`} key={option.id}>
                <input type="radio" name={question.key} value={option.id} required checked={answer === option.id}
                  onChange={() => setAnswer(option.id)} /><span lang={question.content_language}>{option.text}</span>
              </label>)}
            </fieldset>}
            {hint && <p className="dev-hint" role="status" lang={question.content_language}>{hint}</p>}
            <div className="dev-actions"><button type="submit" className="dev-button" disabled={busy || !answer.trim()}>
              {busy ? c.sending : pending.current ? c.retrySubmit : c.submit}</button>
              {session.purpose === 'practice' && <button type="button" className="dev-link" disabled={busy || Boolean(pending.current)} onClick={() => perform(async () => {
                const result = await getDevelopmentHint(session.id, question.key); setHint(result.hint);
              })}>{c.hint}</button>}
            </div>
          </form> : <div className="dev-finish"><h3>{c.allAnswered}</h3><button className="dev-button" disabled={busy || !session.can_finish}
            onClick={() => perform(async () => {
              const result = await finishDevelopmentSession(session.id); applyEnrollment(result.enrollment);
            })}>{c.finish} →</button></div>}
        </section> : <>
          {enrollment.other_active_enrollment_id && <div className="dev-hint"><p>{c.otherSession}</p>
            <button className="dev-link" disabled={busy} onClick={() => perform(async () => {
              applyEnrollment(await getDevelopmentEnrollment(enrollment.other_active_enrollment_id));
            })}>{c.returnToSession} →</button>
          </div>}
          {enrollment.precheck_score !== null && <section className="dev-panel dev-results">
            <h3>{c.results}</h3><div className="dev-metrics">
              <div><span>{c.baseline}</span><strong>{enrollment.precheck_score}%</strong></div>
              <div><span>{c.final}</span><strong>{enrollment.postcheck_score === null ? '—' : `${enrollment.postcheck_score}%`}</strong></div>
              <div><span>{c.delta}</span><strong>{enrollment.delta_percentage_points === null ? '—' : `${enrollment.delta_percentage_points > 0 ? '+' : ''}${enrollment.delta_percentage_points}`}</strong><small>{c.points}</small></div>
            </div><p className="dev-note">{c.limit}</p>
          </section>}
          {!enrollment.learning_locked && <SkillProgress skills={enrollment.skill_progress} lessons={enrollment.lessons}
            c={c} onSelectLesson={selectLesson} />}
          {!enrollment.learning_locked && enrollment.focus_lesson_keys?.length > 0 && <div className="dev-focus-list">
            <strong>{c.focusedLessons}</strong>{enrollment.focus_lesson_keys.map((key) => {
              const index = enrollment.lessons.findIndex((lesson) => lesson.key === key);
              return index < 0 ? null : <button key={key} className="dev-link" lang={enrollment.lessons[index].content_language} onClick={() => selectLesson(index)}>{enrollment.lessons[index].title} →</button>;
            })}
          </div>}
          {enrollment.check_bank_exhausted && enrollment.stage !== 'completed' && <p className="dev-hint">{c.exhausted}</p>}
          <div className="dev-actions dev-main-actions">
            {enrollment.stage === 'precheck' && <button className="dev-button" disabled={busy || Boolean(enrollment.other_active_enrollment_id)} onClick={() => start('precheck')}>{c.startPrecheck} →</button>}
            {enrollment.can_postcheck && <button className="dev-button" disabled={busy || Boolean(enrollment.other_active_enrollment_id)} onClick={() => start('postcheck')}>{c.startPostcheck} →</button>}
            {['practice', 'postcheck', 'completed'].includes(enrollment.stage) && <button className="dev-button dev-button-secondary" disabled={busy || Boolean(enrollment.other_active_enrollment_id)} onClick={() => start('practice')}>
              {enrollment.check_bank_exhausted ? c.morePractice : c.startPractice}</button>}
          </div>
          {enrollment.lessons.length > 0 && <section className="dev-study">
            <nav className="dev-lesson-nav" aria-label={c.study}>{enrollment.lessons.map((lesson, index) => <button key={lesson.key}
              aria-current={index === lessonIndex ? 'true' : undefined} onClick={() => setLessonIndex(index)}>
              <span>{enrollment.completed_lesson_keys.includes(lesson.key) ? '✓' : String(index + 1).padStart(2, '0')}</span><span lang={lesson.content_language}>{lesson.title}
                {enrollment.focus_lesson_keys?.includes(lesson.key) && <small lang={language}>{c.focusedLesson}</small>}</span>
            </button>)}</nav>
            {enrollment.lessons[lessonIndex] && (() => {
              const lesson = enrollment.lessons[lessonIndex];
              const done = enrollment.completed_lesson_keys.includes(lesson.key);
              return <article className="dev-panel dev-lesson" lang={lesson.content_language}><p className="dev-eyebrow">{c.study} / {lessonIndex + 1}</p>
                <h3 ref={lessonHeading} tabIndex={-1}>{lesson.title}</h3>{lesson.theory.map((line, index) => <p key={index}>{line}</p>)}
                <details className="dev-example" open={expandedExamples.includes(lesson.key)} onToggle={(event) => {
                  const open = event.currentTarget.open;
                  setExpandedExamples((keys) => open ? (keys.includes(lesson.key) ? keys : [...keys, lesson.key]) : keys.filter((key) => key !== lesson.key));
                }}><summary>{c.example}</summary><p className="dev-math">{lesson.worked_example.prompt ?? lesson.worked_example.prompt_uz}</p>
                  <ol>{(lesson.worked_example.solution_steps ?? lesson.worked_example.solution_steps_uz).map((line, index) => <li key={index}>{line}</li>)}</ol>
                  <strong className="dev-math">{lesson.worked_example.answer ?? lesson.worked_example.answer_uz}</strong>
                </details>
                <button className="dev-button" disabled={busy || done} onClick={() => perform(async () => {
                  const data = await completeDevelopmentLesson(enrollment.id, lesson.key);
                  applyEnrollment(data);
                  const next = data.focus_lesson_keys.find((key) => !data.completed_lesson_keys.includes(key));
                  setLessonIndex(next ? data.lessons.findIndex((item) => item.key === next) : Math.min(lessonIndex + 1, data.lessons.length - 1));
                })}>{done ? `✓ ${c.done}` : c.lessonDone} →</button>
              </article>;
            })()}
          </section>}
          {enrollment.checks.length > 0 && <details className="dev-panel dev-review"><summary>{c.mistakes}</summary>
            {enrollment.checks.map((check) => <section key={check.id}><h3>{c[check.purpose]} · {check.score}%</h3>
              {check.review?.map((item) => <details key={item.exercise_key}><summary lang={item.content_language || contentLanguage}>{item.correct ? '✓' : '○'} {item.prompt}</summary>
                <ol lang={item.content_language || contentLanguage}>{item.solution_steps.map((line, index) => <li key={index}>{line}</li>)}</ol></details>)}
            </section>)}
          </details>}
        </>}
      </>}
    </>}
  </div>;
}
