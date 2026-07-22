from django.db.models import Avg, Count, Max, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsAdmin
from apps.assessments.models import AssessmentAttempt, BehavioralCategory, BehavioralItem, CognitiveQuestion
from apps.assessments.serializers import (
    AdminBehavioralItemCreateSerializer,
    AdminBehavioralItemUpdateSerializer,
    AdminCognitiveQuestionCreateSerializer,
    AdminCognitiveQuestionUpdateSerializer,
)
from apps.i18n import get_language
from apps.reviews.models import TeacherReview
from apps.reviews.status import status_style
from apps.scoring import calculators
from apps.scoring.constants import FIELD_CHOICES, FIELD_LABELS, INDICATOR_CHOICES, INDICATOR_LABELS
from apps.scoring.models import FieldRecommendation, IndicatorScore, OverallScore

# indicator keys whose assessment uses the MCQ question bank (CognitiveQuestion);
# every other indicator uses the Likert self-report pattern (BehavioralCategory/Item).
MCQ_INDICATOR_KEYS = {t.value for t in AssessmentAttempt.MCQ_TYPES}

# CognitiveResponse/BehavioralResponse both use on_delete=PROTECT against these
# models, so a question/item a student has already answered can't be deleted —
# surfaced verbatim as {detail} by the frontend's api client.
CANNOT_DELETE_MESSAGE = {
    'ru': 'Этот вопрос уже содержит ответы студентов, его нельзя удалить.',
    'uz': "Bu savolga talabalar javob bergan, uni o'chirib bo'lmaydi.",
}


def _serialize_mcq(question, lang):
    return {
        'id': question.id,
        'category': getattr(question, f'category_{lang}'),
        'categoryRu': question.category_ru, 'categoryUz': question.category_uz,
        'type': question.question_type,
        'prompt': getattr(question, f'prompt_{lang}'),
        'promptRu': question.prompt_ru, 'promptUz': question.prompt_uz,
        'options': getattr(question, f'options_{lang}'),
        'optionsRu': question.options_ru, 'optionsUz': question.options_uz,
        'correctIndices': question.correct_indices,
        'difficulty': question.difficulty,
    }


def _serialize_likert(item, lang):
    return {
        'id': item.id,
        'prompt': getattr(item, f'text_{lang}'),
        'textRu': item.text_ru, 'textUz': item.text_uz,
        'reverseScored': item.reverse_scored,
    }

# NOTE: {{ k.delta }} in the mockup ("+64 this week", "+1.8 vs last term") compares
# against a prior period. A real implementation needs a periodic snapshot
# (e.g. a nightly AdminKpiSnapshot row) to diff against — out of scope for this
# scaffold; the fields below are wired but the "vs last period" comparison is a TODO.
# The placeholder text itself is still translated so it never leaks English to the UI.
NO_PRIOR_PERIOD = {
    'ru': 'нет данных за прошлый период',
    'uz': 'avvalgi davr uchun maʼlumot yoʼq',
}

MONTH_ABBR = {
    'ru': ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'],
    'uz': ['yan', 'fev', 'mar', 'apr', 'may', 'iyun', 'iyul', 'avg', 'sen', 'okt', 'noy', 'dek'],
}


def _format_date(dt, lang: str) -> str:
    return f'{MONTH_ABBR[lang][dt.month - 1]} {dt.day}'


