"""Bilingual cluster integration, release atomicity and cross-cluster privacy."""
import os
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import StudentProfile
from apps.assessments.content import MCQ_QUESTIONS
from apps.assessments.models import CognitiveQuestion
from apps.development.content_loader import bundled_contents, import_bundle, import_content, publish_module, read_content
from apps.development.models import DevelopmentAnswer, DevelopmentEnrollment, DevelopmentExercise, DevelopmentModule, DevelopmentSession
from apps.development.progress import enroll, start_session, submit_answer, finish_session
from apps.development.translations import DIRECTORY, bundled_translation, validate_translation
from apps.development.validation import ContentValidationError, content_hash, validate_content
from apps.scoring.models import IndicatorScore, OverallScore, StudentAbilityEstimate
from .test_content import ContentDatabaseCase


def legacy_contents():
    return bundled_contents(cluster=1) + bundled_contents(cluster=2)


def graph_for(contents):
    return {s['key']: s['prerequisite_keys'] for d in contents for s in d['skills']}


def seed_diagnostic_references():
    needed = {link['question_key'] for d in bundled_contents() for link in d['diagnostic_links']}
    for indicator, rows in MCQ_QUESTIONS.items():
        for row in rows:
            if row['key'] in needed:
                CognitiveQuestion.objects.get_or_create(key=row['key'], defaults={
                    'indicator_key': indicator, **{k: v for k, v in row.items() if k != 'key'},
                })


class ClusterTwoResourceTests(SimpleTestCase):
    def setUp(self):
        self.contents = legacy_contents()
        self.graph = graph_for(self.contents)
        self.data = next(d for d in self.contents if d['module']['key'] == 'creative-mini-apps')

    def test_all_twelve_resources_validate_and_reviewed_copies_match(self):
        root = Path(__file__).resolve().parents[4] / 'docs/content/cluster2'
        self.assertEqual(len(self.contents), 12)
        self.assertEqual(len(bundled_contents()), 6)
        self.assertEqual(len(bundled_contents(cluster=2)), 6)
        for data in self.contents:
            validate_content(data, known_skills=self.graph)
            if data['schema_version'] == 2:
                key = data['module']['key']
                self.assertEqual(content_hash(data), content_hash(read_content(root / f'{key}.v1.json')))
                ru = bundled_translation(key, 1)
                self.assertEqual(ru, read_content(root / 'translations' / f'{key}.v1.ru.json'))
                self.assertEqual(len(ru['lessons']), 5)
                self.assertEqual(len(ru['exercises']), 20)
                self.assertEqual(len(ru['notation']), 8)
        self.assertEqual(len(self.data['projects']), 2)

    def test_new_schema_rejects_invalid_metadata_projects_and_notation(self):
        mutations = [
            lambda d: d['module'].update(cluster=True),
            lambda d: d['module'].update(cluster=1),
            lambda d: d['module'].update(topic_number='1.6'),
            lambda d: d['module'].update(order=7),
            lambda d: d['module'].update(indicator_keys=['math']),
            lambda d: d.update(notation_uz=[]),
            lambda d: d['projects'][0].update(assessment='automatic'),
            lambda d: d['projects'][0].update(answer_key={'value': '1'}),
            lambda d: d['projects'][0].update(rubric_uz=[]),
            lambda d: d['projects'].append(deepcopy(d['projects'][0])),
        ]
        for mutation in mutations:
            data = deepcopy(self.data); mutation(data)
            with self.subTest(mutation=mutation), self.assertRaises(ContentValidationError):
                validate_content(data, known_skills=self.graph)

    def test_legacy_schema_cannot_smuggle_new_cluster_resources(self):
        data = deepcopy(self.data); data['schema_version'] = 1
        with self.assertRaises(ContentValidationError):
            validate_content(data, known_skills=self.graph)
        for old in bundled_contents():
            self.assertEqual(old['schema_version'], 1)
            self.assertNotIn('cluster', old['module'])
            validate_content(old, known_skills=self.graph)

    def test_missing_project_or_notation_translation_and_changed_code_are_rejected(self):
        original = bundled_translation(self.data['module']['key'], 1)
        mutations = [lambda d: d.pop('notation'), lambda d: d.update(projects={}),
                     lambda d: d['projects']['project-study-planner'].pop('rubric'),
                     lambda d: d['projects']['project-study-planner'].update(answer_key='x')]
        for mutation in mutations:
            translated = deepcopy(original); mutation(translated)
            with self.subTest(mutation=mutation), self.assertRaises(ContentValidationError):
                validate_translation(self.data, translated)
        data = next(d for d in self.contents if d['module']['key'] == 'loops-recursion')
        translated = deepcopy(bundled_translation(data['module']['key'], 1))
        translated['exercises']['loop-while-precheck']['prompt'] = translated['exercises']['loop-while-precheck']['prompt'].replace('<', '>')
        with self.assertRaisesMessage(ContentValidationError, 'operators changed'):
            validate_translation(data, translated)

    def test_malformed_translation_is_a_content_error(self):
        for value in (None, [], {}, {'module_key': self.data['module']['key']}):
            with self.subTest(value=value), self.assertRaises(ContentValidationError):
                validate_translation(self.data, value)


