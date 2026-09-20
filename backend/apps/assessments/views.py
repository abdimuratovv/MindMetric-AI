import random

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import HasCompletedProfile, IsStudent
from apps.i18n import get_language
from apps.scoring.engine import AdaptiveTestingEngine
from apps.scoring.state_tracker import StudentStateTracker, sjt_points
from apps.scoring.views import serialize_achievement

from . import limits
from .coding_sandbox import run_test_cases
from .models import (
    AnagramItem,
    AnagramResponse,
    AssessmentAttempt,
    CodingProblem,
    CodingSubmission,
    CognitiveQuestion,
    LearningItem,
    LearningModule,
    LearningResponse,
    SjtResponse,
    SjtScenario,
)
from .serializers import CodingProblemSerializer, CognitiveQuestionSerializer

# Question counts and time limits are admin-tunable — see apps.assessments.limits.


def _mcq_cap(kind: str) -> int:
    return limits.mcq_cap(kind)


def _mcq_time_limit(kind: str) -> int:
    return limits.mcq_time_limit_seconds(kind)


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
    Shared by every Submit*View — `result` is StudentStateTracker.
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


class AssessmentConfigView(APIView):
    """GET /api/assessments/config/ — effective question counts / time limits per indicator, for the selection cards."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(limits.get_all_config())


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
    the attempt has reached the indicator's question cap, which the
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
    the configured number of distinct problems have a final submission this cycle.
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
        if len(done_ids) >= limits.coding_task_cap():
            return Response({'problem': None, 'cpNumber': len(done_ids), 'cpTotal': limits.coding_task_cap()})

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
            'cpTotal': limits.coding_task_cap(),
        })


class RunCodingView(APIView):
    """
    POST /api/assessments/coding/run/  {problem_id, code}

    Executes `code` against `problem_id`'s *sample* (non-hidden) test cases via
    apps.assessments.coding_sandbox and returns {{ testResults }} shape. Doesn't
    count toward the coding-task cap or state_tracker._score_hybrid — only "Submit
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

    Returns {phase: 'next', cpNumber, cpTotal} until the configured number of distinct problems
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
        if done_count < limits.coding_task_cap():
            return Response({'phase': 'next', 'cpNumber': done_count + 1, 'cpTotal': limits.coding_task_cap()})

        result = StudentStateTracker().complete_attempt(attempt)
        return _completion_response(result, get_language(request))


# -- Learning pattern: learning_speed ------------------------------------------------------

LEARNING_FAMILY_ORDER = [
    LearningModule.Family.SYMBOLS, LearningModule.Family.PSEUDOCODE, LearningModule.Family.GRAMMAR,
]
LEARNING_BLOCKS = (1, 2, 3)


def _learning_attempt(request):
    return get_object_or_404(
        AssessmentAttempt, student=request.user, assessment_type=AssessmentAttempt.Type.LEARNING_SPEED,
    )


def _ensure_learning_plan(attempt) -> list[int]:
    """One module per family for this cycle, preferring modules never seen in a past cycle."""
    plan = attempt.learning_plan or {}
    if plan.get('cycle') == attempt.attempt_cycle and plan.get('modules'):
        return plan['modules']

    seen_ids = set(
        LearningResponse.objects.filter(attempt=attempt).values_list('item__module_id', flat=True)
    )
    module_ids = []
    for family in LEARNING_FAMILY_ORDER:
        candidates = list(LearningModule.objects.filter(family=family, is_active=True).values_list('id', flat=True))
        fresh = [m for m in candidates if m not in seen_ids]
        pool = fresh or candidates
        if pool:
            module_ids.append(random.choice(pool))
    attempt.learning_plan = {'cycle': attempt.attempt_cycle, 'modules': module_ids}
    attempt.save(update_fields=['learning_plan'])
    return module_ids


def _learning_items_by_module(module_ids):
    items = LearningItem.objects.filter(module_id__in=module_ids).order_by('block', 'order')
    by_module = {mid: [] for mid in module_ids}
    for item in items:
        by_module[item.module_id].append(item)
    return by_module


def _learning_position(attempt, module_ids):
    """First (module, block) with an unanswered item this cycle, or None when everything is answered."""
    answered = set(
        attempt.learning_responses.filter(cycle=attempt.attempt_cycle).values_list('item_id', flat=True)
    )
    by_module = _learning_items_by_module(module_ids)
    for index, module_id in enumerate(module_ids):
        items = by_module[module_id]
        for block in LEARNING_BLOCKS:
            pending = [i for i in items if i.block == block and i.id not in answered]
            if pending:
                started = any(i.id in answered for i in items)
                return {'index': index, 'module_id': module_id, 'block': block, 'pending': pending, 'started': started}
    return None