class PublicStatsView(APIView):
    """
    GET /api/public/stats/ — feeds the welcome screen's {{ welcomeStats }} tiles.
    No auth required (it's the marketing landing page); numbers are the same
    aggregate style as AdminKpiView but only the ones safe to show publicly.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        lang = get_language(request)
        total_assessed = OverallScore.objects.count()
        reviewed = TeacherReview.objects.filter(submitted=True).count()
        agreement_rate = round(100 * reviewed / total_assessed) if total_assessed else 0
        indicator_count = len(dict(IndicatorScore._meta.get_field('indicator_key').choices))

        labels = {
            'ru': ['Оценено студентов', 'Согласие преподавателей', 'Ключевых показателей', 'Быстрее ручной проверки'],
            'uz': ['Baholangan talabalar', "O'qituvchilar rozilik darajasi", "Asosiy ko'rsatkichlar", "Qo'lda tekshirishdan tezroq"],
        }[lang]

        return Response([
            {'value': f'{total_assessed:,}', 'label': labels[0]},
            {'value': f'{agreement_rate}%', 'label': labels[1]},
            {'value': str(indicator_count), 'label': labels[2]},
            {'value': '3.2×', 'label': labels[3]},
        ])


class AdminKpiView(APIView):
    """GET /api/admin/kpis/ — feeds the 4 {{ adminKpis }} tiles."""

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        total_assessed = OverallScore.objects.count()
        avg_score = OverallScore.objects.aggregate(avg=Avg('score'))['avg'] or 0
        total_attempts = AssessmentAttempt.objects.count()
        completed_attempts = AssessmentAttempt.objects.filter(status=AssessmentAttempt.Status.COMPLETED).count()
        completion_rate = round(100 * completed_attempts / total_attempts) if total_attempts else 0
        flagged = TeacherReview.objects.filter(flagged=True).count()
        flagged_unresolved = TeacherReview.objects.filter(flagged=True, submitted=False).count()

        labels = {
            'ru': ['Всего оценено', 'Средний балл способностей', 'Доля завершения', 'Отмечено для проверки'],
            'uz': ['Jami baholandi', "O'rtacha qobiliyat balli", 'Yakunlanish darajasi', 'Koʼrib chiqish uchun belgilangan'],
        }[lang]
        unresolved_suffix = {'ru': 'не решено', 'uz': 'hal qilinmagan'}[lang]

        return Response([
            {'label': labels[0], 'value': f'{total_assessed:,}', 'delta': NO_PRIOR_PERIOD[lang], 'deltaColor': '#93A39A'},
            {'label': labels[1], 'value': f'{avg_score:.1f}', 'delta': NO_PRIOR_PERIOD[lang], 'deltaColor': '#93A39A'},
            {'label': labels[2], 'value': f'{completion_rate}%', 'delta': NO_PRIOR_PERIOD[lang], 'deltaColor': '#93A39A'},
            {'label': labels[3], 'value': str(flagged), 'delta': f'{flagged_unresolved} {unresolved_suffix}', 'deltaColor': '#B8862F'},
        ])


class CohortDistributionView(APIView):
    """GET /api/admin/distribution/ — feeds {{ distributionBars }} (score-band histogram)."""

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        scores = list(OverallScore.objects.values_list('score', flat=True))
        total = len(scores) or 1
        bucket_order = ['foundational', 'developing', 'high', 'exceptional']
        buckets = {k: 0 for k in bucket_order}
        for score in scores:
            buckets[calculators.band_for(score, lang)['key']] += 1

        max_count = max(buckets.values()) or 1
        colors = {'foundational': '#BD5B4C', 'developing': '#B8862F', 'high': '#4FAE83', 'exceptional': '#2E7052'}
        short_labels = calculators.BAND_SHORT_LABELS[lang]
        return Response([
            {
                'label': short_labels[key], 'pctLabel': f'{round(100 * count / total)}%',
                'barHeight': f'{round(100 * count / max_count)}%', 'color': colors[key],
            }
            for key, count in buckets.items()
        ])


FIELD_DISTRIBUTION_COLORS = {
    'backend': '#2E5570', 'frontend': '#BD5B4C', 'data_ai': '#3E7EA6',
    'qa': '#B8862F', 'team_lead': '#1F374B', 'devops': '#4FAE83',
}


class FieldDistributionView(APIView):
    """
    GET /api/admin/field-distribution/ — cohort breakdown of which specialization
    (apps.scoring.constants.FIELD_CHOICES) each student's indicator profile best
    fits. Mirrors CohortDistributionView's bucket-and-count shape, but only counts
    students whose FieldRecommendation cleared the confidence gate (`is_confident`)
    — students still mid-assessment have no top_field_key and would otherwise
    silently inflate an "undetermined" bucket that isn't a real specialization.
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        top_keys = list(
            FieldRecommendation.objects.filter(is_confident=True).values_list('top_field_key', flat=True)
        )
        total = len(top_keys) or 1
        buckets = {key: 0 for key, _ in FIELD_CHOICES}
        for key in top_keys:
            buckets[key] += 1

        max_count = max(buckets.values()) or 1
        return Response([
            {
                'key': key, 'label': FIELD_LABELS[lang][key],
                'count': count, 'pctLabel': f'{round(100 * count / total)}%',
                'barHeight': f'{round(100 * count / max_count)}%', 'color': FIELD_DISTRIBUTION_COLORS[key],
            }
            for key, count in buckets.items()
        ])


