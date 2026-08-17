from django.conf import settings
from django.db import models

from apps.scoring.constants import INDICATOR_CHOICES


class CognitiveQuestion(models.Model):
    """
    One item in the cognitive test's question bank (COGNITIVE_QUESTIONS in the mockup).
    `difficulty` and `indicator_key` are new — the mockup has neither, since it just
    walks a fixed array — and are what apps.scoring.engine.AdaptiveTestingEngine uses
    to pick the next item and to route a correct/incorrect answer into the right
    IndicatorScore bucket.

    The product ships Russian/Uzbek only (no English) — see apps.i18n — so every
    display field is a _ru/_uz pair rather than one language-neutral column.
    `key` is a stable, language-independent identifier used by the seed command's
    upsert lookup (the old code upserted on `prompt`, which broke once there were
    two different-language prompts for "the same" question).
    """

    class QuestionType(models.TextChoices):
        SINGLE = 'single', 'Single choice'
        MULTI = 'multi', 'Multiple choice'
        ESSAY = 'essay', 'Essay / open-ended'

    key = models.SlugField(max_length=60, unique=True)
    category_ru = models.CharField(max_length=60)  # e.g. "Распознавание образов"
    category_uz = models.CharField(max_length=60)  # e.g. "Naqshlarni aniqlash"
    indicator_key = models.CharField(max_length=20, choices=INDICATOR_CHOICES)
    question_type = models.CharField(max_length=10, choices=QuestionType.choices, default=QuestionType.SINGLE)
    prompt_ru = models.TextField()
    prompt_uz = models.TextField()
    options_ru = models.JSONField(default=list, help_text='Ordered list of answer strings, e.g. ["36","40","42","45"]. Empty for essay questions.')
    options_uz = models.JSONField(default=list, help_text='Same order/length as options_ru — correct_indices applies to both. Empty for essay questions.')
    correct_indices = models.JSONField(
        default=list,
        help_text=(
            '0-based option indices that count as correct. Single choice (incl. step-ordering '
            'questions folded into this type): exactly one element. Multiple choice: 2+ elements, '
            'order-independent (exact-set match). Essay: [] (unused — see apps.scoring.essay_grader).'
        ),
    )
    difficulty = models.FloatField(default=0.0, help_text='2PL difficulty (b), roughly -3..3')
    # 2PL discrimination (a) — how sharply P(correct) rises around theta=difficulty; higher
    # means the item separates low/high-ability students more cleanly. Default 1.0 makes an
    # uncalibrated item behave like a 1PL/Rasch item until apps.scoring.calibration estimates
    # a real value for it from response data — see apps.scoring.irt.probability_2pl.
    discrimination = models.FloatField(default=1.0, help_text='2PL discrimination (a), typically 0.3..2.5; 1.0 = uncalibrated default')
    # Pedagogical advice shown only on the student's Results page for questions they didn't
    # answer fully correctly (never during the live test — see apps.scoring.views' mistakes
    # endpoint). Blank until authored; content lives in apps.assessments.feedback_content.
    feedback_ru = models.TextField(blank=True, default='')
    feedback_uz = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['indicator_key', 'difficulty']

    def __str__(self):
        return f'[{self.key}] {self.prompt_ru[:50]}'


