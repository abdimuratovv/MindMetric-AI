from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import HasCompletedProfile, IsStudent
from apps.i18n import get_language
from apps.scoring.engine import AdaptiveTestingEngine
from apps.scoring.state_tracker import StudentStateTracker
from apps.scoring.views import serialize_achievement

from .coding_sandbox import run_test_cases
from .models import (
    AssessmentAttempt,
    BehavioralCategory,
    BehavioralResponse,
    CodingProblem,
    CodingSubmission,
    CognitiveQuestion,
)
from .serializers import (
    BehavioralCategorySerializer,
    CodingProblemSerializer,
    CognitiveQuestionSerializer,
)

MCQ_QUESTION_CAP = 5  # questions per MCQ-pattern indicator (math/logic/creative/problem_solving/attention/iq)
MCQ_TIME_LIMIT_SECONDS = 300  # 5 min, set on start for any MCQ-pattern attempt

# Mirrors {{ behavioralError }} — the only free-text message this app emits itself.
ALL_STATEMENTS_REQUIRED = {
    'ru': 'Пожалуйста, ответьте на все утверждения перед отправкой.',
    'uz': "Iltimos, yuborishdan oldin barcha bayonotlarga javob bering.",
}

ANSWER_REQUIRED = {
    'ru': 'Пожалуйста, дайте ответ.',
    'uz': 'Iltimos, javob bering.',
}


def _valid_kind(kind: str, allowed: frozenset) -> str:
    """Validates a `<str:kind>` URL kwarg against a pattern's type set, 404s otherwise."""
    if kind not in {t.value for t in allowed}:
        raise Http404(f'Unknown assessment type: {kind}')
    return kind


def _completion_response(result: dict, lang: str) -> Response:
    """
    Shared by Submit{Mcq,Coding,Likert}View — `result` is StudentStateTracker.
    complete_attempt()'s {score, achievement}. Feeds the frontend's post-submit
    completion screen: the score just earned on this indicator, plus a badge
    payload only when this submission newly earned/upgraded one.
    """
    payload = {'score': result['score']}
    if result['achievement']:
        payload['achievement'] = serialize_achievement(result['achievement'], lang)
    else:
        payload['achievement'] = None
    return Response(payload)


class AssessmentStatusView(APIView):
    """
    GET /api/assessments/status/

    Feeds the `assessments` cards on the selection screen (status badge +
    button label per card) via StudentStateTracker.get_resume_state — already
    generic across however many AssessmentAttempt.Type values exist.
    """

    permission_classes = [IsStudent, HasCompletedProfile]

    def get(self, request):
        return Response(StudentStateTracker().get_resume_state(request.user))


# -- MCQ pattern: math / logic / creative / problem_solving / attention / iq --------------

class StartMcqAttemptView(APIView):
    """POST /api/assessments/mcq/<kind>/start/"""

    permission_classes = [IsStudent, HasCompletedProfile]

    def post(self, request, kind):
        kind = _valid_kind(kind, AssessmentAttempt.MCQ_TYPES)
        tracker = StudentStateTracker()
        attempt = tracker.start_or_restart_attempt(request.user, kind, time_remaining_seconds=MCQ_TIME_LIMIT_SECONDS)
        return Response({
            'assessment_type': attempt.assessment_type,
            'status': attempt.status,
            'time_remaining_seconds': attempt.time_remaining_seconds,
        })


class NextMcqQuestionView(APIView):
    """
    GET /api/assessments/mcq/<kind>/next-question/

    Delegates to AdaptiveTestingEngine.select_next_question. Returns null when
    the attempt has reached MCQ_QUESTION_CAP answered questions, which the
    frontend treats the same way as "last question" (Next → "Submit test").
    """

    permission_classes = [IsStudent]

    def get(self, request, kind):
        kind = _valid_kind(kind, AssessmentAttempt.MCQ_TYPES)
        attempt = get_object_or_404(AssessmentAttempt, student=request.user, assessment_type=kind)
        answered = attempt.cognitive_responses.count()
        if answered >= MCQ_QUESTION_CAP:
            return Response({'question': None, 'cqNumber': answered, 'cqTotal': MCQ_QUESTION_CAP})

        question = AdaptiveTestingEngine().select_next_question(attempt)
        lang = get_language(request)
        return Response({
            'question': CognitiveQuestionSerializer(question, context={'lang': lang}).data if question else None,
            'cqNumber': answered + 1,
            'cqTotal': MCQ_QUESTION_CAP,
            'time_remaining_seconds': attempt.time_remaining_seconds,
        })


