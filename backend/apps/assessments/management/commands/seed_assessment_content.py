"""
Loads apps/assessments/content.py into the database and creates demo
accounts (one student login, two admin logins, plus a small student roster
so the review queue and admin dashboards have something to show). Safe to
re-run — everything is an upsert.

Usage: python manage.py seed_assessment_content
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import StudentProfile
from apps.assessments.anagram_content import ANAGRAM_ITEMS
from apps.assessments.content import CODING_PROBLEMS, MCQ_QUESTIONS
from apps.assessments.feedback_content import QUESTION_FEEDBACK
from apps.assessments.learning_content import LEARNING_MODULES
from apps.assessments.models import (
    AnagramItem, CodingProblem, CognitiveQuestion, LearningItem, LearningModule, SjtScenario,
)
from apps.assessments.sjt_content import SJT_SCENARIOS
from apps.i18n import DEFAULT_LANGUAGE
from apps.reviews.models import TeacherReview
from apps.scoring.models import IndicatorScore, OverallScore
from apps.scoring.calculators import band_for

User = get_user_model()
DEMO_PASSWORD = 'demo1234'

# Roster shown on the review queue / admin screens — ported from the mockup's STUDENTS array.
ROSTER = [
    {'name': 'Amara Osei', 'program': 'CS · Sophomore', 'score': 88, 'status': 'reviewed'},
    {'name': 'Diego Fernandez', 'program': 'CS · Freshman', 'score': 62, 'status': 'pending'},
    {'name': 'Lin Wei Chen', 'program': 'Data Science · Junior', 'score': 94, 'status': 'flagged'},
    {'name': 'Priya Nair', 'program': 'CS · Sophomore', 'score': 71, 'status': 'pending'},
    {'name': 'Jonah Miles', 'program': 'CS · Freshman', 'score': 55, 'status': 'pending'},
    {'name': 'Sofia Marchetti', 'program': 'Software Eng · Senior', 'score': 83, 'status': 'reviewed'},
]

# The 10 indicator keys, matching apps.scoring.constants.INDICATOR_CHOICES —
# used to give the fake roster a score on every indicator.
INDICATOR_KEYS = [
    'math', 'logic', 'algorithmic', 'creative', 'teamwork',
    'patience', 'problem_solving', 'learning_speed', 'attention', 'iq',
]


class Command(BaseCommand):
    help = 'Seed assessment content (questions, coding tasks, learning modules, SJT, anagrams) and demo accounts.'

    @transaction.atomic
    def handle(self, *args, **options):
        self._seed_mcq_questions()
        self._seed_coding_problem()
        self._seed_learning_modules()
        self._seed_sjt_scenarios()
        self._seed_anagrams()
        reviewer = self._seed_demo_accounts()
        self._seed_roster(reviewer)
        self.stdout.write(self.style.SUCCESS('Seed complete.'))
        self.stdout.write('Demo logins (any of these, password "demo1234"):')
        self.stdout.write('  student  jordan.blake@university.edu')
        self.stdout.write('  admin    elena.marsh@university.edu')
        self.stdout.write('  admin    sam.whitfield@university.edu')

    def _seed_mcq_questions(self):
        count = 0
        for indicator_key, questions in MCQ_QUESTIONS.items():
            for q in questions:
                feedback = QUESTION_FEEDBACK.get(q['key'], {})
                CognitiveQuestion.objects.update_or_create(
                    key=q['key'],
                    defaults={
                        'category_ru': q['category_ru'], 'category_uz': q['category_uz'],
                        'indicator_key': indicator_key,
                        'question_type': q.get('question_type', CognitiveQuestion.QuestionType.SINGLE),
                        'prompt_ru': q['prompt_ru'], 'prompt_uz': q['prompt_uz'],
                        'options_ru': q.get('options_ru', []), 'options_uz': q.get('options_uz', []),
                        'correct_indices': q.get('correct_indices', []), 'difficulty': q['difficulty'],
                        'feedback_ru': feedback.get('ru', ''), 'feedback_uz': feedback.get('uz', ''),
                    },
                )
                count += 1
        self.stdout.write(f'  {count} MCQ questions across {len(MCQ_QUESTIONS)} indicators')

    def _seed_coding_problem(self):
        for problem in CODING_PROBLEMS:
            CodingProblem.objects.update_or_create(
                slug=problem['slug'],
                defaults={
                    'title_ru': problem['title_ru'], 'title_uz': problem['title_uz'],
                    'statement_ru': problem['statement_ru'], 'statement_uz': problem['statement_uz'],
                    'example_ru': problem['example_ru'], 'example_uz': problem['example_uz'],
                    'constraints_ru': problem['constraints_ru'], 'constraints_uz': problem['constraints_uz'],
                    'starter_code_ru': problem['starter_code_ru'], 'starter_code_uz': problem['starter_code_uz'],
                    'test_cases': problem['test_cases'], 'is_active': True,
                    'function_name': problem['function_name'],
                    'target_time_seconds': problem['target_time_seconds'],
                    # Editorial tier — defaulted here too so an entry authored before the
                    # field existed still seeds cleanly.
                    'difficulty': problem.get('difficulty', 'medium'),
                },
            )
        self.stdout.write(f'  {len(CODING_PROBLEMS)} coding problems (algorithmic)')

    def _seed_learning_modules(self):
        item_count = 0
        for module in LEARNING_MODULES:
            module_row, _ = LearningModule.objects.update_or_create(
                key=module['key'],
                defaults={
                    'family': module['family'],
                    'title_ru': module['title_ru'], 'title_uz': module['title_uz'],
                    'rules_ru': module['rules_ru'], 'rules_uz': module['rules_uz'],
                    'study_seconds': module.get('study_seconds', 90), 'is_active': True,
                },
            )
            per_block = {}
            for item in module['items']:
                per_block[item['block']] = per_block.get(item['block'], 0) + 1
                order = per_block[item['block']]
                LearningItem.objects.update_or_create(
                    key=f"{module['key']}-b{item['block']}-{order}",
                    defaults={
                        'module': module_row, 'block': item['block'], 'order': order,
                        'prompt_ru': item['prompt_ru'], 'prompt_uz': item['prompt_uz'], 'code': item['code'],
                        'options_ru': item['options_ru'], 'options_uz': item['options_uz'],
                        'correct_index': item['correct_index'],
                        'explanation_ru': item['explanation_ru'], 'explanation_uz': item['explanation_uz'],
                    },
                )
                item_count += 1
        self.stdout.write(f'  {len(LEARNING_MODULES)} learning modules, {item_count} items (learning_speed)')

    def _seed_sjt_scenarios(self):
        for scenario in SJT_SCENARIOS:
            SjtScenario.objects.update_or_create(
                key=scenario['key'],
                defaults={
                    'situation_ru': scenario['situation_ru'], 'situation_uz': scenario['situation_uz'],
                    'options_ru': scenario['options_ru'], 'options_uz': scenario['options_uz'],
                    'ratings': scenario['ratings'], 'is_active': True,
                },
            )
        self.stdout.write(f'  {len(SJT_SCENARIOS)} SJT scenarios (teamwork)')

    def _seed_anagrams(self):
        for item in ANAGRAM_ITEMS:
            AnagramItem.objects.update_or_create(
                key=item['key'],
                defaults={
                    'language': item['language'], 'difficulty': item['difficulty'],
                    'letters': item['letters'], 'answers': item['answers'], 'is_active': True,
                },
            )
        self.stdout.write(f'  {len(ANAGRAM_ITEMS)} anagrams (patience)')

    def _seed_demo_accounts(self):
        student, _ = User.objects.update_or_create(
            email='jordan.blake@university.edu',
            defaults={'first_name': 'Jordan', 'last_name': 'Blake', 'role': User.Role.STUDENT,
                      'program': 'B.S. Computer Science · Sophomore'},
        )
        student.set_password(DEMO_PASSWORD)
        student.save()

        # Pre-completed so the demo login skips the first-login onboarding
        # survey (accounts.permissions.HasCompletedProfile) for smooth manual testing.
        StudentProfile.objects.update_or_create(
            user=student,
            defaults={
                'faculty': 'Faculty of Computer Science',
                'course': '2nd year',
                'group': 'CS-204',
                'specialization': 'Software Engineering',
                'completed_at': timezone.now(),
            },
        )

        # Elena Marsh used to be the demo "teacher" login. The teacher role was
        # removed (a teacher could only ever view their own students' results,
        # nothing else — that's just an admin capability now), so she's an
        # admin account too and keeps reviewing students under that role.
        reviewer, _ = User.objects.update_or_create(
            email='elena.marsh@university.edu',
            defaults={'first_name': 'Elena', 'last_name': 'Marsh', 'role': User.Role.ADMIN},
        )
        reviewer.set_password(DEMO_PASSWORD)
        reviewer.save()

        admin, _ = User.objects.update_or_create(
            email='sam.whitfield@university.edu',
            defaults={'first_name': 'Sam', 'last_name': 'Whitfield', 'role': User.Role.ADMIN},
        )
        admin.set_password(DEMO_PASSWORD)
        admin.save()

        self.stdout.write('  3 demo accounts (student/admin/admin)')
        return reviewer

    def _seed_roster(self, reviewer):
        for row in ROSTER:
            first, _, last = row['name'].partition(' ')
            email = f"{first}.{last}".lower().replace(' ', '') + '@university.edu'
            student, _ = User.objects.update_or_create(
                email=email,
                defaults={'first_name': first, 'last_name': last, 'role': User.Role.STUDENT, 'program': row['program']},
            )
            student.set_unusable_password()
            student.save()

            for key in INDICATOR_KEYS:
                IndicatorScore.objects.update_or_create(
                    student=student, indicator_key=key, defaults={'score': row['score']},
                )
            band = band_for(row['score'], DEFAULT_LANGUAGE)
            OverallScore.objects.update_or_create(
                student=student, defaults={'score': row['score'], 'band': band['key']},
            )

            status = row['status']
            if status == 'reviewed':
                TeacherReview.objects.update_or_create(
                    student=student, defaults={'reviewer': reviewer, 'submitted': True, 'flagged': False},
                )
            elif status == 'flagged':
                TeacherReview.objects.update_or_create(
                    student=student, defaults={'reviewer': reviewer, 'submitted': False, 'flagged': True},
                )
            # 'pending' → no TeacherReview row, matches the model's default 'pending' status.

        self.stdout.write(f'  {len(ROSTER)} roster students (with scores + review status)')
