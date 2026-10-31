"""The additive cluster column must not rewrite pinned legacy content."""
from django.conf import settings
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.utils import timezone


class ClusterMigrationTests(TransactionTestCase):
    def test_legacy_published_content_and_session_snapshots_survive_cluster_backfill(self):
        before = [('development', '0002_developmentenrollment_completed_lesson_keys')]
        after = [('development', '0003_developmentmodule_cluster')]
        executor = MigrationExecutor(connection)
        executor.migrate(before)
        self.addCleanup(lambda: MigrationExecutor(connection).migrate(after))
        old = executor.loader.project_state(before).apps
        User = old.get_model(*settings.AUTH_USER_MODEL.split('.'))
        Module = old.get_model('development', 'DevelopmentModule')
        Enrollment = old.get_model('development', 'DevelopmentEnrollment')
        Session = old.get_model('development', 'DevelopmentSession')
        user = User.objects.create(email='migration-pinned@university.edu', role='student', password='!')
        manifest = {'schema_version': 1, 'legacy': 'unchanged'}
        module = Module.objects.create(key='legacy-migration-check', version=1, order=4,
                                       title_uz='Saqlanadigan mavzu', content_hash='a' * 64,
                                       content_snapshot=manifest, status='published', published_at=timezone.now())
        enrollment = Enrollment.objects.create(student_id=user.pk, module_id=module.pk,
                                                diagnostic_snapshot={'baseline': 42}, completed_lesson_keys=['old-lesson'])
        questions = [{'key': 'old-question', 'answer_key': {'value': '7'}}]
        session = Session.objects.create(enrollment_id=enrollment.pk, purpose='precheck', number=1,
                                         question_snapshot=questions)
        executor = MigrationExecutor(connection); executor.migrate(after)
        new = executor.loader.project_state(after).apps
        updated = new.get_model('development', 'DevelopmentModule').objects.get(pk=module.pk)
        self.assertEqual(updated.cluster, 1)
        self.assertEqual(updated.content_hash, 'a' * 64)
        self.assertEqual(updated.content_snapshot, manifest)
        self.assertEqual(updated.status, 'published')
        self.assertEqual(new.get_model('development', 'DevelopmentEnrollment').objects.get(pk=enrollment.pk).diagnostic_snapshot, {'baseline': 42})
        self.assertEqual(new.get_model('development', 'DevelopmentSession').objects.get(pk=session.pk).question_snapshot, questions)
