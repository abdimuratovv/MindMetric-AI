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
    def test_release_publishes_five_modules_and_is_idempotent(self):
        output=StringIO()
        call_command('activate_development_cluster1',stdout=output)
        ids=list(DevelopmentExercise.objects.order_by('pk').values_list('pk',flat=True))
        call_command('activate_development_cluster1',stdout=output)
        self.assertEqual(DevelopmentModule.objects.filter(status='published').count(),5)
        self.assertEqual(len(ids),100)
        self.assertEqual(list(DevelopmentExercise.objects.order_by('pk').values_list('pk',flat=True)),ids)
        self.assertEqual(get_user_model().objects.count(),0)

    @patch.dict(os.environ, {'RENDER': 'true'})
    def test_render_sqlite_is_rejected_before_writes(self):
        with self.assertRaisesMessage(CommandError,'persistent PostgreSQL'):
            call_command('activate_development_cluster1',stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(),0)

    @patch.dict(os.environ, {'RENDER': ''})
    def test_late_publication_failure_rolls_back_whole_bundle(self):
        count=0
        def publish_then_fail(pk):
            nonlocal count
            count+=1
            if count==5:
                raise RuntimeError('publication failure')
            return publish_module(pk)
        with patch('apps.development.management.commands.activate_development_cluster1.publish_module',side_effect=publish_then_fail):
            with self.assertRaisesMessage(RuntimeError,'publication failure'):
                call_command('activate_development_cluster1',stdout=StringIO())
        self.assertEqual(DevelopmentModule.objects.count(),0)
