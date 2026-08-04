"""
AdaptiveTestingEngine — Computerized Adaptive Testing (CAT) driven by a 2-parameter
logistic (2PL) IRT model (see apps.scoring.irt): every answered item re-estimates the
student's ability (theta) from that attempt's full response history so far via
MLE-with-EAP-fallback, and the next item is chosen by Maximum Fisher Information
(MFI) at the current theta. Replaces the mockup's fixed `COGNITIVE_QUESTIONS[cqIndex]`
walk entirely — see ARCHITECTURE.md §4 for the original design rationale.

Each MCQ-pattern AssessmentAttempt is scoped to exactly one indicator (its
`assessment_type` IS the indicator key — see AssessmentAttempt.MCQ_TYPES), so
question selection only needs to work within that one indicator's bank, not
round-robin across several.
"""
from apps.assessments.models import CognitiveQuestion, CognitiveResponse

from . import irt
from .essay_grader import essay_correctness, grade_essay_response
from .models import StudentAbilityEstimate

# Speed-aware response weighting: a student's own running-average response time on an
# indicator (StudentAbilityEstimate.avg_response_ms) is their baseline, not a fixed global
# number — a "fast" answer for one student may be a "slow" one for another. When the speed
# signal and the correctness signal agree (fast+correct, slow+incorrect), that's a confident
# read on ability, so the response counts for more in the theta estimate — implemented as a
# case weight in a weighted (quasi-)likelihood (see irt.py's module docstring for why this is
# a different, more standard technique than Warm's (1989) WLE bias correction despite the
# similar name). When speed and correctness disagree (slow-but-correct careful work,
# fast-but-wrong guesses) the read is ambiguous, so the response keeps the plain weight of 1.0.
FAST_RATIO = 0.7   # answered in <=70% of their own average time for this indicator
SLOW_RATIO = 1.3   # answered in >=130% of their own average time for this indicator
TIME_BOOST = 1.6   # weight applied when speed and correctness agree
EMA_ALPHA = 0.3    # weight given to each new response time in the running average
TIME_CLAMP_MS = 180_000  # cap a single response_time_ms before it can skew the average/weight


