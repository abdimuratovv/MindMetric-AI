"""
Joint Maximum Likelihood Estimation (JMLE / "UCON") item calibration — Birnbaum's
(1968) alternating-conditional-estimation algorithm:

  1. fix item parameters, re-estimate every respondent's theta (apps.scoring.irt);
  2. rescale the theta scale to mean 0 / sd 1 — JMLE only identifies item and person
     parameters up to a joint linear transform, so without this step the scale drifts
     freely between rounds (see Baker & Kim, 2004, ch. 3);
  3. fix persons, re-estimate every item's (a, b) via 2D Newton-Raphson;
  4. repeat until both sides stop moving or the round budget runs out.

This module is pure data-in/data-out (no Django/ORM), so it can be driven by real
response history *or* synthetic data for validation — see the management command
`calibrate_items` for the Django-facing glue, and see the module-level sanity check
run during development (simulated respondents/items, recovered params checked
against the ground truth) for evidence the Newton-Raphson step is actually correct
and not just plausible-looking.

Needs real response volume to mean anything: classical guidance for stable 2PL
calibration is on the order of several hundred respondents (de Ayala, 2009, ch. 4) —
far more than a small pilot cohort provides. MIN_RESPONSES_PER_ITEM/MIN_RESPONDENTS
below are reported per item/indicator (`sufficient_data`/`sufficient_respondents`)
rather than silently overriding under-sampled items with noisy estimates.
"""
from collections import defaultdict
from statistics import mean, pstdev

from . import irt

MIN_RESPONSES_PER_ITEM = 30
MIN_RESPONDENTS = 30

_A_MIN, _A_MAX = 0.2, 3.0
_ITEM_STEP_CLAMP = 0.5
_ROUND_MAX_ITER = 25
_ROUND_TOL = 1e-3


def _update_item_params(a: float, b: float, person_theta_u):
    """
    One Newton-Raphson step on a single item's (a, b), holding respondent thetas
    fixed. person_theta_u: list of (theta, u).

    For the 2PL/Bernoulli log-likelihood, the observed Hessian equals the negative
    expected Fisher information exactly (a property of the logistic canonical link),
    so this is simultaneously a Newton-Raphson and a Fisher-scoring step — no
    approximation beyond the linearization Newton's method always makes.
    """
    g_a = g_b = 0.0
    h_aa = h_bb = h_ab = 0.0
    for theta, u in person_theta_u:
        p = irt.probability_2pl(theta, a, b)
        pq = p * (1.0 - p)
        g_a += (u - p) * (theta - b)
        g_b += -a * (u - p)
        h_aa += -pq * (theta - b) ** 2
        h_bb += -(a ** 2) * pq
        h_ab += a * pq * (theta - b)

    det = h_aa * h_bb - h_ab * h_ab
    if abs(det) < 1e-9:
        return a, b

    # delta = -H^-1 g, H = [[h_aa, h_ab], [h_ab, h_bb]] (symmetric 2x2 closed-form inverse)
    da = (-h_bb * g_a + h_ab * g_b) / det
    db = (h_ab * g_a - h_aa * g_b) / det
    da = max(-_ITEM_STEP_CLAMP, min(_ITEM_STEP_CLAMP, da))
    db = max(-_ITEM_STEP_CLAMP, min(_ITEM_STEP_CLAMP, db))

    a_new = min(_A_MAX, max(_A_MIN, a + da))
    b_new = min(irt.THETA_MAX, max(irt.THETA_MIN, b + db))
    return a_new, b_new