class CodingProblem(models.Model):
    """One task in the coding-phase pool (CODING_PROBLEMS in apps.assessments.content) that
    apps.assessments.views.CodingProblemView draws CODING_TASK_CAP distinct picks from per
    algorithmic attempt."""

    slug = models.SlugField(max_length=60, unique=True)
    title_ru = models.CharField(max_length=120)
    title_uz = models.CharField(max_length=120)
    statement_ru = models.TextField()
    statement_uz = models.TextField()
    example_ru = models.TextField()
    example_uz = models.TextField()
    constraints_ru = models.JSONField(default=list)
    constraints_uz = models.JSONField(default=list)
    starter_code_ru = models.TextField()
    starter_code_uz = models.TextField()
    # The JS function apps.assessments.coding_sandbox calls after eval-ing the
    # student's submitted code — language-neutral like test_cases, since the
    # student is expected to keep this exact name across both _ru/_uz starter codes.
    function_name = models.CharField(max_length=60, default='solution')
    # Scoring baseline for the coding phase's time factor (apps.scoring.state_tracker.
    # _score_hybrid) — solving at or under this earns full time credit; solving slower
    # tapers off. Not a hard deadline, unlike the MCQ phase's time_remaining_seconds.
    target_time_seconds = models.PositiveIntegerField(default=300)
    # Test data itself (input words, expected output) is language-neutral puzzle
    # content, not UI prose, so it stays a single shared field.
    test_cases = models.JSONField(
        default=list,
        help_text=(
            'List of {"input": ..., "expected": ..., "hidden": bool, "label": str}. '
            'hidden=False cases power "Run tests"; the full list powers "Submit solution".'
        ),
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title_ru


class BehavioralCategory(models.Model):
    """One of BEHAVIORAL_GROUPS' categories, e.g. PERSISTENCE, COLLABORATION."""

    key = models.CharField(max_length=30, unique=True)
    label_ru = models.CharField(max_length=60)
    label_uz = models.CharField(max_length=60)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'behavioral categories'

    def __str__(self):
        return self.label_ru


class BehavioralItem(models.Model):
    """One Likert statement within a BehavioralCategory."""

    key = models.SlugField(max_length=60, unique=True)
    category = models.ForeignKey(BehavioralCategory, related_name='items', on_delete=models.CASCADE)
    text_ru = models.TextField()
    text_uz = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    # The mockup pairs a positively- and negatively-framed statement per category
    # (e.g. "I keep working..." vs "I feel discouraged..."). This flag lets the
    # scoring engine invert the 1-5 scale before averaging into the indicator.
    reverse_scored = models.BooleanField(default=False)

    class Meta:
        ordering = ['category__order', 'order']

    def __str__(self):
        return self.text_ru[:50]


class AssessmentAttempt(models.Model):
    """
    One student's attempt at one of the ten indicator-specific assessment
    cards. Existence + `status` is what powers the `assessments` cards' status
    badge/CTA ("Available"/"Completed", "Start assessment"/"Retake") and the
    `completed{}` flags gating "View my results" — see apps.scoring.state_tracker.

    Each type maps 1:1 to an indicator key (apps.scoring.constants.INDICATOR_CHOICES)
    and to one of three reusable UI/scoring patterns — MCQ_TYPES (timed,
    difficulty-matched question bank), LIKERT_TYPES (self-report statements), and
    the MCQ pattern followed by a coding run/submit phase for HYBRID_TYPES (a
    subset of MCQ_TYPES — see below). Views/state_tracker dispatch on these sets
    rather than hardcoding all ten types individually.
    """

    class Type(models.TextChoices):
        MATH = 'math', 'Math'
        LOGIC = 'logic', 'Logic'
        ALGORITHMIC = 'algorithmic', 'Algorithmic'
        CREATIVE = 'creative', 'Creative'
        TEAMWORK = 'teamwork', 'Teamwork'
        PATIENCE = 'patience', 'Patience'
        PROBLEM_SOLVING = 'problem_solving', 'Problem solving'
        LEARNING_SPEED = 'learning_speed', 'Learning speed'
        ATTENTION = 'attention', 'Attention'
        IQ = 'iq', 'IQ'

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not started'
        IN_PROGRESS = 'in_progress', 'In progress'
        COMPLETED = 'completed', 'Completed'

    MCQ_TYPES = frozenset({
        Type.MATH, Type.LOGIC, Type.ALGORITHMIC, Type.CREATIVE, Type.PROBLEM_SOLVING, Type.ATTENTION, Type.IQ,
    })
    LIKERT_TYPES = frozenset({Type.TEAMWORK, Type.PATIENCE, Type.LEARNING_SPEED})
    # Subset of MCQ_TYPES whose MCQ phase doesn't finalize the attempt on its own —
    # SubmitMcqView instead calls StudentStateTracker.finish_mcq_phase and hands off
    # to the coding pattern (CodingProblem/CodingSubmission, Start/Run/SubmitCodingView)
    # for a second phase, with state_tracker._score_hybrid blending both phases' results
    # into the one indicator score. algorithmic is the only member: MCQ questions alone
    # can't show whether a student can actually produce working code, so this indicator
    # also runs a real coding task before it's scored.
    HYBRID_TYPES = frozenset({Type.ALGORITHMIC})

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attempts', on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NOT_STARTED)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    # MCQ types only — the authoritative source for {{ timerLabel }}/{{ timerColor }};
    # the client just ticks a local copy between answer round-trips.
    time_remaining_seconds = models.PositiveIntegerField(null=True, blank=True)
    # HYBRID_TYPES only. mcq_phase_score is the 0-100 result of the MCQ phase alone,
    # stashed by StudentStateTracker.finish_mcq_phase when that phase ends so
    # _score_hybrid can blend it with the coding phase's result once that finishes
    # too — the attempt isn't COMPLETED yet at that point, so it can't go in
    # IndicatorScore. coding_started_at marks when the coding phase began (set by
    # StartCodingView), the baseline _score_hybrid measures elapsed solve time from.
    mcq_phase_score = models.FloatField(null=True, blank=True)
    coding_started_at = models.DateTimeField(null=True, blank=True)
    # Bumped (never reset) each time a COMPLETED attempt is retaken — see
    # StudentStateTracker.start_or_restart_attempt. Responses are no longer deleted on
    # retake (they're tagged with the cycle they were answered in instead), so selection
    # logic (AdaptiveTestingEngine.select_next_question, CodingProblemView) can tell
    # "answered already this run" (cycle == attempt_cycle) apart from "seen in a past
    # attempt" (any earlier cycle) and avoid re-serving the latter while pool allows.
    attempt_cycle = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'assessment_type'], name='one_attempt_per_type'),
        ]

    def __str__(self):
        return f'{self.student} · {self.assessment_type} · {self.status}'


