"""Parallel HTTP view requests on independent real PostgreSQL connections."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from threading import Barrier
from unittest import skipUnless
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection, connections
from django.test import TransactionTestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import StudentProfile
from apps.assessments.content import MCQ_QUESTIONS
from apps.assessments.models import CognitiveQuestion
from apps.development.content_loader import bundled_contents, import_bundle, publish_module
from apps.development.models import DevelopmentAnswer, DevelopmentEnrollment, DevelopmentSession
from apps.development.progress import finish_session, start_session, submit_answer
from apps.scoring.models import IndicatorScore


@skipUnless(connection.vendor == 'postgresql', 'Requires real PostgreSQL row locks.')
@override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
class ConcurrentDevelopmentTests(TransactionTestCase):
    def setUp(self):
        cache.clear()
        data=bundled_contents()
        required={link['question_key'] for item in data for link in item['diagnostic_links']}
        for indicator, questions in MCQ_QUESTIONS.items():
            for question in questions:
                if question['key'] in required:
                    CognitiveQuestion.objects.create(indicator_key=indicator, **question)
        for _, module, _ in import_bundle(deepcopy(data)):
            publish_module(module.pk)
        self.user=get_user_model().objects.create_user('parallel@university.edu')
        StudentProfile.objects.create(user=self.user,completed_at=timezone.now())
        IndicatorScore.objects.create(student=self.user,indicator_key='math',score=42)
        self.client=APIClient()
        self.client.force_authenticate(self.user)
        self.enrollment=self.client.post('/api/development/modules/arithmetic-algebra/enroll/',{},format='json').data

    def parallel(self, *requests):
        ready=Barrier(len(requests))
        user_id=self.user.pk
        def send(request):
            connections.close_all()
            try:
                client=APIClient()
                client.force_authenticate(get_user_model().objects.get(pk=user_id))
                ready.wait(timeout=10)
                response=client.post(request[0],request[1],format='json')
                return response.status_code,response.data
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=len(requests)) as pool:
            results=list(pool.map(send,requests))
        self.assertEqual(IndicatorScore.objects.get(student=self.user,indicator_key='math').score,42)
        return results

    def begin(self):
        return start_session(self.user,self.enrollment['id'],'precheck')

    def test_duplicate_enrollment_returns_one_row(self):
        request=('/api/development/modules/mathematical-logic/enroll/',{})
        results=self.parallel(request,request)
        self.assertEqual([r[0] for r in results],[200,200])
        self.assertEqual(results[0][1]['id'],results[1][1]['id'])
        self.assertEqual(DevelopmentEnrollment.objects.filter(student=self.user).count(),2)

    def test_duplicate_start_resumes_one_session(self):
        request=(f'/api/development/enrollments/{self.enrollment["id"]}/sessions/',{'purpose':'precheck'})
        results=self.parallel(request,request)
        self.assertEqual([r[0] for r in results],[200,200])
        self.assertEqual(results[0][1]['id'],results[1][1]['id'])
        self.assertEqual(DevelopmentSession.objects.count(),1)

    def test_simultaneous_modules_allow_only_one_active_session(self):
        other=self.client.post('/api/development/modules/mathematical-logic/enroll/',{},format='json').data
        results=self.parallel(*[(f'/api/development/enrollments/{eid}/sessions/',{'purpose':'precheck'})
                                for eid in (self.enrollment['id'],other['id'])])
        self.assertEqual(sorted(r[0] for r in results),[200,409])
        self.assertEqual(next(r[1]['code'] for r in results if r[0]==409),'active_session')
        self.assertEqual(DevelopmentSession.objects.filter(status='in_progress').count(),1)

    def test_identical_parallel_answer_uuid_creates_one_answer(self):
        session=self.begin()
        question=session.question_snapshot[0]
        payload={'exercise_key':question['key'],'response':question['answer_key'],'idempotency_key':str(uuid4())}
        request=(f'/api/development/sessions/{session.pk}/answers/',payload)
        results=self.parallel(request,request)
        self.assertEqual([r[0] for r in results],[200,200])
        self.assertEqual(DevelopmentAnswer.objects.count(),1)
        self.assertEqual([r[1]['session']['answered'] for r in results],[1,1])

    def test_competing_answer_uuids_do_not_advance_twice(self):
        session=self.begin()
        question=session.question_snapshot[0]
        results=self.parallel(*[(f'/api/development/sessions/{session.pk}/answers/',{
            'exercise_key':question['key'],'response':question['answer_key'],'idempotency_key':str(uuid4())})
            for _ in range(2)])
        self.assertEqual(sorted(r[0] for r in results),[200,409])
        self.assertEqual(DevelopmentAnswer.objects.count(),1)

    def test_parallel_finish_is_idempotent(self):
        session=self.begin()
        for question in session.question_snapshot:
            submit_answer(self.user,session.pk,exercise_key=question['key'],
                          response=question['answer_key'],idempotency_key=uuid4())
        request=(f'/api/development/sessions/{session.pk}/finish/',{})
        results=self.parallel(request,request)
        self.assertEqual([r[0] for r in results],[200,200])
        self.assertEqual([r[1]['session']['score'] for r in results],[100,100])
        self.assertEqual(DevelopmentSession.objects.filter(status='completed').count(),1)
        self.assertEqual(DevelopmentAnswer.objects.count(),5)

    def test_parallel_hint_and_answer_preserve_hint_usage(self):
        session=self.begin()
        for question in session.question_snapshot:
            submit_answer(self.user,session.pk,exercise_key=question['key'],
                          response=question['answer_key'],idempotency_key=uuid4())
        finish_session(self.user,session.pk)
        practice=start_session(self.user,self.enrollment['id'],'practice')
        question=practice.question_snapshot[0]
        results=self.parallel(
            (f'/api/development/sessions/{practice.pk}/hints/',{'exercise_key':question['key']}),
            (f'/api/development/sessions/{practice.pk}/answers/',{'exercise_key':question['key'],
                'response':question['answer_key'],'idempotency_key':str(uuid4())}))
        self.assertEqual(results[1][0],200)
        self.assertIn(results[0][0],(200,409))
        answer=DevelopmentAnswer.objects.get(session=practice)
        self.assertEqual(answer.hint_used,results[0][0]==200)