class AnswerMcqView(APIView):
    """
    POST /api/assessments/mcq/<kind>/answer/
      {question_id, selected_indices}  — single/multi-select questions
      {question_id, essay_text}        — essay/open-ended questions

    Records the response, updates the student's ability estimate for that
    indicator, and returns whether the attempt is done.
    """

    permission_classes = [IsStudent]

    def post(self, request, kind):
        kind = _valid_kind(kind, AssessmentAttempt.MCQ_TYPES)
        attempt = get_object_or_404(AssessmentAttempt, student=request.user, assessment_type=kind)
        question = get_object_or_404(CognitiveQuestion, id=request.data.get('question_id'))
        selected_indices = request.data.get('selected_indices')
        essay_text = request.data.get('essay_text')
        response_time_ms = request.data.get('response_time_ms')

        if question.question_type == CognitiveQuestion.QuestionType.ESSAY:
            if not (essay_text and essay_text.strip()):
                return Response({'detail': ANSWER_REQUIRED[get_language(request)]}, status=status.HTTP_400_BAD_REQUEST)
        elif not selected_indices:
            return Response({'detail': ANSWER_REQUIRED[get_language(request)]}, status=status.HTTP_400_BAD_REQUEST)

        engine = AdaptiveTestingEngine()
        response = engine.record_answer(
            attempt, question.id, selected_indices=selected_indices, essay_text=essay_text,
            response_time_ms=int(response_time_ms) if response_time_ms is not None else None,
        )

        answered = attempt.cognitive_responses.count()
        return Response({
            'correctness': response.correctness,
            'answered': answered,
            'is_last': answered >= MCQ_QUESTION_CAP,
            'time_remaining_seconds': attempt.time_remaining_seconds,
        })


class SubmitMcqView(APIView):
    """
    POST /api/assessments/mcq/<kind>/submit/ — finalizes the attempt, *except*
    for HYBRID_TYPES (algorithmic), where the MCQ phase is only half the
    assessment: this stashes its score and hands off to the coding phase
    instead of completing anything, returning {phase: 'coding'} so the
    frontend's Hybrid wrapper knows to mount the Coding screen next.

    Otherwise returns {score, achievement} (achievement is null unless this
    submission newly earned/upgraded a badge) so the frontend can show a
    completion screen with the just-earned score and, when applicable, a
    badge reveal.
    """

    permission_classes = [IsStudent]

    def post(self, request, kind):
        kind = _valid_kind(kind, AssessmentAttempt.MCQ_TYPES)
        attempt = get_object_or_404(AssessmentAttempt, student=request.user, assessment_type=kind)
        if kind in AssessmentAttempt.HYBRID_TYPES:
            StudentStateTracker().finish_mcq_phase(attempt)
            return Response({'phase': 'coding'})
        result = StudentStateTracker().complete_attempt(attempt)
        return _completion_response(result, get_language(request))


# -- Coding pattern: the coding phase of algorithmic's hybrid attempt ----------------------

class StartCodingView(APIView):
    """
    POST /api/assessments/coding/start/ — begins the coding phase of the
    algorithmic hybrid attempt (the MCQ phase already put it IN_PROGRESS, so
    start_or_restart_attempt is a no-op here beyond returning the row).
    """

    permission_classes = [IsStudent, HasCompletedProfile]

    def post(self, request):
        tracker = StudentStateTracker()
        attempt = tracker.start_or_restart_attempt(request.user, AssessmentAttempt.Type.ALGORITHMIC)
        tracker.start_coding_phase(attempt)
        return Response({
            'assessment_type': attempt.assessment_type,
            'status': attempt.status,
            'time_remaining_seconds': attempt.time_remaining_seconds,
        })


class CodingProblemView(APIView):
    """GET /api/assessments/coding/problem/ — {{ codingProblem.* }}."""

    permission_classes = [IsStudent]

    def get(self, request):
        problem = CodingProblem.objects.filter(is_active=True).first()
        return Response(CodingProblemSerializer(problem, context={'lang': get_language(request)}).data)


class RunCodingView(APIView):
    """
    POST /api/assessments/coding/run/  {code}

    Executes `code` against the problem's *sample* (non-hidden) test cases via
    apps.assessments.coding_sandbox and returns {{ testResults }} shape. Doesn't
    count toward the attempt-count penalty in state_tracker._score_hybrid — only
    "Submit solution" (is_final=True) rows do.
    """

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = get_object_or_404(
            AssessmentAttempt, student=request.user, assessment_type=AssessmentAttempt.Type.ALGORITHMIC,
        )
        problem = CodingProblem.objects.filter(is_active=True).first()
        code = request.data.get('code', '')

        sample_cases = [c for c in problem.test_cases if not c.get('hidden')]
        test_results = run_test_cases(problem.function_name, code, sample_cases)
        passed_count = sum(1 for r in test_results if r['passed'])

        CodingSubmission.objects.create(
            attempt=attempt, problem=problem, code=code, is_final=False,
            test_results=test_results, passed_count=passed_count, total_count=len(sample_cases),
        )
        return Response({'testResults': test_results})