class FacultyActivityView(APIView):
    """GET /api/admin/faculty-activity/ — feeds {{ facultyActivity }}."""

    permission_classes = [IsAdmin]

    def get(self, request):
        rows = (
            TeacherReview.objects.filter(submitted=True)
            .values('reviewer__first_name', 'reviewer__last_name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        return Response([
            {'name': f"{r['reviewer__first_name']} {r['reviewer__last_name']}".strip(), 'count': r['count']}
            for r in rows
        ])


class AdminStudentListView(APIView):
    """GET /api/admin/students/?search= — feeds the {{ adminStudents }} recent-assessments table."""

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        search = request.query_params.get('search', '')
        students = User.objects.filter(role=User.Role.STUDENT)
        if search:
            students = students.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )
        students = students.annotate(last_activity=Max('attempts__completed_at'))

        rows = []
        for student in students:
            overall = OverallScore.objects.filter(student=student).first()
            review = TeacherReview.objects.filter(student=student).first()
            style = status_style(review.status if review else 'pending', lang)
            rows.append({
                'name': student.get_full_name() or student.email,
                'program': student.program,
                'score': overall.score if overall else None,
                'statusLabel': style['label'], 'statusBg': style['bg'], 'statusColor': style['color'],
                'date': _format_date(student.last_activity, lang) if student.last_activity else None,
            })
        return Response(rows)


class QuestionBankView(APIView):
    """
    GET /api/admin/question-bank/ — every indicator with its full question bank,
    grouped for the admin "Savollar banki" screen. Unlike
    apps.assessments.serializers.CognitiveQuestionSerializer (used on the
    student-facing endpoints), this includes `correctIndices` — IsAdmin is the
    only thing standing between this and the whole answer key leaking, so it
    must never be relaxed to a broader permission.

    Each row carries both the language-picked display value *and* the raw
    ru/uz pair (promptRu/promptUz etc.) — QuestionBankMcqDetailView/
    QuestionBankLikertDetailView below PATCH those same `id`s, and the edit
    form needs both languages at once rather than one fetch per language.
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        groups = []
        for key, _ in INDICATOR_CHOICES:
            if key in MCQ_INDICATOR_KEYS:
                questions = CognitiveQuestion.objects.filter(indicator_key=key).order_by('difficulty')
                serialized = [_serialize_mcq(q, lang) for q in questions]
                group_type = 'mcq'
            else:
                category = BehavioralCategory.objects.filter(key=key.upper()).prefetch_related('items').first()
                items = category.items.all() if category else []
                serialized = [_serialize_likert(item, lang) for item in items]
                group_type = 'likert'

            groups.append({
                'key': key,
                'label': INDICATOR_LABELS[lang][key],
                'type': group_type,
                'questionCount': len(serialized),
                'questions': serialized,
            })
        return Response(groups)


class QuestionBankMcqListView(APIView):
    """POST /api/admin/question-bank/mcq/ — create a new CognitiveQuestion under an MCQ indicator."""

    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = AdminCognitiveQuestionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        return Response(_serialize_mcq(question, get_language(request)), status=status.HTTP_201_CREATED)


class QuestionBankMcqDetailView(APIView):
    """PATCH/DELETE /api/admin/question-bank/mcq/<id>/ — edit or remove one CognitiveQuestion row."""

    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        question = get_object_or_404(CognitiveQuestion, pk=pk)
        serializer = AdminCognitiveQuestionUpdateSerializer(question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_serialize_mcq(question, get_language(request)))

    def delete(self, request, pk):
        question = get_object_or_404(CognitiveQuestion, pk=pk)
        try:
            question.delete()
        except ProtectedError:
            lang = get_language(request)
            return Response({'detail': CANNOT_DELETE_MESSAGE[lang]}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionBankLikertListView(APIView):
    """POST /api/admin/question-bank/likert/ — create a new BehavioralItem under a Likert indicator."""

    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = AdminBehavioralItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(_serialize_likert(item, get_language(request)), status=status.HTTP_201_CREATED)


class QuestionBankLikertDetailView(APIView):
    """PATCH/DELETE /api/admin/question-bank/likert/<id>/ — edit or remove one BehavioralItem row."""

    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        item = get_object_or_404(BehavioralItem, pk=pk)
        serializer = AdminBehavioralItemUpdateSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_serialize_likert(item, get_language(request)))

    def delete(self, request, pk):
        item = get_object_or_404(BehavioralItem, pk=pk)
        try:
            item.delete()
        except ProtectedError:
            lang = get_language(request)
            return Response({'detail': CANNOT_DELETE_MESSAGE[lang]}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)