def _serialize_learning_item(item, lang):
    return {
        'id': item.id,
        'prompt': getattr(item, f'prompt_{lang}'),
        'code': item.code,
        'options': getattr(item, f'options_{lang}'),
    }


class StartLearningView(APIView):
    """POST /api/assessments/learning/start/"""

    permission_classes = [IsStudent, HasCompletedProfile]

    def post(self, request):
        attempt = StudentStateTracker().start_or_restart_attempt(request.user, AssessmentAttempt.Type.LEARNING_SPEED)
        _ensure_learning_plan(attempt)
        return Response({'assessment_type': attempt.assessment_type, 'status': attempt.status})


class LearningStateView(APIView):
    """
    GET /api/assessments/learning/state/ — where the student is: the module being
    studied/tested, the current block and its still-unanswered items. `phase` is
    'study' before the module's first answer (show the rules screen), 'block' after.
    """

    permission_classes = [IsStudent]

    def get(self, request):
        attempt = _learning_attempt(request)
        module_ids = _ensure_learning_plan(attempt)
        lang = get_language(request)
        total = LearningItem.objects.filter(module_id__in=module_ids).count()
        answered = attempt.learning_responses.filter(cycle=attempt.attempt_cycle).count()

        position = _learning_position(attempt, module_ids)
        if position is None:
            return Response({'done': True, 'answered': answered, 'total': total})

        module = LearningModule.objects.get(id=position['module_id'])
        return Response({
            'done': False,
            'phase': 'block' if position['started'] else 'study',
            'module': {
                'id': module.id,
                'title': getattr(module, f'title_{lang}'),
                'rules': getattr(module, f'rules_{lang}'),
                'studySeconds': module.study_seconds,
            },
            'moduleNumber': position['index'] + 1,
            'moduleTotal': len(module_ids),
            'block': position['block'],
            'blockTotal': len(LEARNING_BLOCKS),
            'blockSize': LearningItem.objects.filter(module_id=module.id, block=position['block']).count(),
            'items': [_serialize_learning_item(i, lang) for i in position['pending']],
            'answered': answered,
            'total': total,
        })


class AnswerLearningView(APIView):
    """
    POST /api/assessments/learning/answer/ {item_id, selected_index, response_time_ms}

    Correctness is withheld until the item's whole block is answered; the answer
    that completes a block returns that block's feedback (correct answer +
    explanation per item). An answer can't be changed once recorded.
    """

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = _learning_attempt(request)
        module_ids = _ensure_learning_plan(attempt)
        item = get_object_or_404(LearningItem, id=request.data.get('item_id'), module_id__in=module_ids)
        selected_index = request.data.get('selected_index')
        if selected_index is None:
            return Response({'detail': ANSWER_REQUIRED[get_language(request)]}, status=status.HTTP_400_BAD_REQUEST)
        response_time_ms = request.data.get('response_time_ms')

        LearningResponse.objects.get_or_create(
            attempt=attempt, item=item, cycle=attempt.attempt_cycle,
            defaults={
                'selected_index': int(selected_index),
                'is_correct': int(selected_index) == item.correct_index,
                'response_time_ms': int(response_time_ms) if response_time_ms is not None else None,
            },
        )

        block_items = list(LearningItem.objects.filter(module_id=item.module_id, block=item.block).order_by('order'))
        responses = {
            r.item_id: r for r in attempt.learning_responses.filter(
                cycle=attempt.attempt_cycle, item__in=block_items,
            )
        }
        if len(responses) < len(block_items):
            return Response({'block_complete': False, 'feedback': None, 'done': False})

        lang = get_language(request)
        feedback = [
            {
                **_serialize_learning_item(i, lang),
                'selectedIndex': responses[i.id].selected_index,
                'correctIndex': i.correct_index,
                'isCorrect': responses[i.id].is_correct,
                'explanation': getattr(i, f'explanation_{lang}'),
            }
            for i in block_items
        ]
        done = _learning_position(attempt, module_ids) is None
        return Response({'block_complete': True, 'feedback': feedback, 'done': done})


class SubmitLearningView(APIView):
    """POST /api/assessments/learning/submit/ — finalizes once every item is answered."""

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = _learning_attempt(request)
        module_ids = _ensure_learning_plan(attempt)
        if _learning_position(attempt, module_ids) is not None:
            return Response({'detail': ANSWER_REQUIRED[get_language(request)]}, status=status.HTTP_400_BAD_REQUEST)
        result = StudentStateTracker().complete_attempt(attempt)
        return _completion_response(result, get_language(request))


# -- SJT pattern: teamwork -----------------------------------------------------------------

SJT_PICK_BOTH = {
    'ru': 'Выберите и самое правильное, и самое неправильное действие — это должны быть разные варианты.',
    'uz': "Eng to'g'ri va eng noto'g'ri harakatni tanlang — ular turli variantlar bo'lishi kerak.",
}


