from django.conf import settings
from django.db import models

from .constants import INDICATOR_CHOICES


class StudentAbilityEstimate(models.Model):
    """
    Per-student, per-indicator ability estimate (theta) used only by the
    cognitive indicators (logic/pattern/decomp). Has no mockup equivalent —
    the mockup has no adaptivity — it's what AdaptiveTestingEngine reads/writes
    on every answered question. See ARCHITECTURE.md §4.
    """

    class EstimationMethod(models.TextChoices):
        PRIOR = 'prior', 'Prior mean (no responses yet)'
        EAP = 'eap', 'Expected a Posteriori'
        MLE = 'mle', 'Maximum Likelihood (Newton-Raphson)'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ability_estimates', on_delete=models.CASCADE)
    indicator_key = models.CharField(max_length=20, choices=INDICATOR_CHOICES)
    theta = models.FloatField(default=0.0)
    # Asymptotic standard error of theta — 1/sqrt(test information) for MLE, posterior SD for
    # EAP (see apps.scoring.irt). Null until at least one response has been scored, since SE is
    # undefined with zero test information.
    se = models.FloatField(null=True, blank=True)
    # Which estimator produced the current `theta`/`se` — see apps.scoring.irt.estimate_theta.
    # MLE is preferred (asymptotically unbiased) but is undefined for all-correct/all-incorrect
    # response patterns, where the engine falls back to EAP (always finite, prior-regularized).
    estimation_method = models.CharField(max_length=10, choices=EstimationMethod.choices, default=EstimationMethod.PRIOR)
    # Running average (EMA) of this student's own response_time_ms on this indicator, used as
    # their personal baseline for "fast"/"slow" rather than a fixed global threshold — see
    # AdaptiveTestingEngine._response_weight. Null until their first timed answer.
    avg_response_ms = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'indicator_key'], name='one_estimate_per_student_indicator'),
        ]


class IndicatorScore(models.Model):
    """
    One of the 10 axes shown on the results radar / breakdown / analytics
    screens ({{ indicators }}, {{ indicatorsDetail }}). Written once per
    indicator when the assessment that feeds it completes — cognitive (MCQ)
    indicators from their question bank, algorithmic additionally blends in a
    coding-task phase (see apps.scoring.state_tracker._score_hybrid), behavioral
    indicators from Likert self-report.
    """

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='indicator_scores', on_delete=models.CASCADE)
    indicator_key = models.CharField(max_length=20, choices=INDICATOR_CHOICES)
    score = models.PositiveSmallIntegerField(help_text='0-100, same scale as the mockup\'s indicatorsBase.score')
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'indicator_key'], name='one_score_per_student_indicator'),
        ]


class OverallScore(models.Model):
    """
    The headline {{ overallScore }}/{{ band }} on the results screen — the mean
    of the student's IndicatorScore rows, recomputed (via calculators.py)
    whenever an assessment completes.
    """

    student = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='overall_score', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    band = models.CharField(max_length=40)
    # Narrower sibling of `score`: weighted toward the indicators that measure
    # programming ability itself (see constants.PROGRAMMING_APTITUDE_WEIGHTS),
    # rather than `score`'s plain mean across all 10 (which weighs soft-skill
    # indicators like teamwork equally). Null until at least one weighted
    # indicator has been completed.
    programming_aptitude_score = models.PositiveSmallIntegerField(null=True, blank=True)
    computed_at = models.DateTimeField(auto_now=True)


class FieldRecommendation(models.Model):
    """
    Which of the 6 specialization tracks (constants.FIELD_CHOICES) a student's
    indicator profile best fits, recomputed alongside OverallScore whenever an
    assessment completes (see state_tracker.py). `top_field_key` is stored as
    its own column (rather than only inside `fit_scores`) so cohort dashboards
    can group by it cheaply — see apps.analytics.views.FieldDistributionView —
    without deserializing every student's JSON blob.
    """

    student = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='field_recommendation', on_delete=models.CASCADE)
    top_field_key = models.CharField(max_length=20, blank=True)
    fit_scores = models.JSONField(default=dict, help_text='{field_key: 0-100 fit score}, only fields that cleared the coverage gate')
    completed_indicator_count = models.PositiveSmallIntegerField(default=0)
    is_confident = models.BooleanField(default=False, help_text='True once completed_indicator_count >= calculators.MIN_COMPLETED_INDICATORS')
    computed_at = models.DateTimeField(auto_now=True)


class Achievement(models.Model):
    """
    A gamification badge earned by crossing a scoring tier (see
    apps.scoring.achievements.tier_for_score) on one indicator. Shown as the
    student's permanent "collection" on the achievements/profile screen.

    One row per (student, indicator): retaking a test and scoring higher
    upgrades the tier in place rather than stacking duplicate badges, so the
    collection always reflects the student's *best* result per indicator and
    a bad retake never takes a badge away.
    """

    class Tier(models.TextChoices):
        BRONZE = 'bronze', 'Bronze'
        SILVER = 'silver', 'Silver'
        GOLD = 'gold', 'Gold'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='achievements', on_delete=models.CASCADE)
    indicator_key = models.CharField(max_length=20, choices=INDICATOR_CHOICES)
    tier = models.CharField(max_length=10, choices=Tier.choices)
    score = models.PositiveSmallIntegerField(help_text='Indicator score at the time this tier was earned')
    first_earned_at = models.DateTimeField(auto_now_add=True)
    tier_earned_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'indicator_key'], name='one_achievement_per_student_indicator'),
        ]
