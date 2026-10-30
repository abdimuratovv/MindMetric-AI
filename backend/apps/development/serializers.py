from rest_framework import serializers
from django.db.models.query import prefetch_related_objects

from .models import DevelopmentExercise
from .progress import can_postcheck, current_question, live_check
from .recommendations import learning_focus, module_analysis


class StrictSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        if not isinstance(data, dict) or set(data) - set(self.fields):
            raise serializers.ValidationError({'detail': 'So‘rov maydonlari noto‘g‘ri.'})
        return super().to_internal_value(data)


class StartSessionSerializer(StrictSerializer):
    purpose = serializers.ChoiceField(choices=DevelopmentExercise.Purpose.choices)


class AnswerSerializer(StrictSerializer):
    exercise_key = serializers.SlugField(max_length=64)
    response = serializers.JSONField()
    idempotency_key = serializers.UUIDField()


class HintSerializer(StrictSerializer):
    exercise_key = serializers.SlugField(max_length=64)


def public_question(question):
    if question is None:
        return None
    return {
        'key': question['key'], 'skill_key': question['skill_key'], 'format': question['format'],
        'prompt': question['prompt_uz'], 'content_language': 'uz',
        'options': [{'id': option['id'], 'text': option['text_uz']} for option in question['options']],
    }


def module_card(module, enrollment=None):
    prefetch_related_objects([module], 'skills', 'lessons')
    return {
        'key': module.key, 'version': module.version, 'title': module.title_uz,
        'order': module.order,
        'skill_titles': [row.title_uz for row in sorted(module.skills.all(), key=lambda skill: next(
            (lesson.order for lesson in module.lessons.all() if lesson.skill_id == skill.pk), 0))],
        'content_language': 'uz', 'indicator_keys': module.indicator_keys,
        'enrollment_id': enrollment.pk if enrollment else None,
        'stage': enrollment.stage if enrollment else None,
    }


def feedback(session, answer):
    question = next(q for q in session.question_snapshot if q['id'] == answer.exercise_id)
    option = next((o for o in question['options'] if o['id'] == answer.response.get('option_id')), None)
    correct_option = next((o for o in question['options'] if o['id'] == question['answer_key'].get('option_id')), None)
    return {
        'exercise_key': question['key'], 'skill_key': question['skill_key'], 'prompt': question['prompt_uz'],
        'response': answer.response, 'correct': answer.correctness == 1, 'hint_used': answer.hint_used,
        'solution_steps': question['solution_steps_uz'],
        'explanation': option['feedback_uz'] if option else question['common_error_uz'],
        'answer': correct_option['text_uz'] if correct_option else question['answer_key'].get('value'),
    }


def session_state(session):
    completed = session.status == 'completed'
    total = len(session.question_snapshot)
    answered = session.answers.values('exercise_id').distinct().count()
    result = {
        'id': session.pk, 'purpose': session.purpose, 'number': session.number, 'status': session.status,
        'answered': answered, 'total': total, 'score': float(session.score) if completed else None,
        'can_finish': not completed and answered == total,
        'question': public_question(current_question(session)) if not completed else None,
    }
    if completed and not live_check(session.enrollment):
        result['review'] = [feedback(session, answer) for answer in session.answers.order_by('answered_at', 'pk')]
    return result


def enrollment_state(enrollment):
    active = enrollment.sessions.filter(status='in_progress').first()
    checks = list(enrollment.sessions.filter(status='completed', purpose__in=['precheck', 'postcheck']).order_by('pk'))
    pre = next((s for s in checks if s.purpose == 'precheck'), None)
    post = next((s for s in checks if s.purpose == 'postcheck'), None)
    hide_lessons = enrollment.stage == 'precheck' or live_check(enrollment)
    focus = {'focus_lesson_keys': [], 'required_lesson_keys': []} if hide_lessons else learning_focus(enrollment)
    other_active = enrollment.student.development_enrollments.filter(
        sessions__status='in_progress').exclude(pk=enrollment.pk).values_list('pk', flat=True).first()
    return {
        'id': enrollment.pk, 'module': module_card(enrollment.module, enrollment), 'stage': enrollment.stage,
        'completed_lesson_keys': enrollment.completed_lesson_keys,
        'lesson_count': enrollment.module.lessons.count(),
        'practice_completed': enrollment.sessions.filter(purpose='practice', status='completed').exists(),
        **focus,
        'skill_progress': [] if hide_lessons else module_analysis(enrollment.student, enrollment.module, enrollment),
        'other_active_enrollment_id': other_active,
        'learning_locked': live_check(enrollment),
        'lessons': [] if hide_lessons else [
            {'key': lesson.key, 'title': lesson.title_uz, 'skill_key': lesson.skill.key,
             'theory': lesson.theory_uz, 'worked_example': lesson.worked_example_uz, 'content_language': 'uz'}
            for lesson in enrollment.module.lessons.select_related('skill').order_by('order')
        ],
        'active_session': session_state(active) if active else None,
        'can_postcheck': not live_check(enrollment) and can_postcheck(enrollment), 'check_bank_exhausted': post is not None,
        'precheck_score': float(pre.score) if pre else None,
        'postcheck_score': float(post.score) if post else None,
        'delta_percentage_points': float(post.score - pre.score) if post and pre else None,
        'checks': [session_state(s) for s in checks],
    }