def _sjt_attempt(request):
    return get_object_or_404(AssessmentAttempt, student=request.user, assessment_type=AssessmentAttempt.Type.TEAMWORK)


class StartSjtView(APIView):
    """POST /api/assessments/sjt/start/"""

    permission_classes = [IsStudent, HasCompletedProfile]

    def post(self, request):
        attempt = StudentStateTracker().start_or_restart_attempt(request.user, AssessmentAttempt.Type.TEAMWORK)
        return Response({'assessment_type': attempt.assessment_type, 'status': attempt.status})


class NextSjtView(APIView):
    """
    GET /api/assessments/sjt/next/ — a scenario not answered this cycle, preferring
    ones never seen in a past cycle. Options are shuffled per request; each carries
    its original `index`, which is what the answer endpoint expects back.
    Returns {scenario: null} once the configured number of scenarios are answered.
    """

    permission_classes = [IsStudent]

    def get(self, request):
        attempt = _sjt_attempt(request)
        answered_ids = set(
            attempt.sjt_responses.filter(cycle=attempt.attempt_cycle).values_list('scenario_id', flat=True)
        )
        cap = min(limits.sjt_scenario_cap(), SjtScenario.objects.filter(is_active=True).count())
        if len(answered_ids) >= cap:
            return Response({'scenario': None, 'number': len(answered_ids), 'total': cap})

        seen_ids = set(SjtResponse.objects.filter(attempt=attempt).values_list('scenario_id', flat=True))
        candidates = list(SjtScenario.objects.filter(is_active=True).exclude(id__in=answered_ids))
        fresh = [s for s in candidates if s.id not in seen_ids]
        scenario = random.choice(fresh or candidates)

        lang = get_language(request)
        options = [{'index': i, 'text': text} for i, text in enumerate(getattr(scenario, f'options_{lang}'))]
        random.shuffle(options)
        return Response({
            'scenario': {'id': scenario.id, 'situation': getattr(scenario, f'situation_{lang}'), 'options': options},
            'number': len(answered_ids) + 1,
            'total': cap,
        })


class AnswerSjtView(APIView):
    """POST /api/assessments/sjt/answer/ {scenario_id, best_index, worst_index, response_time_ms}"""

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = _sjt_attempt(request)
        scenario = get_object_or_404(SjtScenario, id=request.data.get('scenario_id'), is_active=True)
        best, worst = request.data.get('best_index'), request.data.get('worst_index')
        valid = range(len(scenario.ratings))
        if best is None or worst is None or int(best) not in valid or int(worst) not in valid or int(best) == int(worst):
            return Response({'detail': SJT_PICK_BOTH[get_language(request)]}, status=status.HTTP_400_BAD_REQUEST)
        response_time_ms = request.data.get('response_time_ms')

        SjtResponse.objects.get_or_create(
            attempt=attempt, scenario=scenario, cycle=attempt.attempt_cycle,
            defaults={
                'best_index': int(best), 'worst_index': int(worst),
                'points': sjt_points(scenario.ratings, int(best), int(worst)),
                'response_time_ms': int(response_time_ms) if response_time_ms is not None else None,
            },
        )
        answered = attempt.sjt_responses.filter(cycle=attempt.attempt_cycle).count()
        cap = min(limits.sjt_scenario_cap(), SjtScenario.objects.filter(is_active=True).count())
        return Response({'answered': answered, 'is_last': answered >= cap})


class SubmitSjtView(APIView):
    """POST /api/assessments/sjt/submit/"""

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = _sjt_attempt(request)
        result = StudentStateTracker().complete_attempt(attempt)
        return _completion_response(result, get_language(request))


# -- Anagram pattern: patience -------------------------------------------------------------

# Serving order: easy warm-up first, then unsolvable sets hidden among medium/hard ones.
ANAGRAM_SLOTS = ['easy', 'easy', 'easy', 'medium', 'medium', 'unsolvable', 'medium', 'hard', 'unsolvable', 'hard', 'hard', 'unsolvable']
ANAGRAM_MAX_ACTIVE_MS = 10 * 60 * 1000


def _anagram_attempt(request):
    return get_object_or_404(AssessmentAttempt, student=request.user, assessment_type=AssessmentAttempt.Type.PATIENCE)