class SubmitCodingView(APIView):
    """
    POST /api/assessments/coding/submit/ {code} — full hidden suite, finalizes the attempt.

    Returns {score, achievement}, same shape as SubmitMcqView — see
    _completion_response.
    """

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = get_object_or_404(
            AssessmentAttempt, student=request.user, assessment_type=AssessmentAttempt.Type.ALGORITHMIC,
        )
        problem = CodingProblem.objects.filter(is_active=True).first()
        code = request.data.get('code', '')

        test_results = run_test_cases(problem.function_name, code, problem.test_cases)
        passed_count = sum(1 for r in test_results if r['passed'])

        CodingSubmission.objects.create(
            attempt=attempt, problem=problem, code=code, is_final=True,
            test_results=test_results, passed_count=passed_count, total_count=len(test_results),
        )
        result = StudentStateTracker().complete_attempt(attempt)
        return _completion_response(result, get_language(request))


# -- Likert pattern: teamwork / patience / learning_speed ----------------------------------

class StartLikertAttemptView(APIView):
    """POST /api/assessments/likert/<kind>/start/"""

    permission_classes = [IsStudent, HasCompletedProfile]

    def post(self, request, kind):
        kind = _valid_kind(kind, AssessmentAttempt.LIKERT_TYPES)
        tracker = StudentStateTracker()
        attempt = tracker.start_or_restart_attempt(request.user, kind)
        return Response({
            'assessment_type': attempt.assessment_type,
            'status': attempt.status,
            'time_remaining_seconds': attempt.time_remaining_seconds,
        })


class LikertItemsView(APIView):
    """
    GET /api/assessments/likert/<kind>/items/ — {{ behavioralGroups }}, scoped to
    the single BehavioralCategory matching `kind` (kind.upper() == category.key).
    Returned as a 1-element list so the frontend's existing `groups.map()` needs
    no restructuring.
    """

    permission_classes = [IsStudent]

    def get(self, request, kind):
        kind = _valid_kind(kind, AssessmentAttempt.LIKERT_TYPES)
        categories = BehavioralCategory.objects.filter(key=kind.upper()).prefetch_related('items')
        return Response(
            BehavioralCategorySerializer(categories, many=True, context={'lang': get_language(request)}).data
        )


class AnswerLikertView(APIView):
    """PATCH /api/assessments/likert/<kind>/answer/ {item_id, value} — autosave."""

    permission_classes = [IsStudent]

    def patch(self, request, kind):
        kind = _valid_kind(kind, AssessmentAttempt.LIKERT_TYPES)
        attempt = get_object_or_404(AssessmentAttempt, student=request.user, assessment_type=kind)
        BehavioralResponse.objects.update_or_create(
            attempt=attempt, item_id=request.data['item_id'],
            defaults={'scale_value': int(request.data['value'])},
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubmitLikertView(APIView):
    """
    POST /api/assessments/likert/<kind>/submit/ — completeness check + finalize.

    Returns {score, achievement}, same shape as SubmitMcqView — see
    _completion_response.
    """

    permission_classes = [IsStudent]

    def post(self, request, kind):
        kind = _valid_kind(kind, AssessmentAttempt.LIKERT_TYPES)
        attempt = get_object_or_404(AssessmentAttempt, student=request.user, assessment_type=kind)
        category = BehavioralCategory.objects.filter(key=kind.upper()).prefetch_related('items').first()
        total_items = category.items.count() if category else 0
        if attempt.behavioral_responses.count() < total_items:
            return Response(
                {'detail': ALL_STATEMENTS_REQUIRED[get_language(request)]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = StudentStateTracker().complete_attempt(attempt)
        return _completion_response(result, get_language(request))


class PauseAttemptView(APIView):
    """POST /api/assessments/<type>/pause/ — mirrors the focused-test header's 'Save & exit'."""

    permission_classes = [IsAuthenticated]

    def post(self, request, assessment_type):
        attempt = get_object_or_404(AssessmentAttempt, student=request.user, assessment_type=assessment_type)
        if 'time_remaining_seconds' in request.data:
            attempt.time_remaining_seconds = int(request.data['time_remaining_seconds'])
            attempt.save(update_fields=['time_remaining_seconds'])
        return Response(status=status.HTTP_204_NO_CONTENT)
