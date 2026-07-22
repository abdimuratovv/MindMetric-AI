from django.conf import settings
from django.db import models

# Ported from RUBRIC_LABELS in the mockup (line 679), translated ru/uz. `key` is
# the stable, language-independent identifier stored in `rubric_scores` — display
# text can't be the storage key once it varies by request language (see
# apps.reviews.views.TeacherStudentDetailView / SubmitReviewView).
RUBRIC_ITEMS = [
    {'key': 'code_readability', 'ru': 'Читаемость кода', 'uz': "Kod o'qilishi"},
    {'key': 'debugging_approach', 'ru': 'Подход к отладке', 'uz': 'Debagging yondashuvi'},
    {'key': 'collaboration_observed', 'ru': 'Наблюдаемое сотрудничество', 'uz': 'Kuzatilgan hamkorlik'},
    {'key': 'conceptual_understanding', 'ru': 'Понимание концепций', 'uz': 'Tushunchalarni anglash'},
]


class TeacherReview(models.Model):
    """
    One faculty review of one student — backs the teacherReview screen's
    right-hand panel (rubric + comment + submit) and the {{ s.statusLabel }}
    badge in both the teacher queue and the admin student table.
    """

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_received', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_given', on_delete=models.SET_NULL, null=True)

    rubric_scores = models.JSONField(default=dict, help_text='{"code_readability": 4, ...} — keys from RUBRIC_ITEMS')
    comment = models.TextField(blank=True)

    submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    # A teacher can flag a case for closer institutional attention independent
    # of whether their own review is finished — mirrors STUDENTS' 'flagged' status.
    flagged = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student'], name='one_review_per_student'),
        ]

    @property
    def status(self) -> str:
        if self.flagged:
            return 'flagged'
        if self.submitted:
            return 'reviewed'
        return 'pending'
