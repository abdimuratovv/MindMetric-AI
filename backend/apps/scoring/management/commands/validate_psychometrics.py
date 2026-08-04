"""
Prints the full psychometric validation report for each MCQ indicator's item bank:
item fit (infit/outfit), local independence (Q3), unidimensionality (eigenvalue
ratio), and the test information/reliability curve — the diagnostics apps.scoring.
validation implements and that a CAT/IRT methodology write-up is expected to report
(item calibration itself is calibrate_items, not this command).

Computes each student's theta fresh from their response history under the item
bank's *current* (a, b) — independent of whatever is cached on StudentAbilityEstimate
— so the report is self-consistent with the response data it's validating.

Usage:
    python manage.py validate_psychometrics                  # all MCQ indicators
    python manage.py validate_psychometrics --indicator=math  # one indicator
"""
from django.core.management.base import BaseCommand

from apps.assessments.models import AssessmentAttempt, CognitiveQuestion, CognitiveResponse
from apps.scoring import irt, validation


class Command(BaseCommand):
    help = 'Print item fit / local independence / unidimensionality / test information for each MCQ indicator.'

    def add_arguments(self, parser):
        parser.add_argument('--indicator', default=None, help='Limit to one indicator key (default: all MCQ indicators).')

    def handle(self, *args, **options):
        indicator_filter = options['indicator']
        indicators = [t.value for t in AssessmentAttempt.MCQ_TYPES]
        if indicator_filter:
            indicators = [k for k in indicators if k == indicator_filter]

        for indicator_key in indicators:
            self._validate_one(indicator_key)

    def _validate_one(self, indicator_key: str):
        questions = list(CognitiveQuestion.objects.filter(indicator_key=indicator_key))
        if not questions:
            return
        by_id = {q.id: q for q in questions}
        item_bank = {q.id: (q.discrimination, q.difficulty) for q in questions}

        response_matrix = {q.id: [] for q in questions}
        rows = CognitiveResponse.objects.filter(question__indicator_key=indicator_key).values(
            'question_id', 'attempt__student_id', 'correctness',
        )
        for r in rows:
            response_matrix[r['question_id']].append((r['attempt__student_id'], r['correctness']))

        student_ids = sorted({sid for records in response_matrix.values() for sid, _u in records})
        by_student = {sid: [] for sid in student_ids}
        for qid, records in response_matrix.items():
            for sid, u in records:
                by_student[sid].append((qid, u))

        student_thetas = {}
        for sid in student_ids:
            responses = [(item_bank[qid][0], item_bank[qid][1], float(u), 1.0) for qid, u in by_student[sid]]
            theta, _se, _method = irt.estimate_theta(responses)
            student_thetas[sid] = theta

        n_responses = sum(len(v) for v in response_matrix.values())
        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n=== {indicator_key} -- {len(questions)} items, {n_responses} responses, {len(student_ids)} respondents ==="
        ))

        self.stdout.write(self.style.HTTP_INFO('-- Item fit (infit/outfit; ok in [0.70,1.30], warn in [0.50,1.50]) --'))
        flag_counts = {'ok': 0, 'warn': 0, 'misfit': 0, 'insufficient_data': 0}
        for q in sorted(questions, key=lambda q: q.key):
            responses = [(student_thetas[sid], float(u)) for sid, u in response_matrix[q.id]]
            fit = validation.item_fit(q.discrimination, q.difficulty, responses)
            flag = validation.fit_flag(fit['infit'], fit['outfit'])
            flag_counts[flag] += 1
            infit_s = f"{fit['infit']:.2f}" if fit['infit'] is not None else '  - '
            outfit_s = f"{fit['outfit']:.2f}" if fit['outfit'] is not None else '  - '
            self.stdout.write(f"  [{flag:>18}] {q.key:<24} n={fit['n']:<4} infit={infit_s} outfit={outfit_s}")
        self.stdout.write(f"  totals: {flag_counts}")

        self.stdout.write(self.style.HTTP_INFO('\n-- Local independence (Q3, flag threshold |Q3| >= 0.20) --'))
        li = validation.local_independence_q3(item_bank, response_matrix, student_thetas)
        if li['mean_abs_q3'] is None:
            self.stdout.write('  not enough shared respondents between any item pair to compute Q3.')
        else:
            self.stdout.write(f"  mean|Q3|={li['mean_abs_q3']:.3f}  max|Q3|={li['max_abs_q3']:.3f}  flagged_pairs={len(li['flagged_pairs'])}/{len(li['pairs'])}")
            for (qi, qj) in li['flagged_pairs']:
                self.stdout.write(f"    {by_id[qi].key} <-> {by_id[qj].key}: Q3={li['pairs'][(qi, qj)]:.3f}")

        self.stdout.write(self.style.HTTP_INFO('\n-- Unidimensionality (Reckase 1979: PCA of raw item-score correlations) --'))
        uni = validation.unidimensionality_report(response_matrix)
        if not uni['available']:
            self.stdout.write(f"  unavailable: {uni['reason']}")
        else:
            verdict = 'unidimensional' if uni['unidimensional'] else 'NOT clearly unidimensional'
            self.stdout.write(
                f"  eigenvalue_1={uni['eigenvalue_1']:.2f}  eigenvalue_2={uni['eigenvalue_2']:.2f}  "
                f"ratio={uni['ratio']:.2f}  ->  {verdict} (cutoff: ratio >= {validation.EIGENVALUE_RATIO_OK})"
            )

        self.stdout.write(self.style.HTTP_INFO('\n-- Test information / SE / marginal reliability --'))
        curve = validation.test_information_curve(item_bank)
        for row in curve:
            se_s = f"{row['se']:.2f}" if row['se'] is not None else '  - '
            rel_s = f"{row['reliability']:.2f}" if row['reliability'] is not None else '  - '
            self.stdout.write(f"  theta={row['theta']:>5.1f}   info={row['information']:6.2f}   SE={se_s}   reliability={rel_s}")
