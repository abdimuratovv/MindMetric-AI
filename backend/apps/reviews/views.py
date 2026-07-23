from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsAdmin
from apps.i18n import get_language
from apps.scoring.constants import INDICATOR_CHOICES, INDICATOR_SHORT_LABELS
from apps.scoring.models import FieldRecommendation, IndicatorScore, OverallScore
from apps.scoring.views import serialize_field_recommendation

from .models import RUBRIC_ITEMS, TeacherReview
from .status import status_style


class TeacherStudentListView(APIView):
    """
    GET /api/teacher/students/?search=&faculty=&course=&group=

    Feeds {{ teacherStudents }} — searchable by name/program, same `.filter()`
    semantics as the mockup's client-side search over `STUDENTS`, now a
    server-side query so the roster isn't hardcoded. faculty/course/group
    narrow it further using the student's onboarding-survey answers
    (accounts.StudentProfile) — options come from
    GET /api/admin/student-filter-options/.
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        lang = get_language(request)
        search = request.query_params.get('search', '')
        students = User.objects.filter(role=User.Role.STUDENT)
        if search:
            students = students.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(program__icontains=search)
            )
        faculty = request.query_params.get('faculty', '')
        if faculty:
            students = students.filter(student_profile__faculty=faculty)
        course = request.query_params.get('course', '')
        if course:
            students = students.filter(student_profile__course=course)
        group = request.query_params.get('group', '')
        if group:
            students = students.filter(student_profile__group=group)

        rows = []
        for student in students:
            overall = OverallScore.objects.filter(student=student).first()
            review = TeacherReview.objects.filter(student=student).first()
            status = review.status if review else 'pending'
            style = status_style(status, lang)
            rows.append({
                'id': student.id,
                'name': student.get_full_name() or student.email,
                'program': student.program,
                'initials': student.initials,
                'score': overall.score if overall else None,
                'statusLabel': style['label'], 'statusBg': style['bg'], 'statusColor': style['color'],
            })
        return Response(rows)


class TeacherStudentDetailView(APIView):
    """
    GET /api/teacher/students/{id}/

    Feeds `selectedStudent` (profile + score) and `{{ selectedStudent.indicatorTags }}`
    (all 10 indicators, not just the ones the student has completed — a student can reach
    a teacher review after finishing just one assessment, same as the results screens; see
    apps.scoring.views.ResultsSummaryView's docstring. Each tag carries `completed` so the
    reviewer can tell "not scored" apart from a genuine low score).
    """

    permission_classes = [IsAdmin]

    def get(self, request, student_id):
        lang = get_language(request)
        student = get_object_or_404(User, id=student_id, role=User.Role.STUDENT)
        overall = OverallScore.objects.filter(student=student).first()
        scores_by_key = {
            row.indicator_key: row.score
            for row in IndicatorScore.objects.filter(student=student)
        }
        field_recommendation = FieldRecommendation.objects.filter(student=student).first()

        return Response({
            'id': student.id,
            'name': student.get_full_name() or student.email,
            'program': student.program,
            'score': overall.score if overall else None,
            'programmingAptitudeScore': overall.programming_aptitude_score if overall else None,
            'fieldRecommendations': serialize_field_recommendation(field_recommendation, lang),
            'indicatorTags': [
                {
                    'label': INDICATOR_SHORT_LABELS[lang][key],
                    'score': scores_by_key.get(key),
                    'completed': key in scores_by_key,
                }
                for key, _ in INDICATOR_CHOICES
            ],
            'rubricLabels': [{'key': item['key'], 'label': item[lang]} for item in RUBRIC_ITEMS],
        })


class SubmitReviewView(APIView):
    """POST /api/teacher/students/{id}/review/ {rubric_scores, comment} — mirrors `submitReview`."""

    permission_classes = [IsAdmin]

    def post(self, request, student_id):
        student = get_object_or_404(User, id=student_id, role=User.Role.STUDENT)
        review, _ = TeacherReview.objects.get_or_create(student=student)
        review.reviewer = request.user
        review.rubric_scores = request.data.get('rubric_scores', {})
        review.comment = request.data.get('comment', '')
        review.submitted = True
        review.submitted_at = timezone.now()
        review.save()
        return Response({'reviewSubmitted': True})
