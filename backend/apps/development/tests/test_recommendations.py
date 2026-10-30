import json
from copy import deepcopy
from datetime import timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection
from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import StudentProfile
from apps.assessments.content import MCQ_QUESTIONS
from apps.assessments.models import AssessmentAttempt, CognitiveQuestion, CognitiveResponse
from apps.development.content_loader import bundled_contents, import_bundle, publish_module
from apps.development.models import DevelopmentAnswer, DevelopmentEnrollment, DevelopmentModule, DevelopmentSession
from apps.development.progress import snapshot_question
from apps.development.recommendations import learning_focus
from apps.scoring.models import IndicatorScore
from .test_content import ContentDatabaseCase


@override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
class RecommendationTests(ContentDatabaseCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        contents = bundled_contents()
        keys = {link['question_key'] for data in contents for link in data['diagnostic_links']}
        for indicator, questions in MCQ_QUESTIONS.items():
            for question in questions:
                if question['key'] in keys:
                    CognitiveQuestion.objects.get_or_create(key=question['key'], defaults={
                        'indicator_key': indicator, **{key: value for key, value in question.items() if key != 'key'},
                    })
        for _, module, _ in import_bundle(deepcopy(contents)):
            publish_module(module.pk)
        cls.user = get_user_model().objects.create_user('plan@university.edu')
        cls.other = get_user_model().objects.create_user('other-plan@university.edu')
        for user in (cls.user, cls.other):
            StudentProfile.objects.create(user=user, completed_at=timezone.now())

    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def plan(self, language='uz'):
        response = self.client.get('/api/development/plan/', HTTP_X_LANGUAGE=language)
        self.assertEqual(response.status_code, 200, response.data)
        return response.data

    def entry(self, key='arithmetic-algebra'):
        return next(row for row in self.plan()['modules'] if row['key'] == key)

    def diagnostic(self, keys=None, *, user=None, indicator='math', status='completed', cycle=1, response_cycle=None, correctness=0):
        keys = keys or ['math-easy-2', 'math-easy-8', 'math-easy-13']
        attempt = AssessmentAttempt.objects.create(student=user or self.user, assessment_type=indicator,
            status=status, attempt_cycle=cycle, completed_at=timezone.now() if status == 'completed' else None)
        for key in keys:
            CognitiveResponse.objects.create(attempt=attempt, question=CognitiveQuestion.objects.get(key=key),
                cycle=response_cycle or cycle, selected_indices=[0], correctness=correctness)
        return attempt

    def check(self, key='arithmetic-algebra', purpose='precheck', wrong=()):
        module = DevelopmentModule.objects.get(key=key)
        enrollment, _ = DevelopmentEnrollment.objects.get_or_create(student=self.user, module=module)
        pool = {q.key: q for q in module.exercises.filter(purpose=purpose).select_related('skill')}
        questions = [pool[q] for q in module.blueprint[purpose+'_order']]
        wrong = set(wrong)
        score = 100 * (5-len(wrong)) / 5
        session = DevelopmentSession.objects.create(enrollment=enrollment, purpose=purpose, status='completed',
            score=score, completed_at=timezone.now(), question_snapshot=[snapshot_question(q) for q in questions])
        for q in questions:
            DevelopmentAnswer.objects.create(session=session, exercise=q, response=q.answer_key,
                idempotency_key=uuid4(), correctness=int(q.skill.key not in wrong))
        enrollment.stage = ('completed' if score >= 80 else 'practice') if purpose == 'postcheck' else ('postcheck' if score >= 80 else 'study')
        enrollment.save()
        return enrollment, session

    def test_no_data_offers_two_checks_without_zero_ability_scores(self):
        data = self.plan()
        self.assertEqual(len(data['recommended']), 2)
        self.assertEqual(data['recommended'][0]['key'], 'arithmetic-algebra')
        self.assertTrue(all(row['recommendation']['action'] == 'verify' for row in data['recommended']))
        for module in data['modules']:
            for skill in module['skills']:
                self.assertIsNone(skill['error_fraction'])
                self.assertEqual(skill['count'], 0)
        self.assertEqual(DevelopmentEnrollment.objects.count(), 0)

    def test_three_distinct_current_completed_answers_establish_diagnostic_gap(self):
        self.diagnostic()
        data = self.plan()
        self.assertEqual(data['recommended'][0]['key'], 'arithmetic-algebra')
        self.assertEqual(data['recommended'][0]['recommendation']['code'], 'diagnostic_review')
        skill = next(row for row in data['recommended'][0]['skills'] if row['key'] == 'arith-order')
        self.assertEqual((skill['status'], skill['count'], skill['error_fraction']), ('review', 3, 1))

    def test_two_answers_are_insufficient_even_when_both_wrong(self):
        self.diagnostic(keys=['math-easy-2','math-easy-8'])
        entry = self.entry()
        self.assertEqual(entry['recommendation']['code'], 'verify')
        skill = next(row for row in entry['skills'] if row['key'] == 'arith-order')
        self.assertEqual(skill['status'], 'insufficient')
        self.assertEqual(skill['count'], 2)
        self.assertIsNone(skill['error_fraction'])

    def test_old_cycles_are_excluded(self):
        self.diagnostic(cycle=2, response_cycle=1)
        skill = next(row for row in self.entry()['skills'] if row['key'] == 'arith-order')
        self.assertEqual(skill['count'], 0)

    def test_in_progress_diagnostic_is_not_evidence(self):
        self.diagnostic(status='in_progress')
        IndicatorScore.objects.create(student=self.user, indicator_key='math', score=1)
        self.assertEqual(self.entry()['recommendation']['code'], 'verify')

    def test_mismatched_indicator_question_is_not_evidence(self):
        self.diagnostic(indicator='logic')
        self.assertEqual(next(row for row in self.entry()['skills'] if row['key']=='arith-order')['count'], 0)

    def test_other_students_answers_are_not_used(self):
        self.diagnostic(user=self.other)
        self.assertTrue(all(skill['count'] == 0 for row in self.plan()['modules'] for skill in row['skills']))

    def test_iq_only_prioritizes_matching_sequence_skills(self):
        self.diagnostic(keys=['iq-extra-series-1','iq-extra-series-2','iq-extra-series-3'], indicator='iq')
        IndicatorScore.objects.create(student=self.user, indicator_key='iq', score=0)
        data = self.plan()
        first = data['recommended'][0]
        self.assertEqual(first['key'], 'functions-sequences-combinatorics')
        self.assertEqual(first['recommendation']['focus_skill_keys'], ['sequences-arithmetic'])
        self.assertTrue(all(skill['source'] == 'none' for row in data['modules'] if row['key']=='matrices-linear-algebra' for skill in row['skills']))

    def test_unrelated_low_score_does_not_create_gaps(self):
        AssessmentAttempt.objects.create(student=self.user, assessment_type='iq', status='completed')
        IndicatorScore.objects.create(student=self.user, indicator_key='iq', score=0)
        self.assertFalse(any(skill['status']=='review' for row in self.plan()['modules'] for skill in row['skills']))

    def test_module_check_is_provisional_and_focuses_only_its_wrong_skill(self):
        enrollment, _ = self.check(wrong=['arith-substitution','arith-identities'])
        row = self.entry()
        wrong = {skill['key'] for skill in row['skills'] if skill['status']=='review'}
        self.assertEqual(wrong, {'arith-substitution','arith-identities'})
        self.assertTrue(all(skill['provisional'] for skill in row['skills']))
        focus = learning_focus(enrollment)
        self.assertEqual(set(focus['required_lesson_keys']), {'arith-lesson-substitution','arith-lesson-identities'})

    def test_focused_lessons_unlock_practice_without_forcing_successful_topics(self):
        enrollment, _ = self.check(wrong=['arith-substitution','arith-identities'])
        root=f'/api/development/enrollments/{enrollment.pk}/lessons/'
        for key in ('arith-lesson-substitution','arith-lesson-identities'):
            result=self.client.post(root+key+'/complete/',{},format='json')
            self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(result.data['stage'],'practice')
        self.assertEqual(len(result.data['completed_lesson_keys']),2)

    def test_weak_local_prerequisite_comes_before_dependent_lesson(self):
        enrollment, _ = self.check(wrong=['arith-order','arith-equations'])
        focus=learning_focus(enrollment)['focus_lesson_keys']
        self.assertLess(focus.index('arith-lesson-order'),focus.index('arith-lesson-equations'))
        self.assertNotIn('arith-lesson-fractions',focus)  # The prerequisite check was answered correctly.

    def test_newer_postcheck_supersedes_old_diagnostic_errors(self):
        self.diagnostic()
        self.check(purpose='precheck',wrong=['arith-order'])
        self.check(purpose='postcheck')
        row=self.entry()
        self.assertEqual(row['recommendation']['code'],'mastered')
        self.assertEqual(next(skill for skill in row['skills'] if skill['key']=='arith-order')['source'],'postcheck')
        self.assertNotIn('arithmetic-algebra',[row['key'] for row in self.plan()['recommended']])

    def test_weaker_foundation_precedes_more_severe_dependent_module(self):
        _, foundation = self.check(wrong=['arith-fractions'])
        # The child has a larger error fraction, so prerequisites must override rank.
        foundation.answers.filter(exercise__skill__key='arith-fractions').update(correctness=.5)
        self.check(key='functions-sequences-combinatorics', wrong=['functions-domain','counting-factorial'])
        keys = [row['key'] for row in self.plan()['recommended']]
        self.assertEqual(keys, ['arithmetic-algebra','functions-sequences-combinatorics'])

    def test_completed_module_with_one_remaining_error_is_optional(self):
        self.check(purpose='postcheck', wrong=['arith-order'])
        row = self.entry()
        self.assertEqual(row['recommendation']['code'], 'mastered')
        self.assertTrue(any(skill['status']=='review' for skill in row['skills']))
        self.assertNotIn('arithmetic-algebra', [item['key'] for item in self.plan()['recommended']])

    def test_invalid_numeric_answer_uses_russian_interface_language(self):
        enrollment=self.client.post('/api/development/modules/arithmetic-algebra/enroll/',{},format='json').data
        session=self.client.post(f'/api/development/enrollments/{enrollment["id"]}/sessions/',
            {'purpose':'precheck'},format='json').data
        while session['question']['format'] != 'numeric':
            exercise=DevelopmentModule.objects.get(key='arithmetic-algebra').exercises.get(key=session['question']['key'])
            session=self.client.post(f'/api/development/sessions/{session["id"]}/answers/',
                {'exercise_key':exercise.key,'response':exercise.answer_key,'idempotency_key':str(uuid4())},
                format='json').data['session']
        result=self.client.post(f'/api/development/sessions/{session["id"]}/answers/',
            {'exercise_key': session['question']['key'], 'response': {'value':'1+2'},
             'idempotency_key':str(uuid4())},format='json',HTTP_X_LANGUAGE='ru')
        self.assertEqual(result.status_code,400)
        self.assertIn('Введите',str(result.data['detail']))

    def test_new_diagnostic_after_postcheck_can_suggest_optional_review(self):
        self.check(purpose='postcheck')
        attempt=self.diagnostic()
        CognitiveResponse.objects.filter(attempt=attempt).update(responded_at=timezone.now()+timedelta(seconds=1))
        row=self.entry()
        self.assertEqual(row['recommendation']['code'],'diagnostic_review')
        self.assertEqual(row['stage'],'completed')

    def test_practice_is_not_diagnostic_or_check_evidence(self):
        module=DevelopmentModule.objects.get(key='arithmetic-algebra')
        enrollment=DevelopmentEnrollment.objects.create(student=self.user,module=module)
        session=DevelopmentSession.objects.create(enrollment=enrollment,purpose='practice',status='completed',score=100)
        q=module.exercises.filter(purpose='practice').first()
        DevelopmentAnswer.objects.create(session=session,exercise=q,response=q.answer_key,idempotency_key=uuid4(),correctness=1)
        self.assertTrue(all(row['count']==0 for row in self.entry()['skills']))

    def test_live_check_redacts_plan_and_blocks_other_module_help(self):
        first=self.client.post('/api/development/modules/arithmetic-algebra/enroll/',{},format='json').data
        self.client.post(f'/api/development/enrollments/{first["id"]}/sessions/',{'purpose':'precheck'},format='json')
        data=self.plan()
        self.assertEqual(len(data['recommended']),1)
        self.assertEqual(data['recommended'][0]['recommendation']['code'],'continue_check')
        self.assertTrue(all(row['skills']==[] for row in data['modules']))
        other=self.client.post('/api/development/modules/mathematical-logic/enroll/',{},format='json').data
        self.assertEqual(other['lessons'],[])
        self.assertEqual(other['skill_progress'],[])
        blocked=self.client.post(f'/api/development/enrollments/{other["id"]}/sessions/',{'purpose':'precheck'},format='json')
        self.assertEqual(blocked.status_code,409)
        self.assertEqual(blocked.data['code'],'active_session')

    def test_plan_is_localized_and_read_only(self):
        self.diagnostic()
        before=list(CognitiveResponse.objects.values())
        with CaptureQueriesContext(connection) as queries:
            data=self.plan('ru')
        self.assertLessEqual(len(queries),40)
        self.assertIn('тесте',data['recommended'][0]['recommendation']['reason'])
        self.assertEqual(list(CognitiveResponse.objects.values()),before)
        self.assertEqual(DevelopmentEnrollment.objects.count(),0)
        self.assertNotIn('answer_key',json.dumps(data))
        self.assertNotIn('selected_indices',json.dumps(data))

    def test_new_enrollment_captures_server_reason_and_keeps_it_immutable(self):
        self.diagnostic()
        result=self.client.post('/api/development/modules/arithmetic-algebra/enroll/',{
            'recommendation_reason': {'code':'forged'}},format='json')
        self.assertEqual(result.status_code,200)
        row=DevelopmentEnrollment.objects.get(pk=result.data['id'])
        before=deepcopy(row.recommendation_reason)
        self.assertEqual(before['code'],'diagnostic_review')
        self.plan()
        row.refresh_from_db()
        self.assertEqual(row.recommendation_reason,before)

    @override_settings(DEVELOPMENT_CLUSTER1_ENABLED=False)
    def test_flag_blocks_plan(self):
        self.assertEqual(self.client.get('/api/development/plan/').status_code,403)
