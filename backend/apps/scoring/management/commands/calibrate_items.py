"""
Runs JMLE item calibration (apps.scoring.calibration) against real response history
and reports, per MCQ indicator, which items got enough data to trust and what their
re-estimated (a, b) look like next to the current (seed-authored) values.

Dry-run by default — prints the report only. Pass --apply to persist the calibrated
(discrimination, difficulty) back onto CognitiveQuestion, and only for items that
cleared MIN_RESPONSES_PER_ITEM (see apps.scoring.calibration); under-sampled items
keep their current values either way.

Usage:
    python manage.py calibrate_items                    # dry run, all MCQ indicators
    python manage.py calibrate_items --indicator=math    # dry run, one indicator
    python manage.py calibrate_items --apply             # calibrate and persist
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.assessments.models import AssessmentAttempt, CognitiveQuestion, CognitiveResponse
from apps.scoring import calibration


class Command(BaseCommand):
    help = 'Calibrate CognitiveQuestion (discrimination, difficulty) from response history via JMLE.'

    def add_arguments(self, parser):
        parser.add_argument('--indicator', default=None, help='Limit to one indicator key (default: all MCQ indicators).')
        parser.add_argument('--apply', action='store_true', help='Persist calibrated params for sufficiently-sampled items (default: dry run).')

    def handle(self, *args, **options):
        indicator_filter = options['indicator']
        indicators = [t.value for t in AssessmentAttempt.MCQ_TYPES]
        if indicator_filter:
            indicators = [k for k in indicators if k == indicator_filter]

        for indicator_key in indicators:
            self._calibrate_one(indicator_key, apply_changes=options['apply'])

    @transaction.atomic
    def _calibrate_one(self, indicator_key: str, *, apply_changes: bool):
        questions = list(CognitiveQuestion.objects.filter(indicator_key=indicator_key))
        if not questions:
            return

        item_bank = {q.id: (q.discrimination, q.difficulty) for q in questions}
        response_matrix = {q.id: [] for q in questions}
        responses = CognitiveResponse.objects.filter(question__indicator_key=indicator_key).values(
            'question_id', 'attempt__student_id', 'correctness',
        )
        for r in responses:
            response_matrix[r['question_id']].append((r['attempt__student_id'], r['correctness']))

        result = calibration.calibrate_indicator(item_bank, response_matrix)

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n{indicator_key}: {len(questions)} items, "
            f"{sum(len(v) for v in response_matrix.values())} responses, "
            f"{len(result['persons'])} respondents "
            f"(sufficient_respondents={result['sufficient_respondents']}, "
            f"rounds_run={result['rounds_run']}, converged={result['converged']})"
        ))

        by_id = {q.id: q for q in questions}
        applied = 0
        for qid, item in sorted(result['items'].items(), key=lambda kv: by_id[kv[0]].key):
            q = by_id[qid]
            flag = 'OK' if item['sufficient_data'] else 'insufficient data'
            self.stdout.write(
                f"  [{flag:>17}] {q.key:<24} n={item['n_responses']:<4} "
                f"a: {q.discrimination:.2f} -> {item['a']:.2f}   b: {q.difficulty:.2f} -> {item['b']:.2f}"
            )
            if apply_changes and item['sufficient_data']:
                q.discrimination = item['a']
                q.difficulty = item['b']
                q.save(update_fields=['discrimination', 'difficulty'])
                applied += 1

        if apply_changes:
            self.stdout.write(self.style.SUCCESS(f"  Applied calibrated params to {applied}/{len(questions)} items."))
        else:
            self.stdout.write('  Dry run -- pass --apply to persist calibrated params for sufficiently-sampled items.')
