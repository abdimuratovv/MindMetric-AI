import csv

from django.db.models import Avg, Count, F, Max, Q
from django.db.models.deletion import ProtectedError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import StudentProfile, User
from apps.accounts.permissions import IsAdmin
from apps.assessments.models import AnagramItem, AssessmentAttempt, CognitiveQuestion, LearningModule, SjtScenario
from apps.assessments.serializers import AdminCognitiveQuestionCreateSerializer, AdminCognitiveQuestionUpdateSerializer
from apps.i18n import get_language
from apps.reviews.models import TeacherReview
from apps.reviews.status import status_style
from apps.scoring import calculators
from apps.scoring.constants import FIELD_CHOICES, FIELD_LABELS, INDICATOR_CHOICES, INDICATOR_LABELS
from apps.scoring.models import FieldRecommendation, IndicatorScore, OverallScore
from apps.scoring.views import build_results_mistakes, build_results_summary

from .models import InstitutionSettings

# Indicator keys served by the learning / SJT / anagram patterns; every other
# indicator uses the MCQ question bank (CognitiveQuestion).
LEARNING_INDICATOR_KEYS = {t.value for t in AssessmentAttempt.LEARNING_TYPES}
SJT_INDICATOR_KEYS = {t.value for t in AssessmentAttempt.SJT_TYPES}
ANAGRAM_INDICATOR_KEYS = {t.value for t in AssessmentAttempt.ANAGRAM_TYPES}

# CognitiveResponse uses on_delete=PROTECT against CognitiveQuestion, so a question
# a student has already answered can't be deleted — surfaced verbatim as {detail}
# by the frontend's api client.
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