class ClusterTwoImportTests(ContentDatabaseCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        seed_diagnostic_references()

    def test_combined_dry_run_and_draft_import_are_atomic_idempotent_and_legacy_default_stays_six(self):
        out = StringIO()
        call_command('seed_development_content', all=True, cluster='all', dry_run=True, stdout=out)
        self.assertEqual(out.getvalue().count('Validated without writes'), 16)
        self.assertFalse(DevelopmentModule.objects.exists())
        call_command('seed_development_content', all=True, stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(), 6)
        call_command('seed_development_content', all=True, cluster='2', stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(), 12)
        ids = list(DevelopmentExercise.objects.order_by('pk').values_list('pk', 'key'))
        call_command('seed_development_content', all=True, cluster='all', stdout=StringIO())
        self.assertEqual(ids, list(DevelopmentExercise.objects.filter(module__cluster__in=[1, 2]).order_by('pk').values_list('pk', 'key')))
        self.assertEqual(DevelopmentModule.objects.count(), 16)
        self.assertEqual(DevelopmentExercise.objects.count(), 320)
        all_ids = list(DevelopmentExercise.objects.order_by('pk').values_list('pk', 'key'))
        call_command('seed_development_content', all=True, cluster='all', stdout=StringIO())
        self.assertEqual(all_ids, list(DevelopmentExercise.objects.order_by('pk').values_list('pk', 'key')))
        self.assertEqual(set(DevelopmentModule.objects.values_list('status', flat=True)), {'draft'})
        self.assertFalse(get_user_model().objects.exists())

    def test_missing_or_wrong_russian_translation_prevents_any_writes(self):
        original = bundled_translation
        for missing in (True, False):
            def bad_translation(key, version):
                value = original(key, version)
                if key == 'creative-mini-apps':
                    if missing:
                        return None
                    value = deepcopy(value); value['source_hash'] = '0' * 64
                return value
            with self.subTest(missing=missing), patch('apps.development.translations.bundled_translation', side_effect=bad_translation):
                with self.assertRaises(ContentValidationError):
                    import_bundle(legacy_contents())
                self.assertFalse(DevelopmentModule.objects.exists())

    def test_missing_prerequisite_and_duplicate_topic_are_rejected_without_fabricated_cluster_one_dependency(self):
        invalid = deepcopy(bundled_contents(cluster=2))
        invalid[0]['skills'][0]['prerequisite_keys'] = ['missing-skill']
        with self.assertRaisesMessage(ContentValidationError, 'Unknown prerequisite'):
            import_bundle(invalid)
        self.assertFalse(DevelopmentModule.objects.exists())
        for field, value in (('order', []), ('cluster', {})):
            malformed = deepcopy(bundled_contents(cluster=2))
            malformed[0]['module'][field] = value
            with self.subTest(field=field), self.assertRaises(ContentValidationError):
                import_bundle(malformed)
        import_bundle(bundled_contents(cluster=2))
        self.assertEqual(DevelopmentModule.objects.count(), 6)
        contents = deepcopy(legacy_contents())
        contents[-1]['module']['order'] = 5
        with self.assertRaisesMessage(ContentValidationError, 'Duplicate topic'):
            import_bundle(contents)
        self.assertEqual(DevelopmentModule.objects.count(), 6)

    @patch.dict(os.environ, {'RENDER': ''})
    def test_combined_release_publishes_twelve_without_users_scores_and_keeps_ids(self):
        call_command('activate_development_cluster2', stdout=StringIO())
        rows = list(DevelopmentModule.objects.values_list('pk', 'key', 'cluster', 'content_hash'))
        exercises = list(DevelopmentExercise.objects.order_by('pk').values_list('pk', flat=True))
        call_command('activate_development_cluster2', stdout=StringIO())
        self.assertEqual(rows, list(DevelopmentModule.objects.values_list('pk', 'key', 'cluster', 'content_hash')))
        self.assertEqual(exercises, list(DevelopmentExercise.objects.order_by('pk').values_list('pk', flat=True)))
        self.assertEqual(DevelopmentModule.objects.filter(status='published', cluster=2).count(), 6)
        self.assertEqual(DevelopmentModule.objects.filter(status='published', cluster=1).count(), 6)
        for model in (get_user_model(), IndicatorScore, OverallScore, StudentAbilityEstimate):
            self.assertFalse(model.objects.exists())

    @patch.dict(os.environ, {'RENDER': ''})
    def test_late_publication_failure_rolls_back_both_clusters(self):
        def fail_last(pk):
            module = DevelopmentModule.objects.get(pk=pk)
            if module.cluster == 2 and module.order == 6:
                raise RuntimeError('late cluster-two publication failure')
            return publish_module(pk)
        with patch('apps.development.management.commands.activate_development_cluster2.publish_module', side_effect=fail_last):
            with self.assertRaisesMessage(RuntimeError, 'late cluster-two'):
                call_command('activate_development_cluster2', stdout=StringIO())
        self.assertFalse(DevelopmentModule.objects.exists())
        self.assertFalse(DevelopmentExercise.objects.exists())

    @patch.dict(os.environ, {'RENDER': ''})
    def test_incomplete_release_bundle_is_rejected_before_writes(self):
        for cluster in (1, 2):
            contents = [d for d in legacy_contents()
                        if not (d['module'].get('cluster', 1) == cluster and d['module']['order'] == 6)]
            with self.subTest(cluster=cluster), patch(
                'apps.development.management.commands.activate_development_cluster2.bundled_contents', return_value=contents
            ), self.assertRaisesMessage(CommandError, 'requires all six reviewed topics'):
                call_command('activate_development_cluster2', stdout=StringIO())
            self.assertFalse(DevelopmentModule.objects.exists())

    @patch.dict(os.environ, {'RENDER': 'true'})
    @patch('apps.development.management.commands.activate_development_cluster2.connection.vendor', 'sqlite')
    def test_render_sqlite_rejected_before_release(self):
        with self.assertRaisesMessage(CommandError, 'persistent PostgreSQL'):
            call_command('activate_development_cluster2', stdout=StringIO())
        self.assertFalse(DevelopmentModule.objects.exists())

    def test_existing_frozen_enrollment_and_question_snapshot_survive_new_import(self):
        for _, module, _ in import_bundle(bundled_contents()):
            publish_module(module.pk)
        baseline = list(DevelopmentModule.objects.values_list('pk', 'content_hash', 'content_snapshot'))
        user = get_user_model().objects.create_user('legacy-pinned@university.edu')
        row = enroll(user, 'arithmetic-algebra')
        session = start_session(user, row.pk, 'precheck')
        original = deepcopy(session.question_snapshot)
        for _, module, _ in import_bundle(bundled_contents(cluster=2)):
            publish_module(module.pk)
        self.assertEqual(baseline, list(DevelopmentModule.objects.filter(cluster=1).values_list('pk', 'content_hash', 'content_snapshot')))
        self.assertEqual(enroll(user, 'arithmetic-algebra').pk, row.pk)
        session.refresh_from_db(); self.assertEqual(original, session.question_snapshot)
        row.module.cluster = 2
        with self.assertRaises(ValidationError):
            row.module.save()

    def test_dry_run_and_import_both_reject_moving_a_module_key_to_another_cluster(self):
        import_content(deepcopy(self.data))
        data = deepcopy(bundled_contents(cluster=2)[0])
        data['module'].update(key='arithmetic-algebra', version=2)
        for dry_run in (True, False):
            with self.subTest(dry_run=dry_run), self.assertRaisesMessage(ContentValidationError, 'cannot move between clusters'):
                import_bundle([data], dry_run=dry_run)
        self.assertEqual(DevelopmentModule.objects.count(), 1)


@override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
class ClusterTwoAPITests(ContentDatabaseCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        seed_diagnostic_references()
        for _, module, _ in import_bundle(legacy_contents()):
            publish_module(module.pk)
        cls.user = get_user_model().objects.create_user('cluster2-learner@university.edu')
        cls.other = get_user_model().objects.create_user('cluster2-other@university.edu')
        for user in (cls.user, cls.other):
            StudentProfile.objects.create(user=user, completed_at=timezone.now())

    def setUp(self):
        cache.clear()
        self.client = APIClient(); self.client.force_authenticate(self.user)

    def get(self, path, language='uz', status=200):
        result = self.client.get('/api/development/' + path, HTTP_X_LANGUAGE=language)
        self.assertEqual(result.status_code, status, result.data)
        return result.data

    def post(self, path, payload=None, language='uz', status=200):
        result = self.client.post('/api/development/' + path, payload or {}, format='json', HTTP_X_LANGUAGE=language)
        self.assertEqual(result.status_code, status, result.data)
        return result.data

    def direct_check(self, user, key, correct=True):
        enrollment = enroll(user, key)
        session = start_session(user, enrollment.pk, 'precheck')
        for q in session.question_snapshot:
            response = self.response_for(q, correct)
            submit_answer(user, session.pk, exercise_key=q['key'], response=response, idempotency_key=uuid4())
        finish_session(user, session.pk)
        return enrollment

    @staticmethod
    def response_for(q, correct=True):
        if q['format'] == 'numeric':
            return {'value': q['answer_key']['value'] if correct else '999999'}
        return {'option_id': q['answer_key']['option_id'] if correct else next(o['id'] for o in q['options'] if o['id'] != q['answer_key']['option_id'])}

    def test_catalogue_clusters_topics_languages_and_optional_diagnostic_reason(self):
        snapshots = list(DevelopmentModule.objects.values_list('pk', 'content_hash', 'content_snapshot'))
        for language in ('ru', 'uz', 'ru'):
            plan = self.get('plan/', language)
            self.assertEqual(len(plan['modules']), 12)
            self.assertEqual([(r['id'], r['module_count']) for r in plan['clusters']], [(1, 6), (2, 6)])
            self.assertEqual([m['topic_number'] for m in plan['modules']], [f'{cluster}.{number}' for cluster in (1, 2) for number in range(1, 7)])
            for card in [m for m in plan['modules'] if m['cluster'] == 2]:
                self.assertEqual(card['content_language'], language)
                self.assertEqual(card['recommendation']['code'], 'no_diagnostic')
                self.assertTrue(all(s['content_language'] == language for s in card['skills']))
        self.assertEqual(snapshots, list(DevelopmentModule.objects.values_list('pk', 'content_hash', 'content_snapshot')))

    def test_all_six_modules_complete_bilingual_learning_flow_with_retry_and_no_diagnostic_writes(self):
        IndicatorScore.objects.create(student=self.user, indicator_key='algorithmic', score=35)
        original_scores = list(IndicatorScore.objects.values())
        for data in bundled_contents(cluster=2):
            with self.subTest(module=data['module']['key']):
                cache.clear()
                key = data['module']['key']
                translated = bundled_translation(key, 1)
                enrollment = self.post(f'modules/{key}/enroll/', language='ru')
                self.assertEqual(len(enrollment['notation']), 8)
                self.assertEqual(enrollment['notation'], translated['notation'])
                self.assertEqual(enrollment['lessons'], [])
                self.assertEqual(enrollment['projects'], [])
                for purpose in ('precheck', 'practice', 'postcheck'):
                    if purpose == 'practice':
                        for lesson in enrollment['lessons']:
                            enrollment = self.post(f'enrollments/{enrollment["id"]}/lessons/{lesson["key"]}/complete/', language='ru')
                    session = self.post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': purpose}, language='ru')
                    snapshot = deepcopy(DevelopmentSession.objects.get(pk=session['id']).question_snapshot)
                    while session['question']:
                        q = next(q for q in snapshot if q['key'] == session['question']['key'])
                        for language in ('uz', 'ru'):
                            state = self.get(f'sessions/{session["id"]}/next/', language)
                            self.assertEqual(state['question']['content_language'], language)
                            self.assertEqual(state['question']['key'], q['key'])
                            tq = translated['exercises'][q['key']]
                            self.assertEqual(state['question']['prompt'], tq['prompt'] if language == 'ru' else q['prompt_uz'])
                            self.assertEqual(state['question']['options'], [
                                {'id': o['id'], 'text': tq['options'][o['id']]['text'] if language == 'ru' else o['text_uz']}
                                for o in q['options']
                            ])
                            if purpose != 'practice':
                                for private in ('answer_key', 'solution_steps', 'hint', 'feedback', 'review'):
                                    self.assertNotIn(private, str(state))
                        if purpose == 'practice' and session['answered'] == 0:
                            hint = self.post(f'sessions/{session["id"]}/hints/', {'exercise_key': q['key']}, language='ru')
                            self.assertEqual(hint['content_language'], 'ru')
                            self.assertEqual(hint['hint'], translated['exercises'][q['key']]['hint'])
                            self.assertEqual(self.get(f'sessions/{session["id"]}/next/', 'uz')['question']['hint'], q['hint_uz'])
                        payload = {'exercise_key': q['key'], 'response': self.response_for(q, purpose != 'precheck'), 'idempotency_key': str(uuid4())}
                        result = self.post(f'sessions/{session["id"]}/answers/', payload, language='ru')
                        if session['answered'] == 0:
                            replay = self.post(f'sessions/{session["id"]}/answers/', payload, language='uz')
                            self.assertEqual(replay['session']['answered'], result['session']['answered'])
                        if purpose == 'practice':
                            self.assertEqual(result['feedback']['content_language'], 'ru')
                            self.assertEqual(result['feedback']['solution_steps'], translated['exercises'][q['key']]['solution_steps'])
                        else:
                            self.assertNotIn('feedback', result)
                        session = result['session']
                    finished = self.post(f'sessions/{session["id"]}/finish/', language='ru')
                    enrollment = finished['enrollment']
                    self.assertEqual(snapshot, DevelopmentSession.objects.get(pk=session['id']).question_snapshot)
                    if purpose == 'precheck':
                        self.assertEqual(enrollment['stage'], 'study')
                        self.assertEqual(len(enrollment['lessons']), 5)
                        for language in ('uz', 'ru'):
                            state = self.get(f'enrollments/{enrollment["id"]}/', language)
                            self.assertEqual(state['module']['content_language'], language)
                            self.assertTrue(all(l['content_language'] == language for l in state['lessons']))
                            for lesson in state['lessons']:
                                original = next(row for row in data['lessons'] if row['key'] == lesson['key'])
                                local = translated['lessons'][lesson['key']]
                                self.assertEqual(lesson['title'], local['title'] if language == 'ru' else original['title_uz'])
                                self.assertEqual(lesson['theory'], local['theory'] if language == 'ru' else original['theory_uz'])
                                self.assertEqual(lesson['worked_example']['prompt'], local['worked_example']['prompt'] if language == 'ru' else original['worked_example']['prompt_uz'])
                            self.assertEqual(len(state['projects']), 2 if key == 'creative-mini-apps' else 0)
                            self.assertTrue(all(p['content_language'] == language for p in state['projects']))
                            for project in state['projects']:
                                original = next(p for p in data['projects'] if p['key'] == project['key'])
                                local = translated['projects'][project['key']]
                                for name in ('title', 'brief', 'constraints', 'steps', 'deliverables', 'rubric'):
                                    self.assertEqual(project[name], local[name] if language == 'ru' else original[name + '_uz'])
                    if purpose == 'practice':
                        self.assertTrue(enrollment['can_postcheck'])
                self.assertEqual(enrollment['stage'], 'completed')
                self.assertEqual(enrollment['postcheck_score'], 100)
                self.assertEqual(enrollment['delta_percentage_points'], 100)
        self.assertEqual(DevelopmentAnswer.objects.count(), 120)
        self.assertEqual(original_scores, list(IndicatorScore.objects.values()))
        self.assertFalse(StudentAbilityEstimate.objects.exists())
        self.assertFalse(OverallScore.objects.exists())

    def test_active_check_hides_projects_notation_lessons_and_reviews_across_both_clusters(self):
        for source_key in ('arithmetic-algebra', 'algorithmization-flowcharts'):
            user = self.user if source_key == 'arithmetic-algebra' else self.other
            self.client.force_authenticate(user)
            project = self.direct_check(user, 'creative-mini-apps')
            legacy = self.direct_check(user, 'matrices-linear-algebra')
            self.assertEqual(len(self.get(f'enrollments/{project.pk}/', 'ru')['projects']), 2)
            source = enroll(user, source_key)
            check = start_session(user, source.pk, 'precheck')
            for target in (project, legacy):
                state = self.get(f'enrollments/{target.pk}/', 'ru')
                self.assertEqual(state['projects'], [])
                self.assertEqual(state['notation'], [])
                self.assertEqual(state['lessons'], [])
                self.assertTrue(state['learning_locked'])
                self.assertTrue(all('review' not in c for c in state['checks']))
                lesson_key = target.module.lessons.first().key
                self.post(f'enrollments/{target.pk}/lessons/{lesson_key}/complete/', status=409)
                self.post(f'enrollments/{target.pk}/sessions/', {'purpose': 'practice'}, status=409)
            self.post(f'sessions/{check.pk}/hints/', {'exercise_key': check.question_snapshot[0]['key']}, status=409)
            plan = self.get('plan/')
            self.assertTrue(plan['check_active'])
            self.assertEqual(plan['active_enrollment_id'], source.pk)
            self.assertTrue(all(not m['skills'] for m in plan['modules']))
            progress = self.get('progress/', 'ru')
            self.assertTrue(all(not row['lessons'] and not row['projects'] and not row['notation'] for row in progress['enrollments']))

    def test_new_cluster_owner_permissions_and_pinned_hashes(self):
        enrollment = self.post('modules/algorithmization-flowcharts/enroll/')
        session = self.post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': 'precheck'})
        snapshot = deepcopy(DevelopmentSession.objects.get(pk=session['id']).question_snapshot)
        self.client.force_authenticate(self.other)
        self.get(f'enrollments/{enrollment["id"]}/', status=404)
        self.get(f'sessions/{session["id"]}/next/', status=404)
        self.post(f'sessions/{session["id"]}/finish/', status=404)
        self.assertEqual(snapshot, DevelopmentSession.objects.get(pk=session['id']).question_snapshot)
        self.assertEqual(self.get('progress/')['enrollments'], [])

    @override_settings(DEVELOPMENT_CLUSTER1_ENABLED=False)
    def test_existing_development_flag_also_gates_new_cluster(self):
        self.assertFalse(self.get('capabilities/')['available'])
        self.post('modules/creative-mini-apps/enroll/', status=403)