def calibrate_indicator(item_bank: dict, response_matrix: dict, *, max_rounds: int = _ROUND_MAX_ITER, tol: float = _ROUND_TOL) -> dict:
    """
    item_bank: {question_id: (a, b)} starting parameters (the seeded/manually-authored
        values — JMLE needs a starting point, it doesn't calibrate from nothing).
    response_matrix: {question_id: [(student_id, u), ...]} — every scored response to
        that item, across all attempts/students. Indicator-scoped: one indicator is one
        unidimensional item bank by construction (CognitiveQuestion.indicator_key), so
        calibration never mixes items that measure different traits.

    Returns {
        'items': {question_id: {'a', 'b', 'n_responses', 'sufficient_data'}},
        'persons': {student_id: {'theta', 'se', 'method', 'n_responses'}},
        'rounds_run': int, 'converged': bool, 'sufficient_respondents': bool,
    }
    """
    by_student = defaultdict(list)  # sid -> [(question_id, u), ...], precomputed once (avoids an O(n^2) rescan per round)
    for qid, records in response_matrix.items():
        for sid, u in records:
            by_student[sid].append((qid, u))
    student_ids = sorted(by_student)

    thetas = {sid: 0.0 for sid in student_ids}
    params = {qid: list(ab) for qid, ab in item_bank.items()}  # [a, b], mutated in place per round

    def responses_for(sid):
        return [(params[qid][0], params[qid][1], float(u), 1.0) for qid, u in by_student[sid]]

    converged = False
    rounds_run = 0
    for round_index in range(max_rounds):
        rounds_run = round_index + 1

        # -- person step: fix items, re-estimate every respondent's theta --
        new_thetas = {}
        max_theta_delta = 0.0
        for sid in student_ids:
            theta_hat, _se, _method = irt.estimate_theta(responses_for(sid), start=thetas[sid])
            max_theta_delta = max(max_theta_delta, abs(theta_hat - thetas[sid]))
            new_thetas[sid] = theta_hat
        thetas = new_thetas

        # -- resolve JMLE's location/scale indeterminacy: rescale persons to mean 0 / sd 1,
        # and apply the inverse transform to items so P(theta, a, b) is unchanged --
        values = list(thetas.values())
        if len(values) >= 2:
            m, sd = mean(values), pstdev(values)
            if sd > 1e-6:
                thetas = {sid: (t - m) / sd for sid, t in thetas.items()}
                for qid in params:
                    a, b = params[qid]
                    params[qid] = [a * sd, (b - m) / sd]

        # -- item step: fix persons, re-estimate each item's (a, b) --
        max_item_delta = 0.0
        for qid, records in response_matrix.items():
            if len(records) < 2:
                continue  # 2 free parameters need at least 2 data points to be identified at all
            pairs = [(thetas[sid], float(u)) for sid, u in records]
            a, b = params[qid]
            a_new, b_new = _update_item_params(a, b, pairs)
            # An item whose true discrimination is high (near-perfect separation in this
            # sample) pushes `a` toward +infinity — a well-known 2PL/logistic-regression
            # degeneracy — so a_new keeps hitting _A_MAX every round without settling. Once
            # pinned at a bound, that item's churn no longer counts against convergence; only
            # its (still-identified) b continues to.
            at_bound = a_new in (_A_MIN, _A_MAX)
            max_item_delta = max(max_item_delta, abs(b_new - b), 0.0 if at_bound else abs(a_new - a))
            params[qid] = [a_new, b_new]

        if max_theta_delta < tol and max_item_delta < tol:
            converged = True
            break

    items_out = {}
    for qid, (a, b) in params.items():
        n = len(response_matrix.get(qid, []))
        items_out[qid] = {'a': a, 'b': b, 'n_responses': n, 'sufficient_data': n >= MIN_RESPONSES_PER_ITEM}

    persons_out = {}
    for sid in student_ids:
        theta_hat, se, method = irt.estimate_theta(responses_for(sid), start=thetas[sid])
        persons_out[sid] = {'theta': theta_hat, 'se': se, 'method': method, 'n_responses': len(by_student[sid])}

    return {
        'items': items_out,
        'persons': persons_out,
        'rounds_run': rounds_run,
        'converged': converged,
        'sufficient_respondents': len(student_ids) >= MIN_RESPONDENTS,
    }
