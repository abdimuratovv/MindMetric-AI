import random

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

MCQ_QUESTION_CAP = 40  # questions per MCQ-pattern indicator (math/logic/creative/problem_solving/attention/iq)
ALGORITHMIC_MCQ_CAP = 20  # algorithmic's MCQ phase — its other 20 items are coding tasks, see CODING_TASK_CAP
CODING_TASK_CAP = 20  # coding tasks in algorithmic's coding phase
MCQ_SECONDS_PER_QUESTION = 60  # pacing baseline both time limits below scale from
MCQ_TIME_LIMIT_SECONDS = MCQ_QUESTION_CAP * MCQ_SECONDS_PER_QUESTION  # 40 min, non-algorithmic MCQ indicators
ALGORITHMIC_MCQ_TIME_LIMIT_SECONDS = ALGORITHMIC_MCQ_CAP * MCQ_SECONDS_PER_QUESTION  # 20 min, algorithmic's MCQ phase


def _mcq_cap(kind: str) -> int:
    return ALGORITHMIC_MCQ_CAP if kind == AssessmentAttempt.Type.ALGORITHMIC else MCQ_QUESTION_CAP


def _mcq_time_limit(kind: str) -> int:
    return ALGORITHMIC_MCQ_TIME_LIMIT_SECONDS if kind == AssessmentAttempt.Type.ALGORITHMIC else MCQ_TIME_LIMIT_SECONDS

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
        attempt = tracker.start_or_restart_attempt(request.user, kind, time_remaining_seconds=_mcq_time_limit(kind))
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
        cap = _mcq_cap(kind)
        answered = attempt.cognitive_responses.filter(cycle=attempt.attempt_cycle).count()
        if answered >= cap:
            return Response({'question': None, 'cqNumber': answered, 'cqTotal': cap})

        question = AdaptiveTestingEngine().select_next_question(attempt)
        lang = get_language(request)
        return Response({
            'question': CognitiveQuestionSerializer(question, context={'lang': lang}).data if question else None,
            'cqNumber': answered + 1,
            'cqTotal': cap,
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

        answered = attempt.cognitive_responses.filter(cycle=attempt.attempt_cycle).count()
        return Response({
            'correctness': response.correctness,
            'answered': answered,
            'is_last': answered >= _mcq_cap(kind),
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
    """
    GET /api/assessments/coding/problem/ — the next coding task in algorithmic's
    coding phase (mirrors NextMcqQuestionView's cqNumber/cqTotal as cpNumber/cpTotal).
    Excludes problems this cycle already has a final submission for, preferring ones
    never seen in any past cycle of this same attempt (falling back to allowing a
    repeat only once that's exhausted) — same history-aware, randomized approach as
    AdaptiveTestingEngine.select_next_question, just without the IRT ranking (coding
    problems aren't difficulty-calibrated). Returns {problem: null, ...} once
    CODING_TASK_CAP distinct problems have a final submission this cycle.
    """

    permission_classes = [IsStudent]

    def get(self, request):
        attempt = get_object_or_404(
            AssessmentAttempt, student=request.user, assessment_type=AssessmentAttempt.Type.ALGORITHMIC,
        )
        done_ids = set(
            attempt.coding_submissions.filter(cycle=attempt.attempt_cycle, is_final=True)
            .values_list('problem_id', flat=True)
        )
        if len(done_ids) >= CODING_TASK_CAP:
            return Response({'problem': None, 'cpNumber': len(done_ids), 'cpTotal': CODING_TASK_CAP})

        seen_ids = set(
            CodingSubmission.objects.filter(attempt=attempt, is_final=True).values_list('problem_id', flat=True)
        )
        candidates = list(CodingProblem.objects.filter(is_active=True).exclude(id__in=done_ids))
        fresh = [p for p in candidates if p.id not in seen_ids]
        pool = fresh or candidates
        problem = random.choice(pool) if pool else None
        return Response({
            'problem': CodingProblemSerializer(problem, context={'lang': get_language(request)}).data if problem else None,
            'cpNumber': len(done_ids) + 1,
            'cpTotal': CODING_TASK_CAP,
        })


class RunCodingView(APIView):
    """
    POST /api/assessments/coding/run/  {problem_id, code}

    Executes `code` against `problem_id`'s *sample* (non-hidden) test cases via
    apps.assessments.coding_sandbox and returns {{ testResults }} shape. Doesn't
    count toward CODING_TASK_CAP or state_tracker._score_hybrid — only "Submit
    solution" (is_final=True) rows do.
    """

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = get_object_or_404(
            AssessmentAttempt, student=request.user, assessment_type=AssessmentAttempt.Type.ALGORITHMIC,
        )
        problem = get_object_or_404(CodingProblem, id=request.data.get('problem_id'), is_active=True)
        code = request.data.get('code', '')

        sample_cases = [c for c in problem.test_cases if not c.get('hidden')]
        test_results = run_test_cases(problem.function_name, code, sample_cases)
        passed_count = sum(1 for r in test_results if r['passed'])

        CodingSubmission.objects.create(
            attempt=attempt, problem=problem, code=code, is_final=False, cycle=attempt.attempt_cycle,
            test_results=test_results, passed_count=passed_count, total_count=len(sample_cases),
        )
        return Response({'testResults': test_results})


class SubmitCodingView(APIView):
    """
    POST /api/assessments/coding/submit/ {problem_id, code, elapsed_ms} — full hidden
    suite for that one problem (elapsed_ms is client-measured time on this problem,
    shown -> submitted, mirroring AnswerMcqView's response_time_ms — feeds this
    problem's time_factor in state_tracker._score_hybrid).

    Returns {phase: 'next', cpNumber, cpTotal} until CODING_TASK_CAP distinct problems
    have a final submission this cycle — the frontend then fetches the next one via
    CodingProblemView, same shape as SubmitMcqView's {phase: 'coding'} hand-off. Once
    the cap is reached this finalizes the attempt instead, returning {score,
    achievement} like every other Submit*View — see _completion_response.
    """

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = get_object_or_404(
            AssessmentAttempt, student=request.user, assessment_type=AssessmentAttempt.Type.ALGORITHMIC,
        )
        problem = get_object_or_404(CodingProblem, id=request.data.get('problem_id'), is_active=True)
        code = request.data.get('code', '')
        elapsed_ms = request.data.get('elapsed_ms')

        test_results = run_test_cases(problem.function_name, code, problem.test_cases)
        passed_count = sum(1 for r in test_results if r['passed'])

        CodingSubmission.objects.create(
            attempt=attempt, problem=problem, code=code, is_final=True, cycle=attempt.attempt_cycle,
            test_results=test_results, passed_count=passed_count, total_count=len(test_results),
            elapsed_ms=int(elapsed_ms) if elapsed_ms is not None else None,
        )

        done_count = (
            attempt.coding_submissions.filter(cycle=attempt.attempt_cycle, is_final=True)
            .values('problem_id').distinct().count()
        )
        if done_count < CODING_TASK_CAP:
            return Response({'phase': 'next', 'cpNumber': done_count + 1, 'cpTotal': CODING_TASK_CAP})

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
            attempt=attempt, item_id=request.data['item_id'], cycle=attempt.attempt_cycle,
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
        if attempt.behavioral_responses.filter(cycle=attempt.attempt_cycle).count() < total_items:
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
