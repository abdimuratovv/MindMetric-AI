from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class DevelopmentModule(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        RETIRED = 'retired', 'Retired'

    key = models.SlugField(max_length=64)
    version = models.PositiveIntegerField()
    cluster = models.PositiveSmallIntegerField(choices=[(1, 'Academic'), (2, 'Algorithmic/practical'), (3, 'Personal/team skills')], default=1)
    order = models.PositiveSmallIntegerField(default=0)
    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True, default='')
    content_language = models.CharField(max_length=2, default='uz')
    indicator_keys = models.JSONField(default=list)
    review_status = models.CharField(max_length=40, default='internally_checked')
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    content_hash = models.CharField(max_length=64)
    content_snapshot = models.JSONField(default=dict)
    blueprint = models.JSONField(default=dict)
    published_at = models.DateTimeField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['cluster', 'order', 'key', '-version']
        constraints = [
            models.UniqueConstraint(fields=['key', 'version'], name='dev_module_version_unique'),
            models.CheckConstraint(check=models.Q(version__gte=1), name='dev_module_positive_version'),
            models.CheckConstraint(check=models.Q(cluster__in=[1, 2, 3]), name='dev_module_valid_cluster'),
        ]

    def __str__(self):
        return f'{self.key} v{self.version}'

    @property
    def is_frozen(self):
        return bool(self.published_at or self.status != self.Status.DRAFT
                    or (self.pk and self.enrollments.exists()))

    def save(self, *args, **kwargs):
        previous = type(self).objects.filter(pk=self.pk).first() if self.pk else None
        if previous and previous.is_frozen:
            # Lifecycle transitions do not reopen content for editing.
            mutable = {'status'}
            for field in self._meta.concrete_fields:
                if field.name not in mutable and getattr(previous, field.attname) != getattr(self, field.attname):
                    raise ValidationError('Published or enrolled content requires a new version.')
            if self.status == self.Status.DRAFT:
                raise ValidationError('Frozen content cannot return to draft.')
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_frozen:
            raise ValidationError('Frozen content cannot be deleted.')
        return super().delete(*args, **kwargs)


class FrozenContent(models.Model):
    """Guard regular model edits; bulk writes are restricted to the importer."""

    class Meta:
        abstract = True

    def content_module(self):
        return self.module

    def save(self, *args, **kwargs):
        module = DevelopmentModule.objects.get(pk=self.content_module().pk)
        if module.is_frozen:
            raise ValidationError('Published or enrolled content requires a new version.')
        if self.pk:
            previous = type(self).objects.get(pk=self.pk)
            if previous.content_module().is_frozen:
                raise ValidationError('Frozen content cannot be moved to another module.')
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.content_module().is_frozen:
            raise ValidationError('Frozen content cannot be deleted.')
        return super().delete(*args, **kwargs)


class DevelopmentSkill(FrozenContent):
    module = models.ForeignKey(DevelopmentModule, related_name='skills', on_delete=models.CASCADE)
    key = models.SlugField(max_length=64)
    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True, default='')
    indicator_keys = models.JSONField(default=list)
    prerequisites = models.ManyToManyField('self', symmetrical=False, related_name='dependents', blank=True)

    class Meta:
        ordering = ['module', 'key']
        constraints = [models.UniqueConstraint(fields=['module', 'key'], name='dev_skill_key_unique')]

    def __str__(self):
        return self.key


class DevelopmentLesson(FrozenContent):
    module = models.ForeignKey(DevelopmentModule, related_name='lessons', on_delete=models.CASCADE)
    skill = models.ForeignKey(DevelopmentSkill, related_name='lessons', on_delete=models.PROTECT)
    key = models.SlugField(max_length=64)
    order = models.PositiveSmallIntegerField(default=0)
    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True, default='')
    theory_uz = models.JSONField(default=list)
    theory_ru = models.JSONField(default=list, blank=True)
    worked_example_uz = models.JSONField(default=dict)
    worked_example_ru = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['module', 'order']
        constraints = [models.UniqueConstraint(fields=['module', 'key'], name='dev_lesson_key_unique')]

    def clean(self):
        if self.skill_id and self.module_id != self.skill.module_id:
            raise ValidationError({'skill': 'Skill must belong to this module version.'})


class DevelopmentExercise(FrozenContent):
    class Purpose(models.TextChoices):
        PRACTICE = 'practice', 'Practice'
        PRECHECK = 'precheck', 'Precheck'
        POSTCHECK = 'postcheck', 'Postcheck'

    class Format(models.TextChoices):
        NUMERIC = 'numeric', 'Numeric'
        SINGLE = 'single', 'Single choice'
        MULTI = 'multi', 'Multiple choice'

    module = models.ForeignKey(DevelopmentModule, related_name='exercises', on_delete=models.CASCADE)
    skill = models.ForeignKey(DevelopmentSkill, related_name='exercises', on_delete=models.PROTECT)
    key = models.SlugField(max_length=64)
    purpose = models.CharField(max_length=12, choices=Purpose.choices)
    format = models.CharField(max_length=10, choices=Format.choices)
    difficulty = models.CharField(max_length=8, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    prompt_uz = models.TextField()
    prompt_ru = models.TextField(blank=True, default='')
    options = models.JSONField(default=list, blank=True)
    answer_key = models.JSONField(default=dict)
    solution_steps_uz = models.JSONField(default=list)
    solution_steps_ru = models.JSONField(default=list, blank=True)
    hint_uz = models.TextField(null=True, blank=True)
    hint_ru = models.TextField(null=True, blank=True)
    common_error_uz = models.TextField()
    common_error_ru = models.TextField(blank=True, default='')
    source = models.JSONField(default=dict)

    class Meta:
        ordering = ['module', 'key']
        constraints = [models.UniqueConstraint(fields=['module', 'key'], name='dev_exercise_key_unique')]

    def clean(self):
        if self.skill_id and self.module_id != self.skill.module_id:
            raise ValidationError({'skill': 'Skill must belong to this module version.'})
        if self.purpose != self.Purpose.PRACTICE and (self.hint_uz or self.hint_ru):
            raise ValidationError('Checks cannot contain hints.')


class DiagnosticSkillLink(FrozenContent):
    question = models.ForeignKey('assessments.CognitiveQuestion', related_name='development_links', on_delete=models.PROTECT)
    skill = models.ForeignKey(DevelopmentSkill, related_name='diagnostic_links', on_delete=models.CASCADE)
    rationale_uz = models.TextField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['question', 'skill'], name='dev_diagnostic_skill_unique')]

    def content_module(self):
        return self.skill.module


