from copy import deepcopy
from io import StringIO
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import StudentProfile
from apps.assessments.content import MCQ_QUESTIONS
from apps.assessments.models import CognitiveQuestion
from apps.development.content_loader import bundled_contents, import_bundle, import_content, publish_module
from apps.development.models import DevelopmentAnswer, DevelopmentEnrollment, DevelopmentExercise, DevelopmentModule, DevelopmentSkill, DiagnosticSkillLink
from apps.development.validation import ContentValidationError, validate_content
from .test_content import ContentDatabaseCase


class BundleTests(ContentDatabaseCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.contents = bundled_contents()
        required = {link['question_key'] for data in cls.contents for link in data['diagnostic_links']}
        for indicator, questions in MCQ_QUESTIONS.items():
            for question in questions:
                if question['key'] in required:
                    CognitiveQuestion.objects.get_or_create(key=question['key'], defaults={
                        'indicator_key': indicator, **{key: value for key, value in question.items() if key != 'key'},
                    })

    def test_all_six_manifests_import_prerequisite_first_even_reversed(self):
        result = import_bundle(list(reversed(deepcopy(self.contents))))
        self.assertEqual(result[0][0]['module']['key'], 'arithmetic-algebra')
        self.assertEqual(DevelopmentModule.objects.count(), 6)
        self.assertEqual(DevelopmentSkill.objects.count(), 30)
        self.assertEqual(DevelopmentExercise.objects.count(), 120)
        self.assertEqual(DiagnosticSkillLink.objects.count(), 29)
        self.assertEqual(set(DevelopmentModule.objects.values_list('status', flat=True)), {'draft'})
        self.assertEqual(DevelopmentEnrollment.objects.count(), 0)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_all_command_is_idempotent_and_keeps_original_single_default(self):
        output = StringIO()
        call_command('seed_development_content', stdout=output)
        self.assertEqual(DevelopmentModule.objects.count(), 1)
        call_command('seed_development_content', all=True, stdout=output)
        ids = list(DevelopmentExercise.objects.values_list('pk', 'key').order_by('pk'))
        call_command('seed_development_content', all=True, stdout=output)
        self.assertEqual(list(DevelopmentExercise.objects.values_list('pk', 'key').order_by('pk')), ids)
        self.assertEqual(DevelopmentModule.objects.count(), 6)

    def test_whole_bundle_dry_run_resolves_cross_module_dependencies_without_writes(self):
        output = StringIO()
        call_command('seed_development_content', all=True, dry_run=True, stdout=output)
        self.assertEqual(DevelopmentModule.objects.count(), 0)
        self.assertEqual(DevelopmentSkill.objects.count(), 0)
        self.assertEqual(output.getvalue().count('Validated without writes'), 6)

    def test_missing_diagnostic_in_last_module_prevents_entire_bundle(self):
        data = deepcopy(self.contents)
        data[-2]['diagnostic_links'][0]['question_key'] = 'missing-question'
        with self.assertRaisesMessage(ContentValidationError, 'Missing diagnostic question'):
            import_bundle(data)
        self.assertFalse(DevelopmentModule.objects.exists())

    def test_failure_after_earlier_module_writes_rolls_back_whole_bundle(self):
        def import_until_last(data):
            if data['module']['key'] == 'matrices-linear-algebra':
                raise RuntimeError('simulated late failure')
            return import_content(data)
        with patch('apps.development.content_loader.import_content', side_effect=import_until_last):
            with self.assertRaises(RuntimeError):
                import_bundle(deepcopy(self.contents))
        self.assertEqual(DevelopmentModule.objects.count(), 0)
        self.assertEqual(DevelopmentExercise.objects.count(), 0)

    def test_missing_prerequisite_module_is_not_silently_dropped(self):
        matrix = next(data for data in self.contents if data['module']['order'] == 6)
        with self.assertRaisesMessage(ContentValidationError, 'Unknown prerequisite'):
            import_bundle([deepcopy(matrix)])

    def test_no_diagnostic_links_requires_explicit_coverage_note(self):
        data = deepcopy(self.contents)
        graph = {skill['key']: skill['prerequisite_keys'] for row in data for skill in row['skills']}
        matrix = next(row for row in data if row['module']['order'] == 6)
        self.assertEqual(matrix['diagnostic_links'], [])
        validate_content(matrix, known_skills=graph)
        del matrix['module']['diagnostic_coverage_note_uz']
        with self.assertRaisesMessage(ContentValidationError, 'diagnostic_coverage_note_uz'):
            validate_content(matrix, known_skills=graph)

    def test_module_dependency_cycle_is_rejected_without_any_writes(self):
        data = deepcopy(self.contents)
        arithmetic = next(row for row in data if row['module']['order'] == 1)
        matrix = next(row for row in data if row['module']['order'] == 6)
        arithmetic['skills'][0]['prerequisite_keys'] = ['matrices-determinant']
        matrix['skills'][-1]['prerequisite_keys'] = []
        with self.assertRaisesMessage(ContentValidationError, 'Module prerequisite cycle'):
            import_bundle(data)
        self.assertEqual(DevelopmentModule.objects.count(), 0)

    def test_duplicate_module_keys_are_rejected(self):
        duplicate = deepcopy(self.contents[0])
        duplicate['module']['version'] = 2
        with self.assertRaisesMessage(ContentValidationError, 'one version per module'):
            import_bundle([deepcopy(self.contents[0]), duplicate])

    @override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
    def test_each_new_module_runs_full_learning_flow_without_changing_diagnostics(self):
        cache.clear()
        rows = import_bundle(deepcopy(self.contents))
        for _, module, _ in rows:
            publish_module(module.pk)
        user = get_user_model().objects.create_user('bundle-learner@university.edu')
        StudentProfile.objects.create(user=user, completed_at=timezone.now())
        client = APIClient()
        client.force_authenticate(user)
        root = '/api/development/'

        def post(path, payload=None):
            response = client.post(root + path, payload or {}, format='json')
            self.assertEqual(response.status_code, 200, response.data)
            return response.data

        def solve(session, *, wrong=False):
            while session['question']:
                key = session['question']['key']
                question = DevelopmentExercise.objects.get(module__key=active_key, key=key)
                if question.format == 'numeric':
                    value = {'value': '999' if wrong else question.answer_key['value']}
                else:
                    option = question.answer_key['option_id']
                    if wrong:
                        option = next(o['id'] for o in question.options if o['id'] != option)
                    value = {'option_id': option}
                result = post(f'sessions/{session["id"]}/answers/', {
                    'exercise_key': key, 'response': value, 'idempotency_key': str(uuid4()),
                })
                session = result['session']
            return post(f'sessions/{session["id"]}/finish/')['enrollment']

        for data in self.contents:
            if data['module']['order'] == 1:
                continue
            # Isolate each course flow; this is not a 35-write/hour throttle test.
            cache.clear()
            active_key = data['module']['key']
            enrollment = post(f'modules/{active_key}/enroll/')
            session = post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': 'precheck'})
            enrollment = solve(session, wrong=True)
            for lesson in enrollment['lessons']:
                enrollment = post(f'enrollments/{enrollment["id"]}/lessons/{lesson["key"]}/complete/')
            session = post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': 'practice'})
            enrollment = solve(session)
            self.assertTrue(enrollment['can_postcheck'])
            session = post(f'enrollments/{enrollment["id"]}/sessions/', {'purpose': 'postcheck'})
            enrollment = solve(session)
            self.assertEqual(enrollment['postcheck_score'], 100)
            self.assertEqual(enrollment['stage'], 'completed')
            self.assertEqual(enrollment['delta_percentage_points'], 100)
        self.assertEqual(DevelopmentAnswer.objects.count(), 100)
        self.assertEqual(user.indicator_scores.count(), 0)
        self.assertEqual(DevelopmentModule.objects.get(key='matrices-linear-algebra').skills.filter(diagnostic_links__isnull=False).count(), 0)
