"""Explainable, read-only learning priorities; never write diagnostic scores."""

import math

from django.db.models import F
from django.db.models.query import prefetch_related_objects

from apps.assessments.models import AssessmentAttempt, CognitiveResponse
from apps.scoring.models import IndicatorScore
from .models import DevelopmentEnrollment, DevelopmentModule, DevelopmentSession


MIN_DIAGNOSTIC_RESPONSES = 3
POLICY_VERSION = 1

REASONS = {
    'uz': {
        'continue': 'Boshlangan modulni davom ettiring.',
        'continue_check': 'Davom etayotgan tekshiruvni yakunlang. Tafsilotlar undan keyin ochiladi.',
        'after_check': 'Shaxsiy tavsiyalar tekshiruv yakunlangach ochiladi.',
        'check_review': 'Mavzu tekshiruvidagi xatolardan kelib chiqib, belgilangan darslarni takrorlang.',
        'diagnostic_review': 'Mos ko‘nikma bo‘yicha kamida uchta joriy diagnostika javobida xatolar bor.',
        'verify': 'Aniq ko‘nikma bo‘yicha dalil yetarli emas. Avval boshlang‘ich tekshiruvni bajaring.',
        'no_diagnostic': 'Bu mavzuga mos diagnostika savoli yo‘q. Bilimingizni boshlang‘ich tekshiruvda aniqlang.',
        'mastered': 'Modul mezoni bajarilgan. Istasangiz mashqlarni takrorlashingiz mumkin.',
        'foundation': 'Boshqa tavsiya etilgan mavzu uchun avval shu tayanch ko‘nikmani takrorlash foydali.',
    },
    'ru': {
        'continue': 'Продолжите начатый модуль.',
        'continue_check': 'Завершите текущую проверку. Подробности откроются после неё.',
        'after_check': 'Персональные рекомендации откроются после завершения проверки.',
        'check_review': 'Повторите отмеченные уроки по ошибкам в проверке темы.',
        'diagnostic_review': 'В текущем завершённом тесте есть ошибки минимум среди трёх ответов по связанному навыку.',
        'verify': 'Данных по конкретному навыку недостаточно. Сначала пройдите входную проверку.',
        'no_diagnostic': 'В диагностике нет вопросов по этой теме. Начните со входной проверки.',
        'mastered': 'Критерий модуля выполнен. При желании можно повторить тренировку.',
        'foundation': 'Сначала полезно повторить этот базовый навык для другой рекомендованной темы.',
    },
}


def visible_catalogue(student):
    enrollments = {row.module.key: row for row in DevelopmentEnrollment.objects.filter(student=student)
                   .select_related('module').order_by('module__version')}
    selected = {}
    for module in DevelopmentModule.objects.filter(status='published').order_by('order', 'key', '-version'):
        selected.setdefault(module.key, module.pk)
    selected.update({key: row.module_id for key, row in enrollments.items()})
    modules = list(DevelopmentModule.objects.filter(pk__in=selected.values()).prefetch_related(
        'skills__prerequisites', 'skills__diagnostic_links', 'lessons',
    ).order_by('order', 'key'))
    for module in modules:
        if module.key in enrollments:
            enrollments[module.key].module = module
    return modules, enrollments


def current_diagnostic_rows(student, question_ids):
    return list(CognitiveResponse.objects.filter(
        attempt__student=student, attempt__status=AssessmentAttempt.Status.COMPLETED,
        cycle=F('attempt__attempt_cycle'), question_id__in=question_ids,
        question__indicator_key=F('attempt__assessment_type'),
    ).values('question_id', 'correctness', 'responded_at', 'question__indicator_key'))


def check_evidence(enrollment):
    """Use completed checks only, not practice or partial checks."""
    result = {}
    if enrollment is None:
        return result
    sessions = enrollment.sessions.filter(status='completed', purpose__in=['precheck', 'postcheck']).prefetch_related('answers').order_by('completed_at', 'pk')
    for session in sessions:
        by_id = {question['id']: question for question in session.question_snapshot}
        for answer in session.answers.all():
            question = by_id.get(answer.exercise_id)
            if answer.attempt_number != 1 or not question:
                continue
            result[question['skill_key']] = {
                'status': 'review' if answer.correctness < 1 else 'observed_success',
                'source': session.purpose, 'count': 1, 'minimum_count': None, 'provisional': True,
                'error_fraction': 1 - answer.correctness,
                '_time': session.completed_at or session.started_at,
            }
    return result