class DevelopmentEnrollment(models.Model):
    class Stage(models.TextChoices):
        PRECHECK = 'precheck', 'Precheck'
        STUDY = 'study', 'Study'
        PRACTICE = 'practice', 'Practice'
        POSTCHECK = 'postcheck', 'Postcheck'
        COMPLETED = 'completed', 'Completed'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='development_enrollments', on_delete=models.CASCADE)
    module = models.ForeignKey(DevelopmentModule, related_name='enrollments', on_delete=models.PROTECT)
    stage = models.CharField(max_length=12, choices=Stage.choices, default=Stage.PRECHECK)
    diagnostic_snapshot = models.JSONField(default=dict, blank=True)
    recommendation_reason = models.JSONField(default=dict, blank=True)
    completed_lesson_keys = models.JSONField(default=list, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['student', 'module'], name='dev_enrollment_unique')]

    def clean(self):
        if self.student_id and self.student.role != 'student':
            raise ValidationError({'student': 'Only students can enroll.'})
        if not self.pk and self.module_id and self.module.status != DevelopmentModule.Status.PUBLISHED:
            raise ValidationError({'module': 'Only published modules accept new enrollments.'})

    def save(self, *args, **kwargs):
        self.clean()
        if self.pk:
            previous = type(self).objects.get(pk=self.pk)
            if any(getattr(previous, field) != getattr(self, field) for field in (
                'student_id', 'module_id', 'diagnostic_snapshot', 'recommendation_reason',
            )):
                raise ValidationError('An enrollment is pinned to its student, version and baseline snapshot.')
        super().save(*args, **kwargs)


class DevelopmentSession(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In progress'
        COMPLETED = 'completed', 'Completed'

    enrollment = models.ForeignKey(DevelopmentEnrollment, related_name='sessions', on_delete=models.CASCADE)
    purpose = models.CharField(max_length=12, choices=DevelopmentExercise.Purpose.choices)
    number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.IN_PROGRESS)
    question_snapshot = models.JSONField(default=list)
    hint_usage = models.JSONField(default=dict, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            previous = type(self).objects.get(pk=self.pk)
            if any(getattr(previous, field) != getattr(self, field) for field in (
                'enrollment_id', 'purpose', 'number', 'question_snapshot',
            )):
                raise ValidationError('A session is pinned to its enrollment and question snapshot.')
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['enrollment', 'purpose', 'number'], name='dev_session_number_unique'),
            models.UniqueConstraint(fields=['enrollment'], condition=models.Q(status='in_progress'), name='dev_one_active_session'),
            models.CheckConstraint(check=models.Q(number__gte=1), name='dev_session_positive_number'),
            models.CheckConstraint(check=models.Q(score__isnull=True) | models.Q(score__gte=0, score__lte=100), name='dev_session_score_range'),
        ]


class DevelopmentAnswer(models.Model):
    session = models.ForeignKey(DevelopmentSession, related_name='answers', on_delete=models.CASCADE)
    exercise = models.ForeignKey(DevelopmentExercise, related_name='answers', on_delete=models.PROTECT)
    idempotency_key = models.UUIDField()
    attempt_number = models.PositiveIntegerField(default=1)
    response = models.JSONField()
    correctness = models.FloatField()
    hint_used = models.BooleanField(default=False)
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    answered_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_first_attempt(self):
        return self.attempt_number == 1

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'idempotency_key'], name='dev_answer_idempotency_unique'),
            models.UniqueConstraint(fields=['session', 'exercise', 'attempt_number'], name='dev_answer_attempt_unique'),
            models.CheckConstraint(check=models.Q(attempt_number__gte=1), name='dev_answer_positive_attempt'),
            models.CheckConstraint(check=models.Q(correctness__gte=0, correctness__lte=1), name='dev_answer_correctness_range'),
        ]

    def clean(self):
        if self.session_id and self.exercise_id:
            if self.exercise.module_id != self.session.enrollment.module_id:
                raise ValidationError({'exercise': 'Exercise must belong to the enrolled module version.'})
            if self.exercise.purpose != self.session.purpose:
                raise ValidationError({'exercise': 'Exercise purpose must match the session.'})

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError('Answers are append-only; retries must create a new attempt.')
        self.clean()
        super().save(*args, **kwargs)