class CognitiveResponse(models.Model):
    attempt = models.ForeignKey(AssessmentAttempt, related_name='cognitive_responses', on_delete=models.CASCADE)
    question = models.ForeignKey(CognitiveQuestion, on_delete=models.PROTECT)
    selected_indices = models.JSONField(
        default=list, blank=True,
        help_text='0-based option indices the student picked. Single: 1 element. Multi: N elements. Essay: [] (unused).',
    )
    essay_text = models.TextField(blank=True, default='')
    rubric_scores = models.JSONField(
        default=dict, blank=True,
        help_text=(
            '{"position": 2, "argument_quality": 3, "counter_argument": 1, "conclusion": 2} — keys '
            'mirror apps.reviews.models.RUBRIC_ITEMS\' stable-key convention. {} for single/multi rows.'
        ),
    )
    correctness = models.FloatField(
        default=0.0,
        help_text=(
            '0.0-1.0 fractional correctness this response contributes to the indicator average. '
            'Single/multi: 1.0 or 0.0 (exact match). Essay: rubric_scores total / 10.'
        ),
    )
    response_time_ms = models.PositiveIntegerField(
        null=True, blank=True,
        help_text=(
            'Client-measured time from question display to submission. Null when the client '
            "didn't report it (older clients). Feeds AdaptiveTestingEngine's speed-aware "
            'ability update — see StudentAbilityEstimate.avg_response_ms.'
        ),
    )
    responded_at = models.DateTimeField(auto_now_add=True)
    # Snapshot of attempt.attempt_cycle at answer time — not just a FK-follow, since the
    # attempt's cycle keeps advancing on later retakes while this row must stay pinned to
    # the run it was actually answered in. See AssessmentAttempt.attempt_cycle.
    cycle = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['attempt', 'question', 'cycle'], name='one_response_per_question_per_cycle'),
        ]


class CodingSubmission(models.Model):
    """
    A code snapshot. `is_final=False` rows come from "Run tests" (sample cases only,
    powers {{ testResults }}); the `is_final=True` row comes from "Submit solution"
    (full hidden suite, feeds the `fluency` IndicatorScore).
    """

    attempt = models.ForeignKey(AssessmentAttempt, related_name='coding_submissions', on_delete=models.CASCADE)
    problem = models.ForeignKey(CodingProblem, on_delete=models.PROTECT)
    code = models.TextField()
    is_final = models.BooleanField(default=False)
    test_results = models.JSONField(default=list)
    passed_count = models.PositiveSmallIntegerField(default=0)
    total_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    # Client-measured time spent on this problem (shown → submitted), mirroring
    # CognitiveResponse.response_time_ms — needed because the coding phase now runs
    # CODING_TASK_CAP distinct problems per attempt, so a single phase-wide
    # coding_started_at can no longer serve as every problem's own time baseline.
    elapsed_ms = models.PositiveIntegerField(null=True, blank=True)
    # See CognitiveResponse.cycle.
    cycle = models.PositiveIntegerField(default=1)


class BehavioralResponse(models.Model):
    attempt = models.ForeignKey(AssessmentAttempt, related_name='behavioral_responses', on_delete=models.CASCADE)
    item = models.ForeignKey(BehavioralItem, on_delete=models.PROTECT)
    scale_value = models.PositiveSmallIntegerField(help_text='1 (Strongly Disagree) .. 5 (Strongly Agree)')
    responded_at = models.DateTimeField(auto_now_add=True)
    # See CognitiveResponse.cycle.
    cycle = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['attempt', 'item', 'cycle'], name='one_response_per_item_per_cycle'),
        ]
