"""Server-owned learning flow. Always lock enrollment before session on writes."""

from copy import deepcopy
from decimal import Decimal

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import Max
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import APIException

from apps.assessments.models import AssessmentAttempt
from apps.scoring.models import IndicatorScore, StudentAbilityEstimate
from .grading import grade
from .recommendations import enrollment_reason, learning_focus
from .models import DevelopmentAnswer, DevelopmentEnrollment, DevelopmentExercise, DevelopmentModule, DevelopmentSession


class FlowError(APIException):
    status_code = 409
    default_code = 'development_conflict'

    def __init__(self, code):
        self.flow_code = code
        super().__init__(code)


ERRORS = {
    'uz': {
        'stage_locked': 'Avval oldingi bosqichni yakunlang.',
        'active_session': 'Avval davom etayotgan mashg‘ulotni yakunlang.',
        'bank_exhausted': 'Yangi tekshiruv savollari hozircha tugadi. Mashqlarni davom ettirishingiz mumkin.',
        'incomplete': 'Yakunlashdan oldin barcha savollarga javob bering.',
        'wrong_question': 'Savol holati o‘zgargan. Joriy savolni qayta yuklang.',
        'idempotency_conflict': 'Bu yuborish kaliti boshqa javob uchun ishlatilgan.',
        'check_no_help': 'Tekshiruv davomida yordam va darslar ochilmaydi.',
        'session_completed': 'Bu mashg‘ulot yakunlangan.',
    },
    'ru': {
        'stage_locked': 'Сначала завершите предыдущий этап.',
        'active_session': 'Сначала завершите текущую сессию.',
        'bank_exhausted': 'Новые проверочные задания закончились. Можно продолжить тренировку.',
        'incomplete': 'Перед завершением ответьте на все вопросы.',
        'wrong_question': 'Состояние вопроса изменилось. Загрузите текущий вопрос.',
        'idempotency_conflict': 'Этот ключ отправки уже использован для другого ответа.',
        'check_no_help': 'Во время проверки помощь и уроки недоступны.',
        'session_completed': 'Эта сессия уже завершена.',
    },
}


def live_check(enrollment):
    return DevelopmentSession.objects.filter(enrollment__student_id=enrollment.student_id,
        status='in_progress', purpose__in=['precheck', 'postcheck']).exists()


def can_postcheck(enrollment):
    if enrollment.sessions.filter(purpose='postcheck').exists():
        return False
    if enrollment.sessions.filter(purpose='precheck', status='completed', score__gte=80).exists():
        return True
    for session in enrollment.sessions.filter(purpose='practice', status='completed').order_by('-number'):
        answers = list(session.answers.filter(attempt_number=1).order_by('-answered_at', '-pk')[:5])
        if len(answers) == 5 and sum(a.correctness == 1 and not a.hint_used for a in answers) >= 4:
            return True
    return False


def diagnostic_snapshot(student, module):
    return {
        'captured_at': timezone.now().isoformat(),
        'scores': [
            {'indicator_key': row.indicator_key, 'score': row.score, 'computed_at': row.computed_at.isoformat()}
            for row in IndicatorScore.objects.filter(student=student, indicator_key__in=module.indicator_keys)
        ],
        'ability_estimates': [
            {'indicator_key': row.indicator_key, 'theta': row.theta, 'se': row.se,
             'estimation_method': row.estimation_method, 'updated_at': row.updated_at.isoformat()}
            for row in StudentAbilityEstimate.objects.filter(student=student, indicator_key__in=module.indicator_keys)
        ],
        'attempts': [
            {'id': row.pk, 'assessment_type': row.assessment_type, 'cycle': row.attempt_cycle,
             'status': row.status, 'completed_at': row.completed_at.isoformat() if row.completed_at else None}
            for row in AssessmentAttempt.objects.filter(student=student, assessment_type__in=module.indicator_keys)
        ],
    }


@transaction.atomic
def enroll(student, module_key):
    get_user_model().objects.select_for_update().get(pk=student.pk)
    # An existing enrollment stays pinned even if a newer version is published.
    existing = DevelopmentEnrollment.objects.filter(student=student, module__key=module_key).order_by('-module__version').first()
    if existing:
        return existing
    module = DevelopmentModule.objects.select_for_update().filter(status='published', key=module_key).order_by('-version').first()
    if module is None:
        raise Http404
    enrollment, _ = DevelopmentEnrollment.objects.get_or_create(student=student, module=module, defaults={
        'diagnostic_snapshot': diagnostic_snapshot(student, module),
        'recommendation_reason': enrollment_reason(student, module),
    })
    return enrollment


def locked_enrollment(student, enrollment_id):
    return get_object_or_404(DevelopmentEnrollment.objects.select_for_update().select_related('module'), pk=enrollment_id, student=student)


@transaction.atomic
def complete_lesson(student, enrollment_id, lesson_key):
    enrollment = locked_enrollment(student, enrollment_id)
    if enrollment.stage == 'precheck' or live_check(enrollment):
        raise FlowError('check_no_help')
    get_object_or_404(enrollment.module.lessons, key=lesson_key)
    if lesson_key not in enrollment.completed_lesson_keys:
        enrollment.completed_lesson_keys.append(lesson_key)
    if enrollment.stage == 'study' and set(enrollment.completed_lesson_keys) >= set(learning_focus(enrollment)['required_lesson_keys']):
        enrollment.stage = 'practice'
    enrollment.save(update_fields=['completed_lesson_keys', 'stage', 'updated_at'])
    return enrollment


