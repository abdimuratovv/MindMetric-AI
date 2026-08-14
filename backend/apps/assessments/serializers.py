import uuid

from rest_framework import serializers

from .models import (
    AssessmentAttempt,
    BehavioralCategory,
    BehavioralItem,
    CodingProblem,
    CognitiveQuestion,
)

# indicator keys the admin question-bank create form is allowed to attach a new
# CognitiveQuestion to — mirrors apps.analytics.views.MCQ_INDICATOR_KEYS.
MCQ_INDICATOR_KEYS = {t.value for t in AssessmentAttempt.MCQ_TYPES}


def _new_content_key(prefix):
    """Stable, collision-free `key` for an admin-created question/item — seed
    content uses hand-picked keys like 'math-easy-1', so admin-created rows
    are tagged distinctly to avoid ever colliding with a future seed run."""
    return f'{prefix}-admin-{uuid.uuid4().hex[:10]}'


class AttemptStatusSerializer(serializers.ModelSerializer):
    """One row of {{ assessments }} on the selection screen."""

    class Meta:
        model = AssessmentAttempt
        fields = ['assessment_type', 'status', 'time_remaining_seconds']


class CognitiveQuestionSerializer(serializers.ModelSerializer):
    """
    {{ cqCategory }} / {{ cqPrompt }} / {{ cqOptions }} — correct_index withheld.

    Picks the _ru/_uz field for `self.context['lang']` (set by the view from
    apps.i18n.get_language) and exposes it under the original language-neutral
    field name, so the frontend contract (and every ported {{ }} binding) is
    unchanged — only the *value* varies per request.
    """

    category = serializers.SerializerMethodField()
    prompt = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()

    class Meta:
        model = CognitiveQuestion
        fields = ['id', 'question_type', 'category', 'prompt', 'options']

    def get_category(self, obj):
        return getattr(obj, f'category_{self.context["lang"]}')

    def get_prompt(self, obj):
        return getattr(obj, f'prompt_{self.context["lang"]}')

    def get_options(self, obj):
        return getattr(obj, f'options_{self.context["lang"]}')


class _McqInvariantsMixin:
    """Shared by the admin MCQ update/create serializers: options_ru/options_uz
    must line up 1:1, correct_indices must point at real options, and a
    single-choice question needs exactly one correct index. Essay questions
    carry no options, so they're exempt."""

    def _check_mcq_invariants(self, question_type, options_ru, options_uz, correct_indices):
        if question_type == CognitiveQuestion.QuestionType.ESSAY:
            return
        if len(options_ru) != len(options_uz):
            raise serializers.ValidationError('options_ru and options_uz must have the same length.')
        if not options_ru:
            raise serializers.ValidationError('At least one answer option is required.')
        if any(i < 0 or i >= len(options_ru) for i in correct_indices):
            raise serializers.ValidationError('correct_indices must reference valid option positions.')
        if question_type == CognitiveQuestion.QuestionType.SINGLE and len(correct_indices) != 1:
            raise serializers.ValidationError('A single-choice question needs exactly one correct index.')


class AdminCognitiveQuestionUpdateSerializer(_McqInvariantsMixin, serializers.ModelSerializer):
    """
    PATCH body for apps.analytics.views.QuestionBankMcqDetailView — the admin
    "Savollar banki" screen's edit form. Unlike CognitiveQuestionSerializer
    above, this is never used to serve students: it both accepts and returns
    correct_indices.
    """

    class Meta:
        model = CognitiveQuestion
        fields = [
            'category_ru', 'category_uz', 'question_type', 'prompt_ru', 'prompt_uz',
            'options_ru', 'options_uz', 'correct_indices', 'difficulty',
        ]

    def validate(self, attrs):
        instance = self.instance
        self._check_mcq_invariants(
            attrs.get('question_type', instance.question_type),
            attrs.get('options_ru', instance.options_ru),
            attrs.get('options_uz', instance.options_uz),
            attrs.get('correct_indices', instance.correct_indices),
        )
        return attrs


