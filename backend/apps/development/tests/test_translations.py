import json
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import StudentProfile
from apps.assessments.content import MCQ_QUESTIONS
from apps.assessments.models import CognitiveQuestion
from apps.development.content_loader import bundled_contents,import_bundle,publish_module
from apps.development.models import DevelopmentAnswer,DevelopmentModule,DevelopmentSession
from apps.development.progress import start_session,submit_answer,finish_session,complete_lesson
from apps.development.translations import DIRECTORY,bundled_translation,validate_translation
from apps.development.validation import ContentValidationError
from .test_content import ContentDatabaseCase


class TranslationResourceTests(SimpleTestCase):
    def test_all_fields_and_math_constants_are_reviewed_and_copies_match(self):
        reviewed=Path(__file__).resolve().parents[4]/'docs/content/cluster1/translations'
        for key in ('arithmetic-algebra','matrices-linear-algebra'):
            translated=bundled_translation(key,1)
            self.assertEqual(translated,json.loads((reviewed/f'{key}.v1.ru.json').read_text(encoding='utf-8')))
            self.assertEqual(len(translated['lessons']),5)
            self.assertEqual(len(translated['exercises']),20)
            self.assertNotIn('answer_key',json.dumps(translated))

    def test_wrong_hash_incomplete_translation_and_changed_options_are_rejected(self):
        source=next(d for d in bundled_contents() if d['module']['key']=='arithmetic-algebra')
        original=bundled_translation('arithmetic-algebra',1)
        changes=[lambda d:d.update(source_hash='0'*64),
                 lambda d:d['lessons'].pop('arith-lesson-order'),
                 lambda d:d['exercises']['arith-precheck-01']['options'].pop('a'),
                 lambda d:d['exercises']['arith-precheck-01'].update(hint='Подсказка'),
                 lambda d:d['exercises']['arith-practice-01'].update(answer_key={'value':'20'}),
                 lambda d:d['exercises']['arith-practice-01'].update(prompt='Вычислите 999.')]
        for change in changes:
            data=deepcopy(original);change(data)
            with self.assertRaises(ContentValidationError):validate_translation(source,data)


