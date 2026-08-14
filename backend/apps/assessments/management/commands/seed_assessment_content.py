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
from apps.assessments.content import CODING_PROBLEM, LIKERT_CATEGORIES, MCQ_QUESTIONS
from apps.assessments.feedback_content import QUESTION_FEEDBACK
from apps.assessments.models import BehavioralCategory, BehavioralItem, CodingProblem, CognitiveQuestion
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
    help = 'Seed assessment content (questions/problem/likert items) and demo accounts.'

    @transaction.atomic
    def handle(self, *args, **options):
        self._seed_mcq_questions()
        self._seed_coding_problem()
        self._seed_likert_categories()
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
        CodingProblem.objects.update_or_create(
            slug=CODING_PROBLEM['slug'],
            defaults={
                'title_ru': CODING_PROBLEM['title_ru'], 'title_uz': CODING_PROBLEM['title_uz'],
                'statement_ru': CODING_PROBLEM['statement_ru'], 'statement_uz': CODING_PROBLEM['statement_uz'],
                'example_ru': CODING_PROBLEM['example_ru'], 'example_uz': CODING_PROBLEM['example_uz'],
                'constraints_ru': CODING_PROBLEM['constraints_ru'], 'constraints_uz': CODING_PROBLEM['constraints_uz'],
                'starter_code_ru': CODING_PROBLEM['starter_code_ru'], 'starter_code_uz': CODING_PROBLEM['starter_code_uz'],
                'test_cases': CODING_PROBLEM['test_cases'], 'is_active': True,
                'function_name': CODING_PROBLEM['function_name'],
                'target_time_seconds': CODING_PROBLEM['target_time_seconds'],
            },
        )
        self.stdout.write('  1 coding problem (algorithmic)')

    def _seed_likert_categories(self):
        item_count = 0
        for order, (indicator_key, category) in enumerate(LIKERT_CATEGORIES.items()):
            category_row, _ = BehavioralCategory.objects.update_or_create(
                key=indicator_key.upper(),
                defaults={'label_ru': category['label_ru'], 'label_uz': category['label_uz'], 'order': order},
            )
            for item_order, item in enumerate(category['items']):
                BehavioralItem.objects.update_or_create(
                    key=item['key'],
                    defaults={
                        'category': category_row, 'text_ru': item['text_ru'], 'text_uz': item['text_uz'],
                        'order': item_order, 'reverse_scored': item['reverse_scored'],
                    },
                )
                item_count += 1
        self.stdout.write(f'  {len(LIKERT_CATEGORIES)} likert categories, {item_count} items')

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