class AdminCognitiveQuestionCreateSerializer(_McqInvariantsMixin, serializers.ModelSerializer):
    """POST body for apps.analytics.views.QuestionBankMcqListView — creates a new
    CognitiveQuestion under an existing MCQ indicator. `key` is auto-generated
    (the admin never sees or picks it; only seed content uses hand-picked keys)."""

    indicator_key = serializers.CharField()

    class Meta:
        model = CognitiveQuestion
        fields = [
            'indicator_key', 'category_ru', 'category_uz', 'question_type', 'prompt_ru', 'prompt_uz',
            'options_ru', 'options_uz', 'correct_indices', 'difficulty',
        ]

    def validate_indicator_key(self, value):
        if value not in MCQ_INDICATOR_KEYS:
            raise serializers.ValidationError('Not an MCQ indicator.')
        return value

    def validate(self, attrs):
        self._check_mcq_invariants(
            attrs.get('question_type', CognitiveQuestion.QuestionType.SINGLE),
            attrs.get('options_ru', []), attrs.get('options_uz', []), attrs.get('correct_indices', []),
        )
        return attrs

    def create(self, validated_data):
        validated_data['key'] = _new_content_key(validated_data['indicator_key'])
        return CognitiveQuestion.objects.create(**validated_data)


class AdminBehavioralItemUpdateSerializer(serializers.ModelSerializer):
    """PATCH body for apps.analytics.views.QuestionBankLikertDetailView."""

    class Meta:
        model = BehavioralItem
        fields = ['text_ru', 'text_uz', 'reverse_scored']


class AdminBehavioralItemCreateSerializer(serializers.ModelSerializer):
    """POST body for apps.analytics.views.QuestionBankLikertListView — creates a
    new BehavioralItem under an existing Likert indicator's category, appended
    after the category's current last item."""

    indicator_key = serializers.CharField(write_only=True)

    class Meta:
        model = BehavioralItem
        fields = ['indicator_key', 'text_ru', 'text_uz', 'reverse_scored']

    def validate_indicator_key(self, value):
        if not BehavioralCategory.objects.filter(key=value.upper()).exists():
            raise serializers.ValidationError('Unknown Likert indicator.')
        return value

    def create(self, validated_data):
        indicator_key = validated_data.pop('indicator_key')
        category = BehavioralCategory.objects.get(key=indicator_key.upper())
        last_order = max((o for o in category.items.values_list('order', flat=True)), default=0)
        return BehavioralItem.objects.create(
            category=category, key=_new_content_key(indicator_key), order=last_order + 1, **validated_data,
        )


class CodingProblemSerializer(serializers.ModelSerializer):
    """{{ codingProblem.* }} — hidden test cases withheld."""

    title = serializers.SerializerMethodField()
    statement = serializers.SerializerMethodField()
    example = serializers.SerializerMethodField()
    constraints = serializers.SerializerMethodField()
    starter_code = serializers.SerializerMethodField()

    class Meta:
        model = CodingProblem
        fields = ['id', 'title', 'statement', 'example', 'constraints', 'starter_code', 'target_time_seconds']

    def get_title(self, obj):
        return getattr(obj, f'title_{self.context["lang"]}')

    def get_statement(self, obj):
        return getattr(obj, f'statement_{self.context["lang"]}')

    def get_example(self, obj):
        return getattr(obj, f'example_{self.context["lang"]}')

    def get_constraints(self, obj):
        return getattr(obj, f'constraints_{self.context["lang"]}')

    def get_starter_code(self, obj):
        return getattr(obj, f'starter_code_{self.context["lang"]}')


class BehavioralItemSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = BehavioralItem
        fields = ['id', 'text', 'order', 'reverse_scored']

    def get_text(self, obj):
        return getattr(obj, f'text_{self.context["lang"]}')


class BehavioralCategorySerializer(serializers.ModelSerializer):
    """One entry of {{ behavioralGroups }}."""

    items = BehavioralItemSerializer(many=True, read_only=True)
    label = serializers.SerializerMethodField()

    class Meta:
        model = BehavioralCategory
        fields = ['id', 'key', 'label', 'items']

    def get_label(self, obj):
        return getattr(obj, f'label_{self.context["lang"]}')
