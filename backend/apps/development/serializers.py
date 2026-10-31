from rest_framework import serializers
from django.db.models.query import prefetch_related_objects

from .models import DevelopmentExercise
from .progress import can_postcheck, current_question, live_check
from .recommendations import learning_focus, module_analysis
from .translations import ContentLocale


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


def public_question(question, locale=None):
    if question is None:
        return None
    translated=locale.exercise(question['key']) if locale else None
    return {
        'key': question['key'], 'skill_key': question['skill_key'], 'format': question['format'],
        'prompt': translated['prompt'] if translated else question['prompt_uz'],
        'content_language': locale.language if locale else 'uz',
        'options': [{'id': option['id'], 'text': translated['options'][option['id']]['text'] if translated else option['text_uz']} for option in question['options']],
    }


def module_card(module, enrollment=None, language='uz'):
    prefetch_related_objects([module], 'skills', 'lessons')
    locale=ContentLocale(module,language)
    return {
        'key': module.key, 'version': module.version, 'title': locale.title(module),
        'order': module.order, 'cluster': module.cluster, 'topic_number': f'{module.cluster}.{module.order}',
        'skill_titles': [locale.skill(row.key,row.title_uz) for row in sorted(module.skills.all(), key=lambda skill: next(
            (lesson.order for lesson in module.lessons.all() if lesson.skill_id == skill.pk), 0))],
        'content_language': locale.language, 'indicator_keys': module.indicator_keys,
        'enrollment_id': enrollment.pk if enrollment else None,
        'stage': enrollment.stage if enrollment else None,
    }


def feedback(session, answer, language='uz'):
    question = next(q for q in session.question_snapshot if q['id'] == answer.exercise_id)
    locale=ContentLocale(session.enrollment.module,language)
    translated=locale.exercise(question['key'])
    option = next((o for o in question['options'] if o['id'] == answer.response.get('option_id')), None)
    correct_option = next((o for o in question['options'] if o['id'] == question['answer_key'].get('option_id')), None)
    return {
        'exercise_key': question['key'], 'skill_key': question['skill_key'],
        'prompt': translated['prompt'] if translated else question['prompt_uz'], 'content_language':locale.language,
        'response': answer.response, 'correct': answer.correctness == 1, 'hint_used': answer.hint_used,
        'solution_steps': translated['solution_steps'] if translated else question['solution_steps_uz'],
        'explanation': (translated['options'][option['id']]['feedback'] if option else translated['common_error']) if translated else (option['feedback_uz'] if option else question['common_error_uz']),
        'answer': (translated['options'][correct_option['id']]['text'] if translated else correct_option['text_uz']) if correct_option else question['answer_key'].get('value'),
    }


def session_state(session, language='uz'):
    completed = session.status == 'completed'
    total = len(session.question_snapshot)
    answered = session.answers.values('exercise_id').distinct().count()
    locale=ContentLocale(session.enrollment.module,language)
    question=current_question(session) if not completed else None
    result = {
        'id': session.pk, 'purpose': session.purpose, 'number': session.number, 'status': session.status,
        'answered': answered, 'total': total, 'score': float(session.score) if completed else None,
        'can_finish': not completed and answered == total,
        'question': public_question(question,locale), 'content_language':locale.language,
    }
    if completed and not live_check(session.enrollment):
        result['review'] = [feedback(session, answer,language) for answer in session.answers.order_by('answered_at', 'pk')]
    elif session.purpose=='practice' and not live_check(session.enrollment):
        previous=session.answers.order_by('-answered_at','-pk').first()
        if previous:result['last_feedback']=feedback(session,previous,language)
        if question and question['key'] in session.hint_usage:
            translated=locale.exercise(question['key'])
            result['question']['hint']=translated['hint'] if translated else question['hint_uz']
    return result


def enrollment_state(enrollment, language='uz'):
    active = enrollment.sessions.filter(status='in_progress').first()
    checks = list(enrollment.sessions.filter(status='completed', purpose__in=['precheck', 'postcheck']).order_by('pk'))
    pre = next((s for s in checks if s.purpose == 'precheck'), None)
    post = next((s for s in checks if s.purpose == 'postcheck'), None)
    hide_lessons = enrollment.stage == 'precheck' or live_check(enrollment)
    focus = {'focus_lesson_keys': [], 'required_lesson_keys': []} if hide_lessons else learning_focus(enrollment)
    other_active = enrollment.student.development_enrollments.filter(
        sessions__status='in_progress').exclude(pk=enrollment.pk).values_list('pk', flat=True).first()
    locale=ContentLocale(enrollment.module,language)
    def lesson_card(lesson):
        translated=locale.lesson(lesson.key)
        original=lesson.worked_example_uz
        example=translated['worked_example'] if translated else {'prompt':original['prompt_uz'],'solution_steps':original['solution_steps_uz'],'answer':original['answer_uz']}
        return {'key':lesson.key,'title':translated['title'] if translated else lesson.title_uz,'skill_key':lesson.skill.key,
                'theory':translated['theory'] if translated else lesson.theory_uz,
                'worked_example':{'prompt_uz':example['prompt'],'solution_steps_uz':example['solution_steps'],
                                  'answer_uz':example['answer'],**example},'content_language':locale.language}
    return {
        'id': enrollment.pk, 'module': module_card(enrollment.module, enrollment,language), 'stage': enrollment.stage,
        'completed_lesson_keys': enrollment.completed_lesson_keys,
        'lesson_count': enrollment.module.lessons.count(),
        'practice_completed': enrollment.sessions.filter(purpose='practice', status='completed').exists(),
        **focus,
        'skill_progress': [] if hide_lessons else locale.progress(module_analysis(enrollment.student, enrollment.module, enrollment)),
        'other_active_enrollment_id': other_active,
        'learning_locked': live_check(enrollment),
        'notation': [] if live_check(enrollment) else locale.notation(enrollment.module),
        'projects': [] if hide_lessons else locale.projects(enrollment.module),
        'lessons': [] if hide_lessons else [
            lesson_card(lesson)
            for lesson in enrollment.module.lessons.select_related('skill').order_by('order')
        ],
        'active_session': session_state(active,language) if active else None,
        'can_postcheck': not live_check(enrollment) and can_postcheck(enrollment), 'check_bank_exhausted': post is not None,
        'precheck_score': float(pre.score) if pre else None,
        'postcheck_score': float(post.score) if post else None,
        'delta_percentage_points': float(post.score - pre.score) if post and pre else None,
        'checks': [session_state(s,language) for s in checks],
    }