class AdaptiveTestingEngine:
    def get_or_create_estimate(self, student, indicator_key: str) -> StudentAbilityEstimate:
        estimate, _ = StudentAbilityEstimate.objects.get_or_create(
            student=student, indicator_key=indicator_key, defaults={'theta': 0.0},
        )
        return estimate

    def _response_weight(self, avg_response_ms: float | None, response_time_ms: int | None, correctness: float) -> float:
        """>1.0 when this answer's speed backs up what its correctness already suggests."""
        if avg_response_ms is None or response_time_ms is None:
            return 1.0  # no personal baseline yet, or the client didn't report timing
        ratio = min(response_time_ms, TIME_CLAMP_MS) / avg_response_ms
        if correctness >= 1.0 and ratio <= FAST_RATIO:
            return TIME_BOOST
        if correctness <= 0.0 and ratio >= SLOW_RATIO:
            return TIME_BOOST
        return 1.0

    def _update_avg_response_ms(self, avg_response_ms: float | None, response_time_ms: int | None) -> float | None:
        if response_time_ms is None:
            return avg_response_ms
        clamped = min(response_time_ms, TIME_CLAMP_MS)
        if avg_response_ms is None:
            return float(clamped)
        return (1 - EMA_ALPHA) * avg_response_ms + EMA_ALPHA * clamped

    def select_next_question(self, attempt) -> CognitiveQuestion | None:
        indicator_key = attempt.assessment_type
        estimate = self.get_or_create_estimate(attempt.student, indicator_key)
        answered = CognitiveResponse.objects.filter(attempt=attempt).select_related('question')
        answered_ids = set(answered.values_list('question_id', flat=True))
        answered_types = set(answered.values_list('question__question_type', flat=True))

        candidates = list(
            CognitiveQuestion.objects.filter(indicator_key=indicator_key).exclude(id__in=answered_ids)
        )
        if not candidates:
            return None

        # Prefer a question_type the student hasn't seen yet this attempt — a content-
        # balancing constraint, so a bank that mixes single/multi/essay (currently only
        # `logic`) actually surfaces all of them within the capped question count — before
        # falling back to pure information-maximizing selection. No-op for single-type-only
        # banks, where every candidate already shares one type.
        unseen_types = {q.question_type for q in candidates} - answered_types
        if unseen_types:
            preferred = [q for q in candidates if q.question_type in unseen_types]
            if preferred:
                candidates = preferred

        # Maximum Fisher Information (MFI) selection: the item that carries the most
        # information about this student at their current ability estimate — see
        # irt.item_information. For 2PL this is generally close to, but not exactly, the
        # item whose difficulty is nearest theta, since high-discrimination items pull the
        # information peak in their favor even a bit off-target.
        return max(candidates, key=lambda q: irt.item_information(estimate.theta, q.discrimination, q.difficulty))

    def record_answer(
        self, attempt, question_id: int, *, selected_indices: list[int] | None = None, essay_text: str | None = None,
        response_time_ms: int | None = None,
    ) -> CognitiveResponse:
        question = CognitiveQuestion.objects.get(id=question_id)

        if question.question_type == CognitiveQuestion.QuestionType.ESSAY:
            rubric_scores = grade_essay_response(essay_text or '')
            correctness = essay_correctness(rubric_scores)
            stored_indices, stored_essay = [], (essay_text or '')
        elif question.question_type == CognitiveQuestion.QuestionType.MULTI:
            rubric_scores = {}
            stored_indices = sorted(set(selected_indices or []))
            correctness = 1.0 if stored_indices == sorted(question.correct_indices) else 0.0
            stored_essay = ''
        else:  # SINGLE — covers both classic MCQ and step-ordering questions folded into it
            rubric_scores = {}
            stored_indices = list(selected_indices or [])
            correctness = 1.0 if stored_indices == list(question.correct_indices) else 0.0
            stored_essay = ''

        # update_or_create (not create) — a double-click or network retry re-submitting the
        # same question would otherwise hit CognitiveResponse's one_response_per_question
        # constraint and crash with an unhandled 500 instead of just no-op'ing.
        response, created = CognitiveResponse.objects.update_or_create(
            attempt=attempt, question=question,
            defaults={
                'selected_indices': stored_indices, 'essay_text': stored_essay,
                'rubric_scores': rubric_scores, 'correctness': correctness,
                'response_time_ms': response_time_ms,
            },
        )

        # Only fold into the ability estimate once per question — a resubmission
        # shouldn't count the same answer twice against theta.
        if created:
            estimate = self.get_or_create_estimate(attempt.student, question.indicator_key)
            estimate.avg_response_ms = self._update_avg_response_ms(estimate.avg_response_ms, response_time_ms)

            # Re-estimate theta from this attempt's full response history so far (not an
            # incremental nudge from just the newest answer) — the standard CAT approach:
            # MLE where the response pattern has an interior maximum, EAP (prior-regularized,
            # always finite) otherwise. See irt.estimate_theta. Every response in the history
            # is weighted against the *current* (most up to date) avg_response_ms baseline, so
            # all of them are judged on the same footing at estimation time.
            history = CognitiveResponse.objects.filter(
                attempt=attempt, question__indicator_key=question.indicator_key,
            ).select_related('question')
            weighted_responses = [
                (
                    r.question.discrimination, r.question.difficulty, r.correctness,
                    self._response_weight(estimate.avg_response_ms, r.response_time_ms, r.correctness),
                )
                for r in history
            ]
            estimate.theta, estimate.se, estimate.estimation_method = irt.estimate_theta(weighted_responses)
            estimate.save(update_fields=['theta', 'se', 'estimation_method', 'avg_response_ms', 'updated_at'])

        return response