def module_analysis(student, module, enrollment=None, diagnostic_rows=None):
    prefetch_related_objects([module], 'skills__prerequisites', 'skills__diagnostic_links', 'lessons')
    lesson_order = {lesson.skill_id: lesson.order for lesson in module.lessons.all()}
    skills = sorted(module.skills.all(), key=lambda row: (lesson_order.get(row.pk, 0), row.key))
    checks = check_evidence(enrollment)
    if diagnostic_rows is None:
        question_ids = {link.question_id for skill in skills for link in skill.diagnostic_links.all()}
        diagnostic_rows = current_diagnostic_rows(student, question_ids)
    by_question = {row['question_id']: row for row in diagnostic_rows
                   if math.isfinite(row['correctness']) and 0 <= row['correctness'] <= 1}
    result = []
    for skill in skills:
        links = list(skill.diagnostic_links.all())
        samples = [by_question[link.question_id] for link in links if link.question_id in by_question
                   and by_question[link.question_id]['question__indicator_key'] in skill.indicator_keys]
        evidence = None
        if len(samples) >= MIN_DIAGNOSTIC_RESPONSES:
            loss = 1 - sum(row['correctness'] for row in samples) / len(samples)
            evidence = {
                'status': 'review' if loss > 0 else 'observed_success', 'source': 'diagnostic',
                'count': len(samples), 'minimum_count': MIN_DIAGNOSTIC_RESPONSES,
                'provisional': False, 'error_fraction': loss,
                '_time': max(row['responded_at'] for row in samples),
            }
        check = checks.get(skill.key)
        if check and (evidence is None or check['_time'] >= evidence['_time']):
            evidence = check.copy()
        if evidence is None:
            evidence = {'status': 'insufficient' if links else 'not_assessed',
                        'source': 'diagnostic' if links else 'none', 'count': len(samples),
                        'minimum_count': MIN_DIAGNOSTIC_RESPONSES if links else None,
                        'provisional': True, 'error_fraction': None, '_time': None}
        observed = evidence.pop('_time')
        evidence['observed_at'] = observed.isoformat() if observed else None
        if evidence['error_fraction'] is not None:
            evidence['error_fraction'] = round(evidence['error_fraction'], 6)
        result.append({'key': skill.key, 'title': skill.title_uz,
                       'prerequisite_keys': [row.key for row in skill.prerequisites.all()], **evidence})
    return result


def learning_focus(enrollment):
    """A check error is a learning signal; it is not a trait/IRT diagnosis."""
    module = enrollment.module
    prefetch_related_objects([module], 'skills__prerequisites', 'lessons')
    skills = {skill.key: skill for skill in module.skills.all()}
    keys_by_id = {skill.pk: skill.key for skill in skills.values()}
    lessons = list(module.lessons.all())
    evidence = check_evidence(enrollment)
    focus, visited = [], set()

    def visit(key):
        if key in visited or key not in skills:
            return
        visited.add(key)
        for parent in skills[key].prerequisites.all():
            if parent.key in skills and evidence.get(parent.key, {}).get('status') != 'observed_success':
                visit(parent.key)
        focus.extend(lesson.key for lesson in lessons if lesson.skill_id == skills[key].pk)

    for lesson in lessons:
        key = keys_by_id[lesson.skill_id]
        if evidence.get(key, {}).get('status') == 'review':
            visit(key)
    required = list(focus)
    precheck = enrollment.sessions.filter(purpose='precheck', status='completed').first()
    if precheck and precheck.score >= 80:
        required = []
    elif precheck and not required:
        required = [lesson.key for lesson in lessons]
    return {'focus_lesson_keys': focus, 'required_lesson_keys': required}


