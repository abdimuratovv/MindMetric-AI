"""
StudentStateTracker — gives the mockup's in-memory `Component.state`
(`completed{}`, per-attempt progress, timers) a server-side home so a
session survives a refresh. See ARCHITECTURE.md §5.
"""
from django.utils import timezone

from apps.assessments.models import AssessmentAttempt, BehavioralResponse, CodingSubmission
from apps.i18n import DEFAULT_LANGUAGE

from . import achievements, calculators
from .models import Achievement, FieldRecommendation, IndicatorScore, OverallScore


class StudentStateTracker:
    def get_or_create_attempt(self, student, assessment_type: str) -> AssessmentAttempt:
        attempt, _ = AssessmentAttempt.objects.get_or_create(
            student=student, assessment_type=assessment_type,
        )
        return attempt

    def start_or_restart_attempt(self, student, assessment_type: str, *, time_remaining_seconds=None) -> AssessmentAttempt:
        """
        Shared by Start{Mcq,Likert,Coding}AttemptView. There's exactly one
        AssessmentAttempt row per (student, assessment_type) — the "Retake" button
        reuses it rather than creating a new one. A COMPLETED attempt's prior answers
        are no longer deleted here: they're left in place, tagged with the
        attempt_cycle they were answered in, and `attempt_cycle` is bumped so this
        run starts "empty" (every count/exclusion query elsewhere scopes to the
        *current* cycle). Keeping old rows around — instead of wiping them — is what
        lets AdaptiveTestingEngine.select_next_question and CodingProblemView avoid
        re-serving the same questions/tasks a retake would otherwise get, since the
        prior cycle's picks are still there to exclude.
        """
        attempt = self.get_or_create_attempt(student, assessment_type)
        if attempt.status == AssessmentAttempt.Status.COMPLETED:
            attempt.attempt_cycle += 1
            attempt.status = AssessmentAttempt.Status.NOT_STARTED
            attempt.completed_at = None
            attempt.mcq_phase_score = None
            attempt.coding_started_at = None
        if attempt.status == AssessmentAttempt.Status.NOT_STARTED:
            attempt.status = AssessmentAttempt.Status.IN_PROGRESS
            attempt.started_at = timezone.now()
            if time_remaining_seconds is not None:
                attempt.time_remaining_seconds = time_remaining_seconds
            attempt.save()
        return attempt

    def get_resume_state(self, student) -> dict:
        """Shape consumed by the selection screen's `assessments` cards."""
        attempts = {a.assessment_type: a for a in AssessmentAttempt.objects.filter(student=student)}
        result = {}
        for assessment_type in AssessmentAttempt.Type.values:
            attempt = attempts.get(assessment_type)
            result[assessment_type] = {
                'status': attempt.status if attempt else AssessmentAttempt.Status.NOT_STARTED,
                'time_remaining_seconds': attempt.time_remaining_seconds if attempt else None,
            }
        result['any_completed'] = any(
            v['status'] == AssessmentAttempt.Status.COMPLETED for v in result.values()
            if isinstance(v, dict)
        )
        return result

    def finish_mcq_phase(self, attempt: AssessmentAttempt) -> None:
        """
        Called by SubmitMcqView for a HYBRID_TYPES attempt instead of complete_attempt —
        the attempt isn't done yet (the coding phase is next), so this just stashes the
        MCQ phase's own score onto the attempt for _score_hybrid to blend in later,
        without touching `status`/`completed_at`.
        """
        responses = attempt.cognitive_responses.filter(cycle=attempt.attempt_cycle).select_related('question')
        results = [r.correctness for r in responses]
        score = round(100 * sum(results) / len(results)) if results else 0
        attempt.mcq_phase_score = score
        attempt.save(update_fields=['mcq_phase_score'])

    def start_coding_phase(self, attempt: AssessmentAttempt) -> None:
        """Called by StartCodingView — marks when the coding phase began, the baseline
        _score_hybrid measures elapsed solve time against target_time_seconds from."""
        attempt.coding_started_at = timezone.now()
        attempt.save(update_fields=['coding_started_at'])

    def complete_attempt(self, attempt: AssessmentAttempt) -> dict:
        """
        Returns {'score': int|None, 'achievement': Achievement|None} — `score`
        is this attempt's just-computed indicator score (None if nothing could
        be scored, e.g. an empty attempt), and `achievement` is set only when
        this submission newly earned or upgraded a badge, so the frontend's
        completion screen can react to *that* precisely rather than re-deriving
        it from a separately fetched achievement list.
        """
        attempt.status = AssessmentAttempt.Status.COMPLETED
        attempt.completed_at = timezone.now()
        attempt.save(update_fields=['status', 'completed_at'])

        result = {'score': None, 'achievement': None}
        if attempt.assessment_type in AssessmentAttempt.HYBRID_TYPES:
            result = self._score_hybrid(attempt)
        elif attempt.assessment_type in AssessmentAttempt.MCQ_TYPES:
            result = self._score_mcq(attempt)
        elif attempt.assessment_type in AssessmentAttempt.LIKERT_TYPES:
            result = self._score_likert(attempt)

        self._recompute_overall_score(attempt.student)
        return result

    # -- per-assessment indicator scoring -------------------------------------------------

    def _score_mcq(self, attempt: AssessmentAttempt) -> dict:
        responses = attempt.cognitive_responses.filter(cycle=attempt.attempt_cycle).select_related('question')
        results = [r.correctness for r in responses]
        if not results:
            return {'score': None, 'achievement': None}
        score = round(100 * sum(results) / len(results))
        return self._upsert_indicator_score(attempt.student, attempt.assessment_type, score)

    def _score_hybrid(self, attempt: AssessmentAttempt) -> dict:
        """
        Blends the MCQ phase's score (attempt.mcq_phase_score, stashed by
        finish_mcq_phase) with the coding phase's result: 0.4 x mcq + 0.6 x coding,
        weighted toward coding since it's the more direct signal of whether the
        student can actually produce working code, not just reason about it.

        The coding phase now runs CODING_TASK_CAP distinct problems (not one), so
        the coding portion is the *average* of each problem's own correctness x
        time_factor — one final submission per problem (CodingProblemView never
        re-offers a problem this cycle already has an is_final submission for, so
        there's normally exactly one; if a client ever double-submits, only the
        latest counts):
          - correctness: passed/total on that problem's full hidden suite.
          - time_factor: full credit at or under that problem's target_time_seconds
            (measured from the client-reported elapsed_ms, not a single phase-wide
            clock), tapering linearly to a 0.7 floor by 2x that target.
        """
        finals = list(
            attempt.coding_submissions.filter(cycle=attempt.attempt_cycle, is_final=True)
            .select_related('problem').order_by('created_at')
        )
        if not finals or attempt.mcq_phase_score is None:
            return {'score': None, 'achievement': None}

        latest_by_problem = {sub.problem_id: sub for sub in finals}  # last-write-wins, in created_at order

        per_problem_scores = []
        for sub in latest_by_problem.values():
            if sub.total_count == 0:
                continue
            correctness = 100 * sub.passed_count / sub.total_count
            target = sub.problem.target_time_seconds
            elapsed = sub.elapsed_ms / 1000 if sub.elapsed_ms is not None else target
            time_factor = 1.0 if elapsed <= target else max(0.7, 1 - 0.3 * (elapsed - target) / target)
            per_problem_scores.append(correctness * time_factor)
        if not per_problem_scores:
            return {'score': None, 'achievement': None}

        coding_score = sum(per_problem_scores) / len(per_problem_scores)
        score = round(0.4 * attempt.mcq_phase_score + 0.6 * coding_score)
        return self._upsert_indicator_score(attempt.student, 'algorithmic', score)

    def _score_likert(self, attempt: AssessmentAttempt) -> dict:
        # Each Likert-pattern attempt is scoped to exactly one BehavioralCategory
        # (kind.upper() == category.key), so every response feeds the same
        # indicator: attempt.assessment_type itself.
        responses = attempt.behavioral_responses.filter(cycle=attempt.attempt_cycle).select_related('item')
        values = []
        for response in responses:
            value = response.scale_value
            if response.item.reverse_scored:
                value = 6 - value  # 1..5 scale flip
            values.append(value)
        if not values:
            return {'score': None, 'achievement': None}
        avg = sum(values) / len(values)  # 1..5
        score = round((avg - 1) / 4 * 100)  # scale to 0..100
        return self._upsert_indicator_score(attempt.student, attempt.assessment_type, score)

    def _upsert_indicator_score(self, student, indicator_key: str, score: int) -> dict:
        score = max(0, min(100, score))
        IndicatorScore.objects.update_or_create(
            student=student, indicator_key=indicator_key, defaults={'score': score},
        )
        return {'score': score, 'achievement': self._award_achievement_if_earned(student, indicator_key, score)}

    def _award_achievement_if_earned(self, student, indicator_key: str, score: int):
        """
        Awards/upgrades the Achievement badge for this indicator if `score`
        newly qualifies for a higher tier than the student already holds.
        Returns the Achievement only when it was newly created or upgraded —
        None otherwise, so callers can distinguish "nothing to celebrate" from
        "already had this badge".
        """
        tier = achievements.tier_for_score(score)
        if tier is None:
            return None
        existing = Achievement.objects.filter(student=student, indicator_key=indicator_key).first()
        if existing and achievements.TIER_ORDER[existing.tier] >= achievements.TIER_ORDER[tier]:
            return None
        achievement, _ = Achievement.objects.update_or_create(
            student=student, indicator_key=indicator_key, defaults={'tier': tier, 'score': score},
        )
        return achievement

    def _recompute_overall_score(self, student) -> None:
        scores_by_key = dict(IndicatorScore.objects.filter(student=student).values_list('indicator_key', 'score'))
        if not scores_by_key:
            return
        overall = calculators.compute_overall_score(scores_by_key.values())
        # `band` here is a stable, language-independent bucket key (not display text —
        # every read path recomputes localized text fresh via calculators.band_for(lang)).
        band_info = calculators.band_for(overall, DEFAULT_LANGUAGE)
        OverallScore.objects.update_or_create(
            student=student, defaults={
                'score': overall,
                'band': band_info['key'],
                'programming_aptitude_score': calculators.compute_programming_aptitude(scores_by_key),
            },
        )
        self._recompute_field_recommendation(student, scores_by_key)

    def _recompute_field_recommendation(self, student, scores_by_key: dict) -> None:
        fit = calculators.compute_field_fit(scores_by_key)
        top_field_key = fit['fields'][0]['key'] if fit['available'] else ''
        FieldRecommendation.objects.update_or_create(
            student=student, defaults={
                'top_field_key': top_field_key,
                'fit_scores': {f['key']: f['score'] for f in fit['fields']},
                'completed_indicator_count': len(scores_by_key),
                'is_confident': fit['available'],
            },
        )
