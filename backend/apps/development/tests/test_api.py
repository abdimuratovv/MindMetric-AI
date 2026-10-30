import json
from copy import deepcopy
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import StudentProfile
from apps.development.content_loader import import_content, publish_module
from apps.development.models import DevelopmentAnswer, DevelopmentEnrollment, DevelopmentModule, DevelopmentSession
from apps.scoring.models import IndicatorScore
from .test_content import ContentDatabaseCase


User = get_user_model()
PREFIX = '/api/development/'


@override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
class DevelopmentAPITests(ContentDatabaseCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        module, _ = import_content(deepcopy(cls.data))
        cls.module = publish_module(module.pk)
        cls.student = User.objects.create_user('learner@university.edu')
        cls.other = User.objects.create_user('another@university.edu')
        for user in (cls.student, cls.other):
            StudentProfile.objects.create(user=user, completed_at=timezone.now())
        IndicatorScore.objects.create(student=cls.student, indicator_key='math', score=42)

    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.client.force_authenticate(self.student)

    def post(self, path, data=None, status=200):
        response = self.client.post(PREFIX + path, data or {}, format='json')
        self.assertEqual(response.status_code, status, response.data)
        return response.data

    def enroll(self):
        return self.post('modules/arithmetic-algebra/enroll/')

    def start(self, enrollment, purpose):
        return self.post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': purpose})

    def solve(self, session, *, wrong=(), hints=()):
        sid = session['id']
        while session['question']:
            question = session['question']
            stored = DevelopmentSession.objects.get(pk=sid)
            private = next(q for q in stored.question_snapshot if q['key'] == question['key'])
            index = session['answered']
            if index in hints:
                self.post(f'sessions/{sid}/hints/', {'exercise_key': question['key']})
            if private['format'] == 'numeric':
                answer = {'value': '999' if index in wrong else private['answer_key']['value']}
            else:
                option_id = private['answer_key']['option_id']
                if index in wrong:
                    option_id = next(o['id'] for o in private['options'] if o['id'] != option_id)
                answer = {'option_id': option_id}
            result = self.post(f'sessions/{sid}/answers/', {
                'exercise_key': question['key'], 'response': answer, 'idempotency_key': str(uuid4()),
            })
            if session['purpose'] != 'practice':
                self.assertNotIn('feedback', result)
                self.assertIsNone(result['session']['score'])
            session = result['session']
        return self.post(f'sessions/{sid}/finish/')

    def study(self, enrollment):
        for lesson in enrollment['lessons']:
            enrollment = self.post(f'enrollments/{enrollment["id"]}/lessons/{lesson["key"]}/complete/')
        return enrollment

    def ready_via_practice(self):
        enrollment = self.solve(self.start(self.enroll(), 'precheck'), wrong=range(5))['enrollment']
        enrollment = self.study(enrollment)
        return self.solve(self.start(enrollment, 'practice'))['enrollment']

    def test_full_low_baseline_learning_flow_and_diagnostic_isolation(self):
        enrollment = self.enroll()
        self.assertEqual(enrollment['lessons'], [])
        self.assertIsNone(enrollment['precheck_score'])
        pre = self.solve(self.start(enrollment, 'precheck'), wrong=range(5))
        enrollment = pre['enrollment']
        self.assertEqual(enrollment['stage'], 'study')
        self.assertEqual(enrollment['precheck_score'], 0)
        self.assertEqual(len(enrollment['lessons']), 5)
        enrollment = self.study(enrollment)
        practice = self.solve(self.start(enrollment, 'practice'), wrong=(0, 1), hints=(0,))
        self.assertEqual(practice['enrollment']['stage'], 'postcheck')
        self.assertEqual(practice['session']['score'], 80)
        final = self.solve(self.start(practice['enrollment'], 'postcheck'), wrong=(0,))
        self.assertEqual(final['enrollment']['stage'], 'completed')
        self.assertEqual(final['enrollment']['delta_percentage_points'], 80)
        self.assertEqual(len(final['session']['review']), 5)
        row = DevelopmentEnrollment.objects.get(pk=enrollment['id'])
        self.assertEqual(row.diagnostic_snapshot['scores'][0]['score'], 42)
        self.assertEqual(IndicatorScore.objects.get(student=self.student).score, 42)

    def test_high_precheck_can_skip_lessons_and_practice(self):
        enrollment = self.solve(self.start(self.enroll(), 'precheck'), wrong=(0,))['enrollment']
        self.assertEqual(enrollment['stage'], 'postcheck')
        self.assertTrue(enrollment['can_postcheck'])
        final = self.solve(self.start(enrollment, 'postcheck'))
        self.assertEqual(final['enrollment']['stage'], 'completed')
        self.assertFalse(DevelopmentSession.objects.filter(purpose='practice').exists())

    def test_hints_in_latest_five_prevent_unlock_and_rehearsal_is_allowed(self):
        enrollment = self.solve(self.start(self.enroll(), 'precheck'), wrong=range(5))['enrollment']
        enrollment = self.study(enrollment)
        result = self.solve(self.start(enrollment, 'practice'), hints=range(5, 10))
        self.assertEqual(result['session']['score'], 100)
        self.assertFalse(result['enrollment']['can_postcheck'])
        self.post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': 'postcheck'}, status=409)
        next_round = self.start(result['enrollment'], 'practice')
        self.assertEqual(next_round['number'], 2)
        result = self.solve(next_round)
        self.assertTrue(result['enrollment']['can_postcheck'])

    def test_failed_postcheck_cannot_be_reused_as_new_growth(self):
        enrollment = self.solve(self.start(self.enroll(), 'precheck'))['enrollment']
        result = self.solve(self.start(enrollment, 'postcheck'), wrong=range(5))
        self.assertEqual(result['enrollment']['stage'], 'practice')
        self.assertTrue(result['enrollment']['check_bank_exhausted'])
        self.assertEqual(result['enrollment']['delta_percentage_points'], -100)
        denied = self.post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': 'postcheck'}, status=409)
        self.assertEqual(denied['code'], 'bank_exhausted')
        self.assertEqual(self.start(result['enrollment'], 'practice')['purpose'], 'practice')

    def test_session_resumes_and_enroll_is_idempotent(self):
        enrollment = self.enroll()
        self.assertEqual(self.enroll()['id'], enrollment['id'])
        session = self.start(enrollment, 'precheck')
        self.assertEqual(self.start(enrollment, 'precheck')['id'], session['id'])
        detail = self.client.get(PREFIX + f'enrollments/{enrollment["id"]}/').data
        self.assertEqual(detail['active_session']['question'], session['question'])
        self.assertEqual(DevelopmentSession.objects.count(), 1)

    def test_answer_replay_is_idempotent_but_changed_payload_conflicts(self):
        session = self.start(self.enroll(), 'precheck')
        payload = {'exercise_key': session['question']['key'], 'response': {'option_id': 'a'}, 'idempotency_key': str(uuid4())}
        self.post(f'sessions/{session["id"]}/answers/', payload)
        self.post(f'sessions/{session["id"]}/answers/', payload)
        self.assertEqual(DevelopmentAnswer.objects.count(), 1)
        payload['response'] = {'option_id': 'b'}
        self.post(f'sessions/{session["id"]}/answers/', payload, status=409)
        self.assertEqual(DevelopmentAnswer.objects.count(), 1)

    def test_check_state_has_no_answer_keys_correctness_or_feedback(self):
        enrollment = self.enroll()
        session = self.start(enrollment, 'precheck')
        result = self.post(f'sessions/{session["id"]}/answers/', {
            'exercise_key': session['question']['key'], 'response': {'option_id': 'a'}, 'idempotency_key': str(uuid4()),
        })
        detail = self.client.get(PREFIX + f'enrollments/{enrollment["id"]}/').data
        for payload in (session, result, detail, self.client.get(PREFIX + 'progress/').data):
            raw = json.dumps(payload)
            for private in ('answer_key', 'correctness', 'solution_steps', 'feedback', 'review', 'worked_example'):
                self.assertNotIn('"' + private + '"', raw)
        self.assertEqual(detail['lessons'], [])

    def test_old_review_and_lessons_are_hidden_during_live_postcheck(self):
        enrollment = self.ready_via_practice()
        self.start(enrollment, 'postcheck')
        detail = self.client.get(PREFIX + f'enrollments/{enrollment["id"]}/').data
        self.assertEqual(detail['lessons'], [])
        for old in DevelopmentSession.objects.exclude(purpose='postcheck'):
            self.assertNotIn('review', self.client.get(PREFIX + f'sessions/{old.pk}/next/').data)
            self.post(f'sessions/{old.pk}/hints/', {'exercise_key': 'arith-practice-01'}, status=409)
        self.post(f'enrollments/{enrollment["id"]}/lessons/arith-lesson-order/complete/', status=409)

    def test_out_of_order_answers_and_early_finish_are_rejected(self):
        session = self.start(self.enroll(), 'precheck')
        self.post(f'sessions/{session["id"]}/answers/', {'exercise_key': 'arith-precheck-03',
            'response': {'value': '10'}, 'idempotency_key': str(uuid4())}, status=409)
        self.post(f'sessions/{session["id"]}/finish/', status=409)
        self.assertEqual(DevelopmentAnswer.objects.count(), 0)

    def test_invalid_payload_and_forged_score_are_rejected(self):
        session = self.start(self.enroll(), 'precheck')
        payload = {'exercise_key': session['question']['key'], 'response': {'option_id': 'a'}, 'idempotency_key': str(uuid4())}
        for change in ({'score': 100}, {'response': {'option_id': []}}, {'idempotency_key': 'invalid'}):
            self.post(f'sessions/{session["id"]}/answers/', {**payload, **change}, status=400)
        self.assertEqual(DevelopmentAnswer.objects.count(), 0)

    def test_numeric_answers_accept_equivalent_fraction_without_expressions(self):
        enrollment = self.solve(self.start(self.enroll(), 'precheck'), wrong=range(5))['enrollment']
        enrollment = self.study(enrollment)
        session = self.start(enrollment, 'practice')
        response = self.post(f'sessions/{session["id"]}/answers/', {'exercise_key': session['question']['key'],
            'response': {'value': '20'}, 'idempotency_key': str(uuid4())})
        question = response['session']['question']
        self.assertEqual(question['key'], 'arith-practice-04')
        self.post(f'sessions/{session["id"]}/answers/', {'exercise_key': question['key'],
            'response': {'value': '1+3/4'}, 'idempotency_key': str(uuid4())}, status=400)
        response = self.post(f'sessions/{session["id"]}/answers/', {'exercise_key': question['key'],
            'response': {'value': '1,75'}, 'idempotency_key': str(uuid4())})
        self.assertTrue(response['feedback']['correct'])

    def test_cannot_skip_precheck_or_required_lessons(self):
        enrollment = self.enroll()
        for purpose in ('practice', 'postcheck'):
            self.post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': purpose}, status=409)
        self.post(f'enrollments/{enrollment["id"]}/lessons/arith-lesson-order/complete/', status=409)
        enrollment = self.solve(self.start(enrollment, 'precheck'), wrong=range(5))['enrollment']
        self.post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': 'practice'}, status=409)

    def test_owner_filters_cover_every_personal_endpoint(self):
        enrollment = self.enroll()
        session = self.start(enrollment, 'precheck')
        self.client.force_authenticate(self.other)
        for path in (f'enrollments/{enrollment["id"]}/', f'sessions/{session["id"]}/next/'):
            self.assertEqual(self.client.get(PREFIX + path).status_code, 404)
        for path in (f'enrollments/{enrollment["id"]}/sessions/',
                     f'enrollments/{enrollment["id"]}/lessons/arith-lesson-order/complete/',
                     f'sessions/{session["id"]}/answers/', f'sessions/{session["id"]}/hints/',
                     f'sessions/{session["id"]}/finish/'):
            self.post(path, status=404)
        self.assertEqual(self.client.get(PREFIX + 'progress/').data['enrollments'], [])

    @override_settings(DEVELOPMENT_CLUSTER1_ENABLED=False)
    def test_capabilities_false_and_all_learning_access_blocked_when_flag_off(self):
        caps = self.client.get(PREFIX + 'capabilities/')
        self.assertEqual(caps.data, {'enabled': False, 'available': False})
        self.assertEqual(self.client.get(PREFIX + 'modules/').status_code, 403)
        self.post('modules/arithmetic-algebra/enroll/', status=403)

    def test_anonymous_teacher_and_incomplete_profile_are_denied(self):
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get(PREFIX + 'modules/').status_code, 401)
        for role in ('student', 'teacher', 'admin'):
            self.client.force_authenticate(User.objects.create_user(role+'@university.edu', role=role))
            self.assertEqual(self.client.get(PREFIX + 'capabilities/').status_code, 403)

    def test_real_jwt_can_access_capabilities_and_uz_fallback_is_explicit(self):
        self.client.force_authenticate(None)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(self.student)}')
        self.assertTrue(self.client.get(PREFIX + 'capabilities/').data['available'])
        cards = self.client.get(PREFIX + 'modules/', HTTP_X_LANGUAGE='ru').data['modules']
        self.assertEqual(cards[0]['content_language'], 'uz')
        self.assertEqual(cards[0]['title'], self.module.title_uz)

    def test_new_student_gets_latest_published_version(self):
        revised = deepcopy(self.data)
        revised['module']['version'] = 2
        module, _ = import_content(revised)
        publish_module(module.pk)
        self.assertEqual(self.enroll()['module']['version'], 2)

    def test_enrolled_student_resumes_original_version(self):
        enrollment = self.enroll()
        revised = deepcopy(self.data)
        revised['module']['version'] = 2
        module, _ = import_content(revised)
        publish_module(module.pk)
        self.assertEqual(self.enroll()['id'], enrollment['id'])
        self.assertEqual(self.client.get(PREFIX + 'modules/').data['modules'][0]['version'], 1)

    def test_draft_module_cannot_be_enrolled(self):
        revised = deepcopy(self.data)
        revised['module']['key'] = 'unpublished'
        import_content(revised)
        self.post('modules/unpublished/enroll/', status=404)
