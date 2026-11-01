"""Three-cluster release, bilingual flow, files and cross-cluster answer privacy."""
import os
from copy import deepcopy
from io import StringIO
from unittest.mock import patch
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from apps.accounts.models import StudentProfile
from apps.development.content_loader import bundled_contents, import_bundle, publish_module
from apps.development.models import DevelopmentModule, DevelopmentSession
from apps.development.progress import enroll, start_session
from apps.development.translations import bundled_translation, validate_translation
from apps.development.validation import ContentValidationError, content_hash, validate_content
from apps.scoring.models import IndicatorScore, OverallScore, StudentAbilityEstimate
from .test_content import ContentDatabaseCase
from . import test_cluster2 as legacy


class ClusterThreeResources(SimpleTestCase):
    def test_real_schema3_all_resources_and_complete_locales(self):
        contents = bundled_contents(None)
        graph = {s['key']: s['prerequisite_keys'] for d in contents for s in d['skills']}
        self.assertEqual(len(contents), 16)
        self.assertEqual(len(bundled_contents(3)), 4)
        for data in contents:
            validate_content(data, known_skills=graph)
            validate_translation(data, bundled_translation(data['module']['key'], 1))
        self.assertEqual(sum(len(d['projects']) for d in bundled_contents(3)), 3)
        self.assertEqual(sum(len(d['study_files']) for d in bundled_contents(3)), 2)

    def test_schema3_rejects_wrong_cluster_teacher_fields_and_file_paths(self):
        source = bundled_contents(3)[0]
        for mutation in (
            lambda d: d['module'].update(cluster=2),
            lambda d: d['module'].update(order=5, topic_number='3.5'),
            lambda d: d['module'].update(indicator_keys=['math']),
            lambda d: d['projects'][0].update(solution_uz=['teacher answer']),
            lambda d: d['study_files'][0].update(filename='../teacher.py'),
            lambda d: d['study_files'][0].update(answer_key='private'),
        ):
            data = deepcopy(source); mutation(data)
            with self.subTest(mutation=mutation), self.assertRaises(ContentValidationError):
                validate_content(data)
        ru = deepcopy(bundled_translation(source['module']['key'], 1))
        ru['study_files'][source['study_files'][0]['key']]['content'] = 'replacement'
        with self.assertRaises(ContentValidationError):
            validate_translation(source, ru)
        ru = deepcopy(bundled_translation(source['module']['key'], 1))
        q = source['exercises'][0]
        ru['exercises'][q['key']]['prompt'] = ru['exercises'][q['key']]['prompt'].replace('/ 0', '/ 1')
        with self.assertRaises(ContentValidationError):
            validate_translation(source, ru)


class ClusterThreeRelease(ContentDatabaseCase):
    def setUp(self):
        legacy.seed_diagnostic_references()

    @patch.dict(os.environ, {'RENDER': ''})
    def test_combined_release_is_idempotent_and_preserves_pinned_cluster2(self):
        call_command('activate_development_cluster2', stdout=StringIO())
        user = get_user_model().objects.create_user('pinned3@university.edu')
        row = enroll(user, 'conditions-comparisons')
        session = start_session(user, row.pk, 'precheck')
        pinned = deepcopy(session.question_snapshot)
        old = list(DevelopmentModule.objects.values_list('pk', 'content_hash', 'content_snapshot'))
        for _ in range(2):
            call_command('activate_development_cluster3', stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(), 16)
        self.assertEqual(old, list(DevelopmentModule.objects.filter(cluster__in=[1, 2]).values_list('pk', 'content_hash', 'content_snapshot')))
        session.refresh_from_db(); self.assertEqual(pinned, session.question_snapshot)
        self.assertFalse(IndicatorScore.objects.exists())

    @patch.dict(os.environ, {'RENDER': ''})
    def test_late_failure_rolls_back_whole_release(self):
        def fail_last(pk):
            module = DevelopmentModule.objects.get(pk=pk)
            if module.cluster == 3 and module.order == 4:
                raise RuntimeError('last module failure')
            return publish_module(pk)
        with patch('apps.development.management.commands.activate_development_cluster3.publish_module', side_effect=fail_last):
            with self.assertRaisesMessage(RuntimeError, 'last module failure'):
                call_command('activate_development_cluster3', stdout=StringIO())
        self.assertFalse(DevelopmentModule.objects.exists())

    @patch.dict(os.environ, {'RENDER': ''})
    def test_missing_topic_and_missing_locale_fail_before_writes(self):
        with patch('apps.development.management.commands.activate_development_cluster3.bundled_contents', return_value=bundled_contents(None)[:-1]):
            with self.assertRaises(CommandError):
                call_command('activate_development_cluster3', stdout=StringIO())
        with patch('apps.development.translations.bundled_translation', return_value=None):
            with self.assertRaises(CommandError):
                call_command('activate_development_cluster3', stdout=StringIO())
        self.assertFalse(DevelopmentModule.objects.exists())

    @patch.dict(os.environ, {'RENDER': 'true'})
    @patch('apps.development.management.commands.activate_development_cluster3.connection.vendor', 'sqlite')
    def test_render_requires_persistent_postgres(self):
        with self.assertRaises(CommandError):
            call_command('activate_development_cluster3', stdout=StringIO())


