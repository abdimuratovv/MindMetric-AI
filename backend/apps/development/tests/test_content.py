from copy import deepcopy
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from uuid import uuid4

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import StudentProfile
from apps.assessments.content import MCQ_QUESTIONS
from apps.assessments.models import CognitiveQuestion
from apps.development.admin import ModuleAdmin
from apps.development.content_loader import BUNDLED_CONTENT, import_content, publish_module, read_content
from apps.development.models import (
    DevelopmentAnswer, DevelopmentEnrollment, DevelopmentExercise, DevelopmentLesson,
    DevelopmentModule, DevelopmentSession, DevelopmentSkill, DiagnosticSkillLink,
)
from apps.development.numeric import parse_numeric
from apps.development.permissions import IsDevelopmentEnabled, IsDevelopmentOwner, STUDENT_PERMISSIONS
from apps.development.validation import ContentValidationError, content_hash, validate_content
from apps.scoring.models import Achievement, FieldRecommendation, IndicatorScore, OverallScore, StudentAbilityEstimate


User = get_user_model()


class NumericTests(SimpleTestCase):
    def test_exact_equivalent_inputs(self):
        for value in ('7/4', '14/8', '1.75', '1,75', ' +7 / +4 ', '-7/-4'):
            with self.subTest(value=value):
                self.assertEqual(parse_numeric(value), parse_numeric('7/4'))
        self.assertEqual(parse_numeric('-.5'), parse_numeric('-1/2'))
        self.assertEqual(parse_numeric('0'), 0)

    def test_rejects_expressions_and_unbounded_input(self):
        for value in ('1+3/4', '1e3', '1/0', 'NaN', 'Infinity', '1 2', '1//2', '1,2,3',
                      '9' * 41, ' ' * 81, '', True, 1.75, '__import__("os")'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_numeric(value)


class ManifestTests(SimpleTestCase):
    def setUp(self):
        self.data = read_content(BUNDLED_CONTENT)

    def test_reviewed_manifest_is_valid(self):
        self.assertEqual(validate_content(self.data), self.data)

    def test_review_copy_matches_bundled_content_when_present(self):
        reviewed = Path(__file__).resolve().parents[4] / 'docs/content/cluster1/arithmetic-algebra.v1.json'
        if reviewed.exists():
            self.assertEqual(content_hash(read_content(reviewed)), content_hash(self.data))

    def test_missing_fields_and_malformed_types_are_validation_errors(self):
        for data in ({}, [], {'module': []}, {**self.data, 'skills': [None]},
                     {**self.data, 'schema_version': True}):
            with self.subTest(data_type=type(data).__name__), self.assertRaises(ContentValidationError):
                validate_content(data)

    def test_duplicate_key_is_rejected(self):
        self.data['exercises'][1]['key'] = self.data['exercises'][0]['key']
        with self.assertRaisesMessage(ContentValidationError, 'duplicate key'):
            validate_content(self.data)

    def test_cycles_and_unknown_prerequisites_are_rejected(self):
        for parent in ('arith-equations', 'missing-skill'):
            data = deepcopy(self.data)
            data['skills'][0]['prerequisite_keys'] = [parent]
            with self.subTest(parent=parent), self.assertRaises(ContentValidationError):
                validate_content(data)

    def test_cross_module_prerequisite_must_exist(self):
        self.data['skills'][0]['prerequisite_keys'] = ['external-skill']
        validate_content(self.data, known_skills={'external-skill': []})
        with self.assertRaises(ContentValidationError):
            validate_content(self.data, known_skills={'external-skill': ['arith-equations']})

    def test_check_cannot_contain_hint(self):
        self.data['exercises'][-1]['hint_uz'] = 'Leaked hint'
        with self.assertRaisesMessage(ContentValidationError, 'cannot expose hints'):
            validate_content(self.data)

    def test_numeric_answer_cannot_be_code_or_zero_denominator(self):
        for value in ('1/0', '1+2', '__import__("os")'):
            self.data['exercises'][0]['answer_key']['value'] = value
            with self.subTest(value=value), self.assertRaises(ContentValidationError):
                validate_content(self.data)

    def test_single_answer_must_reference_existing_unique_option(self):
        question = next(q for q in self.data['exercises'] if q['format'] == 'single')
        question['answer_key']['option_id'] = 'missing'
        with self.assertRaisesMessage(ContentValidationError, 'invalid option answer'):
            validate_content(self.data)

    def test_check_bank_and_skill_coverage_are_required(self):
        for field in ('skill_key', 'purpose'):
            data = deepcopy(self.data)
            data['exercises'][-1][field] = 'arith-order' if field == 'skill_key' else 'practice'
            with self.subTest(field=field), self.assertRaises(ContentValidationError):
                validate_content(data)

    def test_blueprint_cannot_mix_practice_and_check(self):
        self.data['blueprint']['postcheck_order'][0] = 'arith-practice-01'
        with self.assertRaisesMessage(ContentValidationError, 'incomplete order'):
            validate_content(self.data)

    def test_invalid_json_is_rejected(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / 'bad.json'
            for value in ('{"value": NaN}', '{incomplete'):
                path.write_text(value, encoding='utf-8')
                with self.subTest(value=value), self.assertRaises(ContentValidationError):
                    read_content(path)


class ContentDatabaseCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = read_content(BUNDLED_CONTENT)
        keys = {link['question_key'] for link in cls.data['diagnostic_links']}
        for indicator, questions in MCQ_QUESTIONS.items():
            for question in questions:
                if question['key'] in keys:
                    CognitiveQuestion.objects.create(indicator_key=indicator, **question)


class ImportTests(ContentDatabaseCase):
    def test_import_creates_only_content_and_remains_draft(self):
        module, changed = import_content(deepcopy(self.data))
        self.assertTrue(changed)
        self.assertEqual(module.status, 'draft')
        self.assertIsNone(module.published_at)
        self.assertEqual(module.skills.count(), 5)
        self.assertEqual(module.lessons.count(), 5)
        self.assertEqual(module.exercises.count(), 20)
        self.assertEqual(DiagnosticSkillLink.objects.count(), 14)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(DevelopmentEnrollment.objects.count(), 0)

    def test_seed_twice_preserves_ids_without_duplicates(self):
        output = StringIO()
        call_command('seed_development_content', stdout=output)
        ids = list(DevelopmentExercise.objects.values_list('key', 'pk'))
        call_command('seed_development_content', stdout=output)
        self.assertEqual(DevelopmentModule.objects.count(), 1)
        self.assertEqual(list(DevelopmentExercise.objects.values_list('key', 'pk')), ids)
        self.assertIn('Content unchanged', output.getvalue())

    def test_dry_run_does_not_write(self):
        call_command('seed_development_content', dry_run=True, stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(), 0)
        self.assertEqual(DevelopmentSkill.objects.count(), 0)

    def test_missing_diagnostic_fails_before_any_writes(self):
        CognitiveQuestion.objects.filter(key='math-easy-2').delete()
        with self.assertRaisesMessage(CommandError, 'Missing diagnostic question: math-easy-2'):
            call_command('seed_development_content', stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(), 0)

    def test_partial_write_failure_rolls_back_entire_import(self):
        with patch.object(DevelopmentExercise.objects, 'update_or_create', side_effect=RuntimeError('simulated failure')):
            with self.assertRaises(RuntimeError):
                import_content(deepcopy(self.data))
        self.assertEqual(DevelopmentModule.objects.count(), 0)
        self.assertEqual(DevelopmentSkill.objects.count(), 0)
        self.assertEqual(DevelopmentLesson.objects.count(), 0)

    def test_invalid_manifest_preserves_existing_draft(self):
        module, _ = import_content(deepcopy(self.data))
        before = module.content_hash
        invalid = deepcopy(self.data)
        invalid['exercises'][0]['answer_key']['value'] = '1/0'
        with self.assertRaises(ContentValidationError):
            import_content(invalid)
        module.refresh_from_db()
        self.assertEqual(module.content_hash, before)
        self.assertEqual(module.exercises.count(), 20)

    def test_draft_revision_reconciles_removed_keys(self):
        module, _ = import_content(deepcopy(self.data))
        import json
        revised = json.loads(json.dumps(self.data).replace('arith-practice-01', 'arith-practice-new'))
        import_content(revised)
        self.assertEqual(module.exercises.count(), 20)
        self.assertFalse(module.exercises.filter(key='arith-practice-01').exists())
        self.assertTrue(module.exercises.filter(key='arith-practice-new').exists())

    def test_skill_replacement_cannot_leave_stale_prerequisite(self):
        import_content(deepcopy(self.data))
        revised = deepcopy(self.data)
        revised['skills'][0]['prerequisite_keys'] = ['arith-removed']
        with self.assertRaisesMessage(ContentValidationError, 'Unknown prerequisite'):
            import_content(revised)

    def test_publishing_freezes_rows_and_same_manifest_is_idempotent(self):
        module, _ = import_content(deepcopy(self.data))
        published = publish_module(module.pk)
        self.assertIsNotNone(published.published_at)
        same, changed = import_content(deepcopy(self.data))
        self.assertFalse(changed)
        self.assertEqual(same.pk, module.pk)
        revised = deepcopy(self.data)
        revised['module']['title_uz'] += ' changed'
        with self.assertRaisesMessage(ContentValidationError, 'increment module.version'):
            import_content(revised)

    def test_new_version_preserves_enrollment_and_old_content(self):
        module, _ = import_content(deepcopy(self.data))
        module = publish_module(module.pk)
        student = User.objects.create_user('student@university.edu')
        enrollment = DevelopmentEnrollment.objects.create(student=student, module=module,
                                                        diagnostic_snapshot={'math': 42})
        revised = deepcopy(self.data)
        revised['module']['version'] = 2
        revised['module']['title_uz'] += ' v2'
        new, _ = import_content(revised)
        enrollment.refresh_from_db()
        module.refresh_from_db()
        self.assertNotEqual(module.pk, new.pk)
        self.assertEqual(enrollment.module_id, module.pk)
        self.assertEqual(enrollment.diagnostic_snapshot, {'math': 42})
        self.assertEqual(module.content_hash, content_hash(self.data))
        self.assertEqual(new.status, 'draft')

    def test_frozen_model_edits_and_deletion_are_blocked(self):
        module, _ = import_content(deepcopy(self.data))
        publish_module(module.pk)
        exercise = module.exercises.first()
        exercise.prompt_uz = 'Changed'
        with self.assertRaises(ValidationError):
            exercise.save()
        with self.assertRaises(ValidationError), transaction.atomic():
            module.exercises.filter(pk=exercise.pk).delete()
        module.refresh_from_db()
        module.title_uz = 'Changed'
        with self.assertRaises(ValidationError):
            module.save()

    def test_cached_draft_cannot_add_to_published_version(self):
        module, _ = import_content(deepcopy(self.data))
        publish_module(module.pk)
        with self.assertRaises(ValidationError):
            DevelopmentSkill.objects.create(module=module, key='extra', title_uz='Extra')

    def test_frozen_prerequisites_cannot_be_edited_in_either_direction(self):
        module, _ = import_content(deepcopy(self.data))
        skill = module.skills.get(key='arith-fractions')
        parent = module.skills.get(key='arith-order')
        publish_module(module.pk)
        with self.assertRaises(ValidationError), transaction.atomic():
            skill.prerequisites.clear()
        with self.assertRaises(ValidationError), transaction.atomic():
            parent.dependents.remove(skill)

    def test_draft_m2m_prerequisite_cycle_is_blocked(self):
        module, _ = import_content(deepcopy(self.data))
        order = module.skills.get(key='arith-order')
        fractions = module.skills.get(key='arith-fractions')
        with self.assertRaises(ValidationError):
            order.prerequisites.add(fractions)

    def test_import_does_not_change_diagnostic_state_or_accounts(self):
        student = User.objects.create_user('existing@university.edu')
        rows = [
            IndicatorScore.objects.create(student=student, indicator_key='math', score=42),
            StudentAbilityEstimate.objects.create(student=student, indicator_key='math', theta=0.7),
            OverallScore.objects.create(student=student, score=42, band='test'),
            FieldRecommendation.objects.create(student=student, fit_scores={'backend': 42}),
            Achievement.objects.create(student=student, indicator_key='math', tier='bronze', score=42),
        ]
        snapshots = [(type(row), list(type(row).objects.values())) for row in rows]
        import_content(deepcopy(self.data))
        for model, before in snapshots:
            self.assertEqual(list(model.objects.values()), before)
        self.assertEqual(User.objects.count(), 1)


class ProgressFoundationTests(ContentDatabaseCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        module, _ = import_content(deepcopy(cls.data))
        cls.module = publish_module(module.pk)
        cls.student = User.objects.create_user('owner@university.edu')
        cls.other = User.objects.create_user('other@university.edu')
        StudentProfile.objects.create(user=cls.student, completed_at=timezone.now())
        cls.enrollment = DevelopmentEnrollment.objects.create(student=cls.student, module=cls.module)

    def make_session(self, purpose='practice'):
        return DevelopmentSession.objects.create(enrollment=self.enrollment, purpose=purpose,
                                                 question_snapshot=[{'key': 'arith-practice-01'}])

    def test_only_one_active_session_per_enrollment(self):
        self.make_session()
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.make_session('precheck')

    def test_enrollment_cannot_move_between_students(self):
        self.enrollment.student = self.other
        with self.assertRaises(ValidationError):
            self.enrollment.save()

    def test_draft_and_teacher_enrollment_are_rejected(self):
        revised = deepcopy(self.data)
        revised['module']['version'] = 2
        draft, _ = import_content(revised)
        with self.assertRaises(ValidationError):
            DevelopmentEnrollment.objects.create(student=self.student, module=draft)
        teacher = User.objects.create_user('teacher@university.edu', role='teacher')
        with self.assertRaises(ValidationError):
            DevelopmentEnrollment.objects.create(student=teacher, module=self.module)

    def test_session_snapshot_is_immutable(self):
        session = self.make_session()
        session.question_snapshot = []
        with self.assertRaises(ValidationError):
            session.save()

    def test_diagnostic_baseline_is_immutable(self):
        self.enrollment.diagnostic_snapshot = {'math': 100}
        with self.assertRaises(ValidationError):
            self.enrollment.save()

    def test_answer_idempotency_and_attempt_are_database_constraints(self):
        session = self.make_session()
        exercise = self.module.exercises.get(key='arith-practice-01')
        token = uuid4()
        DevelopmentAnswer.objects.create(session=session, exercise=exercise,
                                         idempotency_key=token, response={'value': '20'}, correctness=1)
        for retry in ({'idempotency_key': token, 'attempt_number': 2},
                      {'idempotency_key': uuid4(), 'attempt_number': 1}):
            with self.subTest(retry=retry), self.assertRaises(IntegrityError), transaction.atomic():
                DevelopmentAnswer.objects.create(session=session, exercise=exercise,
                                                 response={'value': '20'}, correctness=1, **retry)

    def test_answer_purpose_and_version_cannot_be_mixed(self):
        session = self.make_session()
        check = self.module.exercises.get(key='arith-precheck-01')
        with self.assertRaises(ValidationError):
            DevelopmentAnswer.objects.create(session=session, exercise=check, idempotency_key=uuid4(),
                                             response={'option_id': 'a'}, correctness=1)
        revised = deepcopy(self.data)
        revised['module']['version'] = 2
        new, _ = import_content(revised)
        with self.assertRaises(ValidationError):
            DevelopmentAnswer.objects.create(session=session, exercise=new.exercises.get(key='arith-practice-01'),
                                             idempotency_key=uuid4(), response={'value': '20'}, correctness=1)

    def test_correctness_range_is_enforced_by_database(self):
        session = self.make_session()
        with self.assertRaises(IntegrityError), transaction.atomic():
            DevelopmentAnswer.objects.create(session=session, exercise=self.module.exercises.get(key='arith-practice-01'),
                                             idempotency_key=uuid4(), response={'value': '20'}, correctness=2)

    def test_recorded_answers_cannot_be_overwritten(self):
        answer = DevelopmentAnswer.objects.create(session=self.make_session(),
            exercise=self.module.exercises.get(key='arith-practice-01'), idempotency_key=uuid4(),
            response={'value': '20'}, correctness=1)
        answer.correctness = 0
        with self.assertRaises(ValidationError):
            answer.save()

    @override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
    def test_student_permission_requires_profile_and_flag(self):
        request = RequestFactory().get('/')
        request.user = self.student
        self.assertTrue(all(permission().has_permission(request, None) for permission in STUDENT_PERMISSIONS))
        request.user = self.other
        self.assertFalse(all(permission().has_permission(request, None) for permission in STUDENT_PERMISSIONS))
        request.user = User.objects.create_user('staff-teacher@university.edu', role='teacher', is_staff=True)
        self.assertFalse(all(permission().has_permission(request, None) for permission in STUDENT_PERMISSIONS))

    @override_settings(DEVELOPMENT_CLUSTER1_ENABLED=False)
    def test_feature_flag_denies_access(self):
        self.assertFalse(IsDevelopmentEnabled().has_permission(None, None))

    def test_owner_permission_handles_nested_objects(self):
        session = self.make_session()
        answer = DevelopmentAnswer.objects.create(session=session,
            exercise=self.module.exercises.get(key='arith-practice-01'), idempotency_key=uuid4(),
            response={'value': '20'}, correctness=1)
        request = RequestFactory().get('/')
        permission = IsDevelopmentOwner()
        for obj in (self.enrollment, session, answer):
            request.user = self.student
            self.assertTrue(permission.has_object_permission(request, None, obj))
            request.user = self.other
            self.assertFalse(permission.has_object_permission(request, None, obj))
        self.assertFalse(permission.has_object_permission(request, None, self.module))

    def test_admin_requires_staff_and_product_admin_role(self):
        model_admin = ModuleAdmin(DevelopmentModule, admin.site)
        request = RequestFactory().get('/')
        for role, staff, expected in (('admin', True, True), ('admin', False, False),
                                      ('teacher', True, False), ('student', True, False)):
            request.user = User.objects.create_user(f'{role}-{staff}@university.edu', role=role, is_staff=staff)
            self.assertEqual(model_admin.has_view_permission(request), expected)
            self.assertEqual(model_admin.has_publish_permission(request), expected)
            self.assertFalse(model_admin.has_add_permission(request))
            self.assertFalse(model_admin.has_change_permission(request))
            self.assertFalse(model_admin.has_delete_permission(request))

    @override_settings(ALLOWED_HOSTS=['testserver'], STORAGES={
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    })
    def test_admin_http_publish_action_is_available_to_staff_admin(self):
        staff = User.objects.create_user('publisher@university.edu', role='admin', is_staff=True)
        self.client.force_login(staff)
        revised = deepcopy(self.data)
        revised['module']['version'] = 2
        draft, _ = import_content(revised)
        url = reverse('admin:development_developmentmodule_changelist')
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url, {'action': 'publish_selected', '_selected_action': [draft.pk]})
        self.assertEqual(response.status_code, 302)
        draft.refresh_from_db()
        self.assertEqual(draft.status, 'published')

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_staff_teacher_cannot_read_admin_content(self):
        teacher = User.objects.create_user('restricted@university.edu', role='teacher', is_staff=True)
        self.client.force_login(teacher)
        response = self.client.get(reverse('admin:development_developmentmodule_changelist'))
        self.assertEqual(response.status_code, 403)
