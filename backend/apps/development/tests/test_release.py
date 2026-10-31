import os
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError

from django.contrib.auth import get_user_model
from apps.assessments.content import MCQ_QUESTIONS
from apps.assessments.models import CognitiveQuestion
from apps.development.content_loader import bundled_contents, publish_module
from apps.development.models import DevelopmentModule, DevelopmentExercise
from apps.development.translations import bundled_translation
from .test_content import ContentDatabaseCase


class ReleaseTests(ContentDatabaseCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        required = {link['question_key'] for data in bundled_contents() for link in data['diagnostic_links']}
        for indicator, questions in MCQ_QUESTIONS.items():
            for question in questions:
                if question['key'] in required:
                    CognitiveQuestion.objects.get_or_create(key=question['key'], defaults={
                        'indicator_key':indicator, **{k:v for k,v in question.items() if k!='key'},
                    })

    @patch.dict(os.environ, {'RENDER': ''})
    def test_release_publishes_six_modules_and_is_idempotent(self):
        output=StringIO()
        call_command('activate_development_cluster1',stdout=output)
        ids=list(DevelopmentExercise.objects.order_by('pk').values_list('pk',flat=True))
        call_command('activate_development_cluster1',stdout=output)
        self.assertEqual(DevelopmentModule.objects.filter(status='published').count(),6)
        self.assertEqual(len(ids),120)
        self.assertEqual(list(DevelopmentExercise.objects.order_by('pk').values_list('pk',flat=True)),ids)
        self.assertEqual(get_user_model().objects.count(),0)

    @patch.dict(os.environ, {'RENDER': 'true'})
    @patch('apps.development.management.commands.activate_development_cluster1.connection.vendor', 'sqlite')
    def test_render_sqlite_is_rejected_before_writes(self):
        with self.assertRaisesMessage(CommandError,'persistent PostgreSQL'):
            call_command('activate_development_cluster1',stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(),0)

    @patch.dict(os.environ, {'RENDER': ''})
    def test_missing_or_stale_russian_topic_blocks_both_releases_before_import(self):
        original = bundled_translation
        for command in ('activate_development_cluster1', 'activate_development_cluster2'):
            for key in ('mathematical-logic', 'sets-and-relations',
                        'number-theory-discrete-mathematics', 'functions-sequences-combinatorics'):
                for missing in (True, False):
                    def broken(topic, version):
                        value = original(topic, version)
                        if topic == key:
                            return None if missing else {**value, 'source_hash': '0'*64}
                        return value
                    with self.subTest(command=command, key=key, missing=missing), patch(
                        'apps.development.translations.bundled_translation', side_effect=broken
                    ), patch('apps.development.management.commands.'+command+'.import_bundle') as importer:
                        with self.assertRaises(CommandError):
                            call_command(command, stdout=StringIO())
                        importer.assert_not_called()
                    self.assertFalse(DevelopmentModule.objects.exists())

    @patch.dict(os.environ, {'RENDER': ''})
    def test_late_publication_failure_rolls_back_whole_bundle(self):
        count=0
        def publish_then_fail(pk):
            nonlocal count
            count+=1
            if count==6:
                raise RuntimeError('publication failure')
            return publish_module(pk)
        with patch('apps.development.management.commands.activate_development_cluster1.publish_module',side_effect=publish_then_fail):
            with self.assertRaisesMessage(RuntimeError,'publication failure'):
                call_command('activate_development_cluster1',stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(),0)