@override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
class ClusterThreeAPI(ContentDatabaseCase):
    get = legacy.ClusterTwoAPITests.get
    post = legacy.ClusterTwoAPITests.post
    response_for = staticmethod(legacy.ClusterTwoAPITests.response_for)
    direct_check = legacy.ClusterTwoAPITests.direct_check

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        legacy.seed_diagnostic_references()
        for _, module, _ in import_bundle(bundled_contents(None)):
            publish_module(module.pk)
        cls.user = get_user_model().objects.create_user('cluster3@university.edu')
        cls.other = get_user_model().objects.create_user('cluster3-other@university.edu')
        for user in (cls.user, cls.other):
            StudentProfile.objects.create(user=user, completed_at=timezone.now())

    def setUp(self):
        cache.clear()
        self.client = APIClient(); self.client.force_authenticate(self.user)

    def test_three_cluster_catalogue_and_all_four_bilingual_learning_flows(self):
        IndicatorScore.objects.create(student=self.user, indicator_key='attention', score=35)
        before = list(IndicatorScore.objects.values())
        for language in ('uz', 'ru'):
            plan = self.get('plan/', language)
            self.assertEqual([(r['id'], r['module_count']) for r in plan['clusters']], [(1, 6), (2, 6), (3, 4)])
            self.assertEqual(len(plan['modules']), 16)
            self.assertTrue(all(m['content_language'] == language for m in plan['modules']))
        for data in bundled_contents(3):
            cache.clear()
            key = data['module']['key']; ru = bundled_translation(key, 1)
            state = self.post(f'modules/{key}/enroll/', language='ru')
            self.assertEqual(state['projects'], [])
            self.assertEqual(state['study_files'], [])
            for purpose in ('precheck', 'practice', 'postcheck'):
                if purpose == 'practice':
                    for lesson in state['lessons']:
                        state = self.post(f'enrollments/{state["id"]}/lessons/{lesson["key"]}/complete/')
                session = self.post(f'enrollments/{state["id"]}/sessions/', {'purpose': purpose}, language='ru')
                snapshot = deepcopy(DevelopmentSession.objects.get(pk=session['id']).question_snapshot)
                while session['question']:
                    q = next(q for q in snapshot if q['key'] == session['question']['key'])
                    for language in ('uz', 'ru'):
                        current = self.get(f'sessions/{session["id"]}/next/', language)
                        self.assertEqual(current['question']['prompt'], ru['exercises'][q['key']]['prompt'] if language == 'ru' else q['prompt_uz'])
                        if purpose != 'practice':
                            self.assertNotIn('answer_key', str(current))
                            self.assertNotIn('solution_steps', str(current))
                    payload = {'exercise_key': q['key'], 'response': self.response_for(q, purpose != 'precheck'), 'idempotency_key': str(uuid4())}
                    response = self.post(f'sessions/{session["id"]}/answers/', payload, language='ru')
                    replay = self.post(f'sessions/{session["id"]}/answers/', payload, language='uz')
                    self.assertEqual(replay['session']['answered'], response['session']['answered'])
                    if purpose != 'practice':
                        self.assertNotIn('feedback', response)
                    session = response['session']
                state = self.post(f'sessions/{session["id"]}/finish/', language='ru')['enrollment']
                if purpose == 'precheck':
                    for language in ('uz', 'ru'):
                        current = self.get(f'enrollments/{state["id"]}/', language)
                        self.assertEqual(len(current['lessons']), 5)
                        self.assertEqual(len(current['projects']), len(data['projects']))
                        self.assertEqual(len(current['study_files']), len(data['study_files']))
                        self.assertNotIn('solution_uz', str(current['projects']))
                        for lesson in current['lessons']:
                            original = next(l for l in data['lessons'] if l['key'] == lesson['key'])
                            target = ru['lessons'][lesson['key']]
                            self.assertEqual(lesson['theory'], target['theory'] if language == 'ru' else original['theory_uz'])
                        for file, original in zip(current['study_files'], data['study_files']):
                            self.assertEqual(file['content'], original['content'])
                            self.assertEqual(file['title'], ru['study_files'][file['key']]['title'] if language == 'ru' else original['title_uz'])
            self.assertEqual(state['stage'], 'completed')
        self.assertEqual(list(IndicatorScore.objects.values()), before)
        self.assertFalse(OverallScore.objects.exists()); self.assertFalse(StudentAbilityEstimate.objects.exists())

    def test_files_projects_and_completed_answers_lock_across_all_clusters(self):
        target = self.direct_check(self.user, 'documentation-learning', False)
        for key in ('arithmetic-algebra', 'conditions-comparisons', 'code-debugging'):
            cache.clear()
            source = enroll(self.user, key)
            check = start_session(self.user, source.pk, 'precheck')
            state = self.get(f'enrollments/{target.pk}/', 'ru')
            for field in ('lessons', 'projects', 'study_files', 'notation', 'skill_progress'):
                self.assertEqual(state[field], [])
            self.assertTrue(all('review' not in item for item in state['checks']))
            self.post(f'enrollments/{target.pk}/sessions/', {'purpose': 'practice'}, status=409)
            for q in check.question_snapshot:
                self.post(f'sessions/{check.pk}/answers/', {'exercise_key': q['key'], 'response': self.response_for(q), 'idempotency_key': str(uuid4())})
            self.post(f'sessions/{check.pk}/finish/')
        self.client.force_authenticate(self.other)
        self.get(f'enrollments/{target.pk}/', status=404)