def _ensure_anagram_plan(attempt, lang) -> list[int]:
    """Fills ANAGRAM_SLOTS in the student's language, preferring items never served in a past cycle."""
    plan = attempt.anagram_plan or {}
    if plan.get('cycle') == attempt.attempt_cycle and plan.get('items'):
        return plan['items']

    # Every served item ends up with a response (the attempt can't finish until each
    # is solved or skipped), so responses alone tell us what past cycles showed.
    seen_ids = set(AnagramResponse.objects.filter(attempt=attempt).values_list('item_id', flat=True))
    pools = {}
    for item in AnagramItem.objects.filter(language=lang, is_active=True):
        pools.setdefault(item.difficulty, []).append(item.id)

    chosen = []
    for difficulty in ANAGRAM_SLOTS:
        candidates = [i for i in pools.get(difficulty, []) if i not in chosen]
        fresh = [i for i in candidates if i not in seen_ids]
        pool = fresh or candidates
        if pool:
            chosen.append(random.choice(pool))
    attempt.anagram_plan = {'cycle': attempt.attempt_cycle, 'items': chosen}
    attempt.save(update_fields=['anagram_plan'])
    return chosen


def _anagram_current(attempt, item_ids):
    finished = set(
        attempt.anagram_responses.filter(cycle=attempt.attempt_cycle)
        .filter(Q(solved=True) | Q(skipped=True)).values_list('item_id', flat=True)
    )
    for index, item_id in enumerate(item_ids):
        if item_id not in finished:
            return index, item_id
    return None, None


def _scrambled(item) -> list[str]:
    letters = list(item.letters)
    for _ in range(20):
        random.shuffle(letters)
        if ''.join(letters) not in item.answers and ''.join(letters) != item.letters:
            break
    return letters


def _anagram_response(attempt, item, active_ms):
    response, _ = AnagramResponse.objects.get_or_create(attempt=attempt, item=item, cycle=attempt.attempt_cycle)
    if active_ms is not None:
        response.active_ms = max(response.active_ms, min(int(active_ms), ANAGRAM_MAX_ACTIVE_MS))
    return response


def _current_anagram_item(request, attempt):
    item_ids = _ensure_anagram_plan(attempt, get_language(request))
    _, current_id = _anagram_current(attempt, item_ids)
    item_id = request.data.get('item_id')
    if current_id is None or str(item_id) != str(current_id):
        raise Http404('Not the current anagram')
    return AnagramItem.objects.get(id=current_id)


class StartAnagramView(APIView):
    """POST /api/assessments/anagram/start/"""

    permission_classes = [IsStudent, HasCompletedProfile]

    def post(self, request):
        attempt = StudentStateTracker().start_or_restart_attempt(request.user, AssessmentAttempt.Type.PATIENCE)
        _ensure_anagram_plan(attempt, get_language(request))
        return Response({'assessment_type': attempt.assessment_type, 'status': attempt.status})


class CurrentAnagramView(APIView):
    """
    GET /api/assessments/anagram/current/ — the next unfinished anagram as shuffled
    letter tiles. Never reveals answers or which items are unsolvable.
    """

    permission_classes = [IsStudent]

    def get(self, request):
        attempt = _anagram_attempt(request)
        item_ids = _ensure_anagram_plan(attempt, get_language(request))
        index, item_id = _anagram_current(attempt, item_ids)
        if item_id is None:
            return Response({'item': None, 'number': len(item_ids), 'total': len(item_ids)})
        item = AnagramItem.objects.get(id=item_id)
        response = attempt.anagram_responses.filter(item=item, cycle=attempt.attempt_cycle).first()
        return Response({
            'item': {'id': item.id, 'letters': _scrambled(item), 'activeMs': response.active_ms if response else 0},
            'number': index + 1,
            'total': len(item_ids),
        })


class GuessAnagramView(APIView):
    """POST /api/assessments/anagram/guess/ {item_id, guess, active_ms} → {correct}"""

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = _anagram_attempt(request)
        item = _current_anagram_item(request, attempt)
        guess = str(request.data.get('guess', '')).strip().upper()
        response = _anagram_response(attempt, item, request.data.get('active_ms'))
        correct = guess in item.answers
        if correct:
            response.solved = True
        elif sorted(guess) == sorted(item.letters) and guess not in response.guesses:
            response.guesses = [*response.guesses, guess]
        response.save()
        return Response({'correct': correct})


class SkipAnagramView(APIView):
    """POST /api/assessments/anagram/skip/ {item_id, active_ms}"""

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = _anagram_attempt(request)
        item = _current_anagram_item(request, attempt)
        response = _anagram_response(attempt, item, request.data.get('active_ms'))
        response.skipped = True
        response.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubmitAnagramView(APIView):
    """POST /api/assessments/anagram/submit/ — finalizes once every anagram is solved or skipped."""

    permission_classes = [IsStudent]

    def post(self, request):
        attempt = _anagram_attempt(request)
        item_ids = _ensure_anagram_plan(attempt, get_language(request))
        if _anagram_current(attempt, item_ids)[1] is not None:
            return Response({'detail': ANSWER_REQUIRED[get_language(request)]}, status=status.HTTP_400_BAD_REQUEST)
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