def build_plan(student, language='uz'):
    language = language if language in REASONS else 'uz'
    modules, enrollments = visible_catalogue(student)
    active = DevelopmentSession.objects.filter(enrollment__student=student, status='in_progress').order_by('started_at', 'pk').first()
    check_active = bool(active and active.purpose != 'practice')
    question_ids = {link.question_id for module in modules for skill in module.skills.all() for link in skill.diagnostic_links.all()}
    diagnostic = [] if check_active else current_diagnostic_rows(student, question_ids)
    completed_types = set(AssessmentAttempt.objects.filter(student=student, status='completed').values_list('assessment_type', flat=True))
    scores = {row.indicator_key: row.score for row in IndicatorScore.objects.filter(student=student, indicator_key__in=completed_types)}
    entries = []
    for module in modules:
        enrollment = enrollments.get(module.key)
        skills = [] if check_active else module_analysis(student, module, enrollment, diagnostic)
        weak = [row for row in skills if row['status'] == 'review']
        diagnostic_weak = [row for row in weak if row['source'] == 'diagnostic']
        active_here = bool(active and enrollment and active.enrollment_id == enrollment.pk)
        if active_here:
            code, action, bucket = ('continue_check' if check_active else 'continue'), 'resume', 0
        elif check_active:
            code, action, bucket = 'after_check', 'wait', 9
        elif enrollment and enrollment.stage != 'completed':
            code = 'check_review' if any(row['source'] in {'precheck', 'postcheck'} for row in weak) else 'continue'
            action, bucket = 'resume', 1
        elif diagnostic_weak:
            code, action, bucket = 'diagnostic_review', 'review' if enrollment else 'verify', 2
        elif enrollment and enrollment.stage == 'completed':
            code, action, bucket = 'mastered', 'review', 8
        else:
            has_links = any(skill.diagnostic_links.all() for skill in module.skills.all())
            code, action, bucket = ('verify' if has_links else 'no_diagnostic'), 'verify', 4
        # Indicator scores break ties only between already evidenced gaps; they
        # cannot create a gap or rank unrelated IQ/math topics as weak.
        relevant = {indicator for skill in module.skills.all() if any(row['key'] == skill.key for row in diagnostic_weak)
                    for indicator in skill.indicator_keys if indicator in scores}
        tie_score = min((scores[key] for key in relevant), default=100)
        rank = (bucket, -max((row['error_fraction'] for row in weak), default=0), tie_score, module.order, module.key)
        entries.append({'module': module, 'enrollment': enrollment, 'skills': skills,
                        'recommendation': {'code': code, 'action': action, 'reason': REASONS[language][code],
                                           'focus_skill_keys': [row['key'] for row in weak],
                                           'evidence_count': max((row['count'] for row in diagnostic_weak), default=0)},
                        '_rank': rank})
    by_key = {entry['module'].key: entry for entry in entries}
    owner = {row['key']: entry['module'].key for entry in entries for row in entry['skills']}
    skill_state = {row['key']: row for entry in entries for row in entry['skills']}
    selected, visited = [], set()

    def append(entry):
        key = entry['module'].key
        if key in visited or entry['_rank'][0] >= 8:
            return
        visited.add(key)
        if entry['_rank'][0] != 0:
            for skill in entry['skills']:
                if skill['status'] != 'review':
                    continue
                for parent in skill['prerequisite_keys']:
                    parent_key = owner.get(parent)
                    if parent_key != key and skill_state.get(parent, {}).get('status') == 'review':
                        foundation = by_key[parent_key]
                        append(foundation)
                        if foundation['recommendation']['action'] != 'resume':
                            foundation['recommendation']['code'] = 'foundation'
                            foundation['recommendation']['reason'] = REASONS[language]['foundation']
        selected.append(entry)

    for entry in sorted(entries, key=lambda row: row['_rank']):
        append(entry)
    return {'entries': entries, 'recommended': selected[:2], 'check_active': check_active,
            'active_enrollment_id': active.enrollment_id if active else None,
            'policy_version': POLICY_VERSION, 'minimum_diagnostic_responses': MIN_DIAGNOSTIC_RESPONSES}


def enrollment_reason(student, module):
    entry = next((row for row in build_plan(student)['entries'] if row['module'].pk == module.pk), None)
    if entry is None:
        return {'code': 'self_selected', 'policy_version': POLICY_VERSION}
    recommendation = entry['recommendation']
    return {key: recommendation[key] for key in ('code', 'focus_skill_keys', 'evidence_count')} | {'policy_version': POLICY_VERSION}