@override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
class TranslationAPITests(ContentDatabaseCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        contents=bundled_contents()
        keys={link['question_key'] for d in contents for link in d['diagnostic_links']}
        for indicator,rows in MCQ_QUESTIONS.items():
            for row in rows:
                if row['key'] in keys:
                    CognitiveQuestion.objects.get_or_create(key=row['key'],defaults={'indicator_key':indicator,**{k:v for k,v in row.items() if k!='key'}})
        for _,module,_ in import_bundle(contents):publish_module(module.pk)
        cls.user=get_user_model().objects.create_user('language@university.edu')
        StudentProfile.objects.create(user=cls.user,completed_at=timezone.now())

    def setUp(self):
        cache.clear();self.client=APIClient();self.client.force_authenticate(self.user)

    def get(self,path,language='ru'):
        result=self.client.get('/api/development/'+path,HTTP_X_LANGUAGE=language)
        self.assertEqual(result.status_code,200,result.data)
        return result.data

    def enroll(self,key='arithmetic-algebra'):
        result=self.client.post(f'/api/development/modules/{key}/enroll/',{},format='json',HTTP_X_LANGUAGE='uz')
        self.assertEqual(result.status_code,200,result.data)
        return self.user.development_enrollments.get(pk=result.data['id'])

    def study(self,key='arithmetic-algebra'):
        enrollment=self.enroll(key)
        session=start_session(self.user,enrollment.pk,'precheck')
        for q in session.question_snapshot:
            response={'value':'999'} if q['format']=='numeric' else {'option_id':next(o['id'] for o in q['options'] if o['id']!=q['answer_key']['option_id'])}
            submit_answer(self.user,session.pk,exercise_key=q['key'],response=response,idempotency_key=uuid4())
        finish_session(self.user,session.pk)
        return enrollment

    def test_catalogue_plan_skill_names_and_fallback_follow_language(self):
        hashes=list(DevelopmentModule.objects.values_list('pk','content_hash','content_snapshot'))
        for language in ('uz','ru','uz'):
            data=self.get('plan/',language)
            by_key={m['key']:m for m in data['modules']}
            for key in ('arithmetic-algebra','matrices-linear-algebra'):
                self.assertEqual(by_key[key]['content_language'],language)
                if language=='ru':self.assertRegex(by_key[key]['title'],'[А-Яа-я]')
                self.assertTrue(all(s['content_language']==language for s in by_key[key]['skills']))
            self.assertEqual(by_key['mathematical-logic']['content_language'],'uz')
        self.assertEqual(hashes,list(DevelopmentModule.objects.values_list('pk','content_hash','content_snapshot')))

    def test_active_pinned_v1_check_swaps_text_without_advancing_or_revealing_answers(self):
        enrollment=self.enroll()
        session=start_session(self.user,enrollment.pk,'precheck')
        before=deepcopy(session.question_snapshot)
        uz=self.get(f'enrollments/{enrollment.pk}/','uz')
        ru=self.get(f'enrollments/{enrollment.pk}/','ru')
        self.assertEqual(ru['module']['version'],1)
        self.assertNotEqual(uz['active_session']['question']['prompt'],ru['active_session']['question']['prompt'])
        for language in ('ru','uz'):
            state=self.get(f'sessions/{session.pk}/next/',language)
            self.assertEqual((state['id'],state['answered']),(session.pk,0))
            self.assertEqual([o['id'] for o in state['question']['options']],['a','b','c','d'])
            for forbidden in ('answer_key','solution_steps','feedback','last_feedback','hint','review'):
                self.assertNotIn(forbidden,json.dumps(state))
        session.refresh_from_db()
        self.assertEqual(session.question_snapshot,before)
        self.assertEqual(DevelopmentAnswer.objects.count(),0)

    def test_lessons_examples_completed_reviews_and_progress_translate_for_both_modules(self):
        for key in ('arithmetic-algebra','matrices-linear-algebra'):
            enrollment=self.study(key)
            ru=self.get(f'enrollments/{enrollment.pk}/','ru')
            uz=self.get(f'enrollments/{enrollment.pk}/','uz')
            self.assertEqual([l['key'] for l in ru['lessons']],[l['key'] for l in uz['lessons']])
            for lesson in ru['lessons']:
                self.assertEqual(lesson['content_language'],'ru')
                self.assertRegex(lesson['title'],'[А-Яа-я]')
                self.assertRegex(lesson['worked_example']['prompt'],'[А-Яа-я]')
                self.assertEqual(lesson['worked_example']['prompt'],lesson['worked_example']['prompt_uz'])
            self.assertTrue(all(r['content_language']=='ru' for r in ru['checks'][0]['review']))
            self.assertTrue(all(r['content_language']=='ru' for r in ru['skill_progress']))
            all_progress=self.get('progress/','ru')['enrollments']
            self.assertTrue(all(p['module']['content_language']=='ru' for p in all_progress))

    def test_language_change_keeps_answer_uuid_and_response_idempotent(self):
        enrollment=self.enroll()
        session=start_session(self.user,enrollment.pk,'precheck')
        q=session.question_snapshot[0];key=uuid4()
        payload={'exercise_key':q['key'],'response':q['answer_key'],'idempotency_key':str(key)}
        for language in ('uz','ru'):
            response=self.client.post(f'/api/development/sessions/{session.pk}/answers/',payload,format='json',HTTP_X_LANGUAGE=language)
            self.assertEqual(response.status_code,200,response.data)
            self.assertEqual(response.data['session']['answered'],1)
        self.assertEqual(DevelopmentAnswer.objects.count(),1)
        self.assertEqual(DevelopmentAnswer.objects.get().response,q['answer_key'])

    def test_practice_hints_and_open_feedback_survive_language_switch(self):
        enrollment=self.study()
        for lesson in enrollment.module.lessons.all():complete_lesson(self.user,enrollment.pk,lesson.key)
        session=start_session(self.user,enrollment.pk,'practice')
        question=session.question_snapshot[0]
        hints=[]
        for language in ('uz','ru'):
            r=self.client.post(f'/api/development/sessions/{session.pk}/hints/',{'exercise_key':question['key']},format='json',HTTP_X_LANGUAGE=language)
            self.assertEqual(r.status_code,200);hints.append(r.data['hint'])
        self.assertNotEqual(*hints)
        state=self.get(f'sessions/{session.pk}/next/','ru')
        self.assertEqual(state['question']['hint'],hints[1])
        submit_answer(self.user,session.pk,exercise_key=question['key'],response=question['answer_key'],idempotency_key=uuid4())
        state=self.get(f'enrollments/{enrollment.pk}/','ru')
        previous=state['active_session']['last_feedback']
        self.assertEqual(previous['exercise_key'],question['key'])
        self.assertEqual(previous['content_language'],'ru')
        self.assertTrue(previous['hint_used'])
        session.refresh_from_db()
        self.assertEqual(len(session.hint_usage),1)

    def test_unsupported_version_never_receives_incompatible_overlay(self):
        from apps.development.translations import ContentLocale
        module=DevelopmentModule.objects.get(key='arithmetic-algebra')
        module.content_hash='0'*64
        self.assertEqual(ContentLocale(module,'ru').language,'uz')
        module.version=999
        self.assertEqual(ContentLocale(module,'ru').language,'uz')
