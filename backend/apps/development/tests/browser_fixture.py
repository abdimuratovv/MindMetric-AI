"""Initialize only the explicitly selected disposable browser database."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
os.environ['DJANGO_SETTINGS_MODULE'] = 'apps.development.tests.browser_settings'

import django
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from apps.accounts.models import StudentProfile
from apps.assessments.content import MCQ_QUESTIONS
from apps.assessments.models import CognitiveQuestion
from apps.development.content_loader import BUNDLED_CONTENT, bundled_contents, import_bundle, publish_module, read_content

call_command('migrate', verbosity=0, interactive=False)
contents = bundled_contents() if os.environ.get('DEVELOPMENT_BROWSER_ALL_CONTENT') == '1' else [read_content(BUNDLED_CONTENT)]
keys = {link['question_key'] for data in contents for link in data['diagnostic_links']}
for indicator, questions in MCQ_QUESTIONS.items():
    for question in questions:
        if question['key'] in keys:
            CognitiveQuestion.objects.create(indicator_key=indicator, **question)
for _, module, _ in import_bundle(contents):
    publish_module(module.pk)
user = get_user_model().objects.create_user('development-smoke@university.edu', first_name='Development', last_name='Smoke')
StudentProfile.objects.create(user=user, faculty='Test', course='1', group='Smoke', specialization='Test', completed_at=timezone.now())
Path(os.environ['DEVELOPMENT_BROWSER_TOKEN_PATH']).write_text(json.dumps({'access': str(AccessToken.for_user(user)), 'user_id': user.pk}), encoding='utf-8')
print('Disposable browser fixture ready.')
