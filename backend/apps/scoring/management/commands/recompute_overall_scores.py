"""
Recomputes OverallScore (and the field recommendation alongside it) for every
student with at least one IndicatorScore, using the current calculators.py
logic. Needed one-off after a formula change — e.g. compute_overall_score
now scales by completed/total indicators instead of averaging only what's
done, so already-stored scores from before that change are stale until the
student's next answer triggers a live recompute.

Usage:
    python manage.py recompute_overall_scores
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.scoring.models import IndicatorScore
from apps.scoring.state_tracker import StudentStateTracker

User = get_user_model()


class Command(BaseCommand):
    help = "Recompute OverallScore/FieldRecommendation for every student with IndicatorScore rows."

    def handle(self, *args, **options):
        student_ids = IndicatorScore.objects.values_list('student_id', flat=True).distinct()
        tracker = StudentStateTracker()
        count = 0
        for student in User.objects.filter(id__in=student_ids):
            tracker._recompute_overall_score(student)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Recomputed overall score for {count} student(s).'))