def _serialize_learning_module(module, lang):
    return {
        'id': module.id,
        'title': getattr(module, f'title_{lang}'),
        'rules': getattr(module, f'rules_{lang}'),
        'items': [
            {
                'id': item.id,
                'block': item.block,
                'prompt': getattr(item, f'prompt_{lang}'),
                'code': item.code,
                'options': getattr(item, f'options_{lang}'),
                'correctIndices': [item.correct_index],
                'explanation': getattr(item, f'explanation_{lang}'),
            }
            for item in module.items.all()
        ],
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


def _scoped_students(request):
    """Students narrowed by the faculty/course/group query params. Every admin
    overview widget goes through this so the dashboard filters apply page-wide."""
    students = User.objects.filter(role=User.Role.STUDENT)
    for param, lookup in (
        ('faculty', 'student_profile__faculty'),
        ('course', 'student_profile__course'),
        ('group', 'student_profile__group'),
    ):
        value = request.query_params.get(param, '')
        if value:
            students = students.filter(**{lookup: value})
    return students


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
        students = _scoped_students(request)
        scores = OverallScore.objects.filter(student__in=students)
        total_assessed = scores.count()
        total_students = students.count()
        avg_score = scores.aggregate(avg=Avg('score'))['avg'] or 0
        attempts = AssessmentAttempt.objects.filter(student__in=students)
        total_attempts = attempts.count()
        completed_attempts = attempts.filter(status=AssessmentAttempt.Status.COMPLETED).count()
        completion_rate = round(100 * completed_attempts / total_attempts) if total_attempts else 0
        reviews = TeacherReview.objects.filter(student__in=students)
        flagged = reviews.filter(flagged=True).count()
        flagged_unresolved = reviews.filter(flagged=True, submitted=False).count()

        labels = {
            'ru': ['Оценено студентов', 'Средний балл', 'Доля завершённых тестов', 'Ожидают проверки'],
            'uz': ['Baholangan talabalar', "O'rtacha ball", 'Tugallangan testlar ulushi', 'Tekshiruvni kutayotganlar'],
        }[lang]
        unresolved_suffix = {'ru': 'не решено', 'uz': 'hal qilinmagan'}[lang]

        return Response([
            {'label': labels[0], 'value': f'{total_assessed:,} / {total_students:,}', 'delta': '', 'deltaColor': '#93A39A'},
            {'label': labels[1], 'value': f'{avg_score:.1f} / 100', 'delta': '', 'deltaColor': '#93A39A'},
            {'label': labels[2], 'value': f'{completion_rate}%', 'delta': '', 'deltaColor': '#93A39A'},
            {'label': labels[3], 'value': str(flagged), 'delta': f'{flagged_unresolved} {unresolved_suffix}', 'deltaColor': '#B8862F'},
        ])


class CohortDistributionView(APIView):
    """GET /api/admin/distribution/ — feeds {{ distributionBars }} (score-band histogram)."""

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        scores = list(OverallScore.objects.filter(student__in=_scoped_students(request)).values_list('score', flat=True))
        total = len(scores) or 1
        bucket_order = ['foundational', 'developing', 'high']
        buckets = {k: 0 for k in bucket_order}
        for score in scores:
            buckets[calculators.band_for(score, lang)['key']] += 1

        max_count = max(buckets.values()) or 1
        colors = {'foundational': '#BD5B4C', 'developing': '#B8862F', 'high': '#2E7052'}
        short_labels = calculators.BAND_SHORT_LABELS[lang]
        return Response([
            {
                'label': short_labels[key], 'count': count, 'pctLabel': f'{round(100 * count / total)}%',
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
            FieldRecommendation.objects.filter(is_confident=True, student__in=_scoped_students(request)).values_list('top_field_key', flat=True)
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
            TeacherReview.objects.filter(submitted=True, student__in=_scoped_students(request))
            .values('reviewer__first_name', 'reviewer__last_name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        return Response([
            {'name': f"{r['reviewer__first_name']} {r['reviewer__last_name']}".strip(), 'count': r['count']}
            for r in rows
        ])


class StudentFilterOptionsView(APIView):
    """
    GET /api/admin/student-filter-options/

    Distinct faculty/course/group values from students' onboarding-survey
    answers (accounts.StudentProfile), feeding the roster filter dropdowns
    on the Overview and Review Queue screens. Not a fixed list — those
    fields are free text (accounts.serializers.StudentProfileSerializer).
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        def distinct_values(field):
            return list(
                StudentProfile.objects.exclude(**{field: ''})
                .order_by(field).values_list(field, flat=True).distinct()
            )

        return Response({
            'faculties': distinct_values('faculty'),
            'courses': distinct_values('course'),
            'groups': distinct_values('group'),
        })


STUDENT_LIST_DEFAULT_PAGE_SIZE = 10
STUDENT_LIST_MAX_PAGE_SIZE = 50
# `?ordering=` values -> (sort field, descending). Unlisted values fall back to name.
STUDENT_LIST_ORDERINGS = {
    'name': ('name', False), '-name': ('name', True),
    'score': ('score', False), '-score': ('score', True),
    'status': ('status', False), '-status': ('status', True),
    'date': ('date', False), '-date': ('date', True),
    'progress': ('progress', False), '-progress': ('progress', True),
}
STUDENT_LEVEL_KEYS = {'foundational', 'developing', 'high', 'none'}  # 'none' = no score yet
STUDENT_STATUS_KEYS = {'reviewed', 'flagged', 'pending'}


def _positive_int(raw, default, maximum=None):
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    if value < 1:
        return default
    return min(value, maximum) if maximum else value


def _student_entries(request, lang):
    """(row, sort values) per student for the current search/filters, already ordered
    per `?ordering=`. Shared by the paginated list and the CSV export."""
    search = request.query_params.get('search', '')
    students = _scoped_students(request)
    if search:
        students = students.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search)
        )
    students = students.annotate(
        last_activity=Max('attempts__completed_at'),
        group_name=F('student_profile__group'),
    )

    scores = dict(OverallScore.objects.filter(student__in=students).values_list('student_id', 'score'))
    progress = dict(
        IndicatorScore.objects.filter(student__in=students)
        .values_list('student_id').annotate(n=Count('indicator_key', distinct=True))
    )
    review_status = {}
    for review in TeacherReview.objects.filter(student__in=students).order_by('id'):
        review_status.setdefault(review.student_id, review.status)  # first review per student, as before

    entries = []
    for student in students:
        score = scores.get(student.id)
        status_key = review_status.get(student.id, 'pending')
        style = status_style(status_key, lang)
        level = calculators.band_for(score, lang) if score is not None else None
        name = student.get_full_name() or student.email
        entries.append(({
            'id': student.id,
            'name': name,
            'program': student.program,
            'group': student.group_name or '',
            'score': score,
            'progress': progress.get(student.id, 0), 'progressTotal': len(INDICATOR_CHOICES),
            'levelLabel': level['band'] if level else None,
            'levelBg': level['bg'] if level else None, 'levelColor': level['color'] if level else None,
            'statusLabel': style['label'], 'statusBg': style['bg'], 'statusColor': style['color'],
            'date': _format_date(student.last_activity, lang) if student.last_activity else None,
        }, {
            'name': name.lower(), 'score': score, 'status': style['label'], 'date': student.last_activity,
            'progress': progress.get(student.id, 0),
            'levelKey': level['key'] if level else 'none', 'statusKey': status_key,
        }))

    level_filter = request.query_params.get('level', '')
    if level_filter in STUDENT_LEVEL_KEYS:
        entries = [e for e in entries if e[1]['levelKey'] == level_filter]
    status_filter = request.query_params.get('status', '')
    if status_filter in STUDENT_STATUS_KEYS:
        entries = [e for e in entries if e[1]['statusKey'] == status_filter]

    field, descending = STUDENT_LIST_ORDERINGS.get(request.query_params.get('ordering', ''), ('name', False))
    entries.sort(key=lambda e: e[1]['name'])  # stable tiebreak for every ordering
    present = [e for e in entries if e[1][field] is not None]
    missing = [e for e in entries if e[1][field] is None]
    present.sort(key=lambda e: e[1][field], reverse=descending)
    return present + missing


class AdminStudentListView(APIView):
    """
    GET /api/admin/students/?search=&faculty=&course=&group=&level=&status=&ordering=&page=&pageSize=
    — feeds the student results table, returned as {results, total, page, pageSize}.
    Rows with no value for the sorted field (e.g. no score yet) always sort last.
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        entries = _student_entries(request, get_language(request))
        page_size = _positive_int(request.query_params.get('pageSize'), STUDENT_LIST_DEFAULT_PAGE_SIZE, STUDENT_LIST_MAX_PAGE_SIZE)
        total = len(entries)
        last_page = max(1, -(-total // page_size))
        page = min(_positive_int(request.query_params.get('page'), 1), last_page)
        start = (page - 1) * page_size
        return Response({
            'results': [row for row, _ in entries[start:start + page_size]],
            'total': total, 'page': page, 'pageSize': page_size,
        })


class AdminStudentDetailView(APIView):
    """
    GET /api/admin/students/<id>/ — one student's full result report for the admin
    (same summary/mistakes payloads the student sees on their own results screen),
    plus their profile and the teacher-review state.
    """

    permission_classes = [IsAdmin]

    def get(self, request, pk):
        lang = get_language(request)
        student = get_object_or_404(User, pk=pk, role=User.Role.STUDENT)
        profile = StudentProfile.objects.filter(user=student).first()
        review = TeacherReview.objects.filter(student=student).select_related('reviewer').first()
        style = status_style(review.status if review else 'pending', lang)
        last_activity = AssessmentAttempt.objects.filter(student=student).aggregate(last=Max('completed_at'))['last']
        reviewer_name = review.reviewer.get_full_name() if review and review.reviewer else ''
        return Response({
            'student': {
                'id': student.id,
                'name': student.get_full_name() or student.email,
                'email': student.email,
                'program': student.program,
                'faculty': profile.faculty if profile else '',
                'course': profile.course if profile else '',
                'group': profile.group if profile else '',
                'specialization': profile.specialization if profile else '',
                'lastActivity': _format_date(last_activity, lang) if last_activity else None,
            },
            'review': {
                'statusLabel': style['label'], 'statusBg': style['bg'], 'statusColor': style['color'],
                'comment': review.comment if review else '',
                'reviewerName': reviewer_name,
                'submittedAt': _format_date(review.submitted_at, lang) if review and review.submitted_at else None,
            },
            'summary': build_results_summary(student, lang),
            'mistakes': build_results_mistakes(student, lang),
        })


CSV_HEADERS = {
    'ru': ['Студент', 'Группа', 'Балл', 'Уровень', 'Показатели', 'Статус', 'Дата'],
    'uz': ['Talaba', 'Guruh', 'Ball', 'Daraja', "Ko'rsatkichlar", 'Holat', 'Sana'],
}


class AdminStudentExportView(APIView):
    """GET /api/admin/students/export/ — the whole filtered/searched/sorted list (not one page) as CSV."""

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        response.write('\ufeff')  # BOM so Excel opens the Cyrillic/Uzbek text as UTF-8
        writer = csv.writer(response)
        writer.writerow(CSV_HEADERS[lang])
        for row, _ in _student_entries(request, lang):
            writer.writerow([
                _csv_safe(row['name']), _csv_safe(row['group'] or row['program']),
                '' if row['score'] is None else row['score'],
                row['levelLabel'] or '', f"{row['progress']} / {row['progressTotal']}", row['statusLabel'], row['date'] or '',
            ])
        return response


def _csv_safe(value):
    """Neutralize spreadsheet formula injection: names/groups are student-typed free text."""
    return f"'{value}" if value and value[0] in '=+-@\t\r' else value


class AdminSettingsView(APIView):
    """GET/PATCH /api/admin/settings/ — institution name and academic term shown on the dashboard header."""

    permission_classes = [IsAdmin]

    @staticmethod
    def _payload(obj):
        return {'name': obj.name, 'academicTerm': obj.academic_term}

    def get(self, request):
        return Response(self._payload(InstitutionSettings.load()))

    def patch(self, request):
        obj = InstitutionSettings.load()
        for key, field, limit in (('name', 'name', 160), ('academicTerm', 'academic_term', 80)):
            if key in request.data:
                value = str(request.data[key] or '').strip()
                if len(value) > limit:
                    return Response({'detail': f'{key}: max {limit}'}, status=status.HTTP_400_BAD_REQUEST)
                setattr(obj, field, value)
        obj.save()
        return Response(self._payload(obj))


class QuestionBankView(APIView):
    """
    GET /api/admin/question-bank/ — every indicator with its full question bank,
    grouped for the admin "Savollar banki" screen. Unlike
    apps.assessments.serializers.CognitiveQuestionSerializer (used on the
    student-facing endpoints), this includes `correctIndices` — IsAdmin is the
    only thing standing between this and the whole answer key leaking, so it
    must never be relaxed to a broader permission.

    Each MCQ row carries both the language-picked display value *and* the raw
    ru/uz pair (promptRu/promptUz etc.) — QuestionBankMcqDetailView below
    PATCHes those same `id`s, and the edit form needs both languages at once
    rather than one fetch per language. Learning/SJT/anagram groups are
    read-only here (their content is seeded from apps.assessments.*_content).
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        groups = []
        for key, _ in INDICATOR_CHOICES:
            if key in SJT_INDICATOR_KEYS:
                scenarios = [
                    {
                        'id': s.id,
                        'situation': getattr(s, f'situation_{lang}'),
                        'options': getattr(s, f'options_{lang}'),
                        'ratings': s.ratings,
                    }
                    for s in SjtScenario.objects.filter(is_active=True)
                ]
                groups.append({
                    'key': key,
                    'label': INDICATOR_LABELS[lang][key],
                    'type': 'sjt',
                    'questionCount': len(scenarios),
                    'scenarios': scenarios,
                    'questions': [],
                })
                continue
            if key in LEARNING_INDICATOR_KEYS:
                modules = LearningModule.objects.filter(is_active=True).prefetch_related('items')
                serialized_modules = [_serialize_learning_module(m, lang) for m in modules]
                groups.append({
                    'key': key,
                    'label': INDICATOR_LABELS[lang][key],
                    'type': 'learning',
                    'questionCount': sum(len(m['items']) for m in serialized_modules),
                    'moduleCount': len(serialized_modules),
                    'modules': serialized_modules,
                    'questions': [],
                })
                continue
            if key in ANAGRAM_INDICATOR_KEYS:
                anagrams = [
                    {'id': a.id, 'language': a.language, 'difficulty': a.difficulty, 'letters': a.letters, 'answers': a.answers}
                    for a in AnagramItem.objects.filter(is_active=True)
                ]
                groups.append({
                    'key': key,
                    'label': INDICATOR_LABELS[lang][key],
                    'type': 'anagram',
                    'questionCount': len(anagrams),
                    'anagrams': anagrams,
                    'questions': [],
                })
                continue

            questions = CognitiveQuestion.objects.filter(indicator_key=key).order_by('difficulty')
            serialized = [_serialize_mcq(q, lang) for q in questions]
            groups.append({
                'key': key,
                'label': INDICATOR_LABELS[lang][key],
                'type': 'mcq',
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