def snapshot_question(exercise):
    return {
        'id': exercise.pk, 'key': exercise.key, 'skill_key': exercise.skill.key,
        **{field: deepcopy(getattr(exercise, field)) for field in (
            'format', 'prompt_uz', 'options', 'answer_key', 'solution_steps_uz', 'hint_uz', 'common_error_uz',
        )},
    }


@transaction.atomic
def start_session(student, enrollment_id, purpose):
    get_user_model().objects.select_for_update().get(pk=student.pk)
    enrollment = locked_enrollment(student, enrollment_id)
    active = enrollment.sessions.filter(status='in_progress').first()
    if active:
        if active.purpose != purpose:
            raise FlowError('active_session')
        return active
    if DevelopmentSession.objects.filter(enrollment__student=student, status='in_progress').exclude(enrollment=enrollment).exists():
        raise FlowError('active_session')
    if purpose in {'precheck', 'postcheck'} and enrollment.sessions.filter(purpose=purpose).exists():
        raise FlowError('bank_exhausted')
    if purpose == 'precheck':
        allowed = enrollment.stage == 'precheck'
    elif purpose == 'postcheck':
        allowed = can_postcheck(enrollment)
    else:
        precheck = enrollment.sessions.filter(purpose='precheck', status='completed').first()
        allowed = bool(precheck and (precheck.score >= 80 or enrollment.stage in {'practice', 'postcheck', 'completed'}))
    if not allowed:
        raise FlowError('stage_locked')
    keys = enrollment.module.blueprint[purpose + '_order']
    pool = {q.key: q for q in enrollment.module.exercises.filter(key__in=keys).select_related('skill')}
    number = (enrollment.sessions.filter(purpose=purpose).aggregate(value=Max('number'))['value'] or 0) + 1
    session = DevelopmentSession.objects.create(enrollment=enrollment, purpose=purpose, number=number,
        question_snapshot=[snapshot_question(pool[key]) for key in keys])
    return session


def current_question(session):
    answered = set(session.answers.values_list('exercise_id', flat=True))
    return next((q for q in session.question_snapshot if q['id'] not in answered), None)


def lock_session(student, session_id):
    parent = get_object_or_404(DevelopmentSession.objects.filter(enrollment__student=student), pk=session_id)
    enrollment = locked_enrollment(student, parent.enrollment_id)
    session = DevelopmentSession.objects.select_for_update().get(pk=parent.pk)
    session.enrollment = enrollment
    return session


@transaction.atomic
def submit_answer(student, session_id, *, exercise_key, response, idempotency_key, language='uz'):
    session = lock_session(student, session_id)
    previous = session.answers.filter(idempotency_key=idempotency_key).select_related('exercise').first()
    if previous:
        if previous.exercise.key != exercise_key or previous.response != response:
            raise FlowError('idempotency_conflict')
        return session, previous
    if session.status != 'in_progress':
        raise FlowError('session_completed')
    question = current_question(session)
    if not question or question['key'] != exercise_key:
        raise FlowError('wrong_question')
    correctness = grade(question, response, language)
    answer = DevelopmentAnswer.objects.create(session=session, exercise_id=question['id'], response=response,
        correctness=correctness, idempotency_key=idempotency_key, hint_used=exercise_key in session.hint_usage)
    return session, answer


@transaction.atomic
def request_hint(student, session_id, exercise_key):
    session = lock_session(student, session_id)
    if session.purpose != 'practice' or live_check(session.enrollment):
        raise FlowError('check_no_help')
    if session.status != 'in_progress':
        raise FlowError('session_completed')
    question = current_question(session)
    if not question or question['key'] != exercise_key:
        raise FlowError('wrong_question')
    session.hint_usage.setdefault(exercise_key, timezone.now().isoformat())
    session.save(update_fields=['hint_usage'])
    return question['hint_uz']


@transaction.atomic
def finish_session(student, session_id):
    session = lock_session(student, session_id)
    if session.status == 'completed':
        return session
    if current_question(session) is not None:
        raise FlowError('incomplete')
    answers = list(session.answers.all())
    session.score = (Decimal(sum(a.correctness == 1 for a in answers)) * 100 / len(session.question_snapshot)).quantize(Decimal('0.01'))
    session.status = 'completed'
    session.completed_at = timezone.now()
    session.save(update_fields=['score', 'status', 'completed_at'])
    enrollment = session.enrollment
    if session.purpose == 'precheck':
        enrollment.stage = 'postcheck' if session.score >= 80 else 'study'
    elif session.purpose == 'postcheck':
        enrollment.stage = 'completed' if session.score >= 80 else 'practice'
        enrollment.completed_at = timezone.now() if session.score >= 80 else None
    elif enrollment.stage != 'completed':
        enrollment.stage = 'postcheck' if can_postcheck(enrollment) else 'practice'
    enrollment.save(update_fields=['stage', 'completed_at', 'updated_at'])
    return session
