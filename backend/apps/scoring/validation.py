"""
Post-hoc psychometric validation diagnostics: item fit (infit/outfit mean-square
residuals), local independence (Q3 statistic), unidimensionality (largest-eigenvalue-
ratio of the standardized-residual correlation matrix — Reckase, 1979), and the test
information function/reliability curve. Pure Python (no numpy/scipy — see
apps.scoring.irt's module docstring), using power iteration for the two dominant
eigenvalues since these item banks are small enough (tens of items) for that to
converge in well under a second.

Every function here takes already-scored response data plus already-estimated
theta/item parameters — this module diagnoses a calibration, it doesn't produce one;
see apps.scoring.calibration for that half. Driven by apps.scoring.management.
commands.validate_psychometrics, which assembles the full per-indicator report.
"""
import math

from . import irt

# Rasch-family infit/outfit mean-square conventions (Wright & Linacre, 1994): outside
# [0.5, 1.5] is "noticeable but not degrading" to measurement; outside the stricter
# [0.7, 1.3] band is the threshold typically applied for high-stakes tests.
FIT_OK_RANGE = (0.7, 1.3)
FIT_WARN_RANGE = (0.5, 1.5)

# Local independence: Yen (1984) suggests flagging pairs whose |Q3| sits well above the
# average pairwise Q3; a fixed 0.2 absolute threshold is used here for simplicity.
Q3_FLAG_THRESHOLD = 0.2
MIN_SHARED_FOR_Q3 = 10  # minimum respondents who answered *both* items in a pair before trusting their residual correlation

# Unidimensionality: ratio of the residual correlation matrix's first to second
# eigenvalue. Reckase (1979) treats a ratio at or above this as evidence of one
# dominant trait; below it, a second meaningful dimension may be present.
EIGENVALUE_RATIO_OK = 3.0


def item_fit(item_a: float, item_b: float, responses) -> dict:
    """
    responses: list of (theta, u) for every respondent who answered this item.
    Standardized residual z = (u-P)/sqrt(P(1-P)); outfit = mean(z^2) (unweighted —
    sensitive to unexpected responses from far-off-target respondents); infit =
    sum((u-P)^2)/sum(P(1-P)) (information-weighted — sensitive to unexpected
    responses from on-target respondents, generally the more diagnostic of the two).
    """
    n = len(responses)
    if n == 0:
        return {'infit': None, 'outfit': None, 'n': 0}

    sum_z2 = 0.0
    sum_resid2 = 0.0
    sum_w = 0.0
    counted = 0
    for theta, u in responses:
        p = irt.probability_2pl(theta, item_a, item_b)
        w = p * (1.0 - p)
        if w < 1e-8:
            continue  # ~zero information at this theta (item far too easy/hard for this respondent) — excluded to avoid a near-zero denominator
        resid = u - p
        sum_z2 += (resid * resid) / w
        sum_resid2 += resid * resid
        sum_w += w
        counted += 1

    if counted == 0 or sum_w == 0:
        return {'infit': None, 'outfit': None, 'n': n}
    return {'infit': sum_resid2 / sum_w, 'outfit': sum_z2 / counted, 'n': n}


def fit_flag(infit, outfit) -> str:
    """'ok' / 'warn' / 'misfit' / 'insufficient_data' — see FIT_OK_RANGE/FIT_WARN_RANGE."""
    if infit is None or outfit is None:
        return 'insufficient_data'
    if FIT_OK_RANGE[0] <= infit <= FIT_OK_RANGE[1] and FIT_OK_RANGE[0] <= outfit <= FIT_OK_RANGE[1]:
        return 'ok'
    if FIT_WARN_RANGE[0] <= infit <= FIT_WARN_RANGE[1] and FIT_WARN_RANGE[0] <= outfit <= FIT_WARN_RANGE[1]:
        return 'warn'
    return 'misfit'


def _pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0 or vy <= 0:
        return None
    return cov / math.sqrt(vx * vy)


def _standardized_residuals(item_params: dict, response_matrix: dict, student_thetas: dict) -> dict:
    """{question_id: {student_id: z}} — shared by local_independence_q3 and unidimensionality_report."""
    residuals = {}
    for qid, (a, b) in item_params.items():
        residuals[qid] = {}
        for sid, u in response_matrix.get(qid, []):
            theta = student_thetas.get(sid)
            if theta is None:
                continue
            p = irt.probability_2pl(theta, a, b)
            w = p * (1.0 - p)
            if w < 1e-8:
                continue
            residuals[qid][sid] = (u - p) / math.sqrt(w)
    return residuals


def local_independence_q3(item_params: dict, response_matrix: dict, student_thetas: dict) -> dict:
    """
    Q3 (Yen, 1984): pairwise correlation of standardized residuals between two items,
    among respondents who answered both. Large |Q3| between a pair means their
    residuals move together after conditioning on theta — a signature of local
    dependence (e.g. a shared sub-passage, or one item giving away another's answer)
    that the additive test-information formula assumes away.
    """
    residuals = _standardized_residuals(item_params, response_matrix, student_thetas)
    qids = list(item_params)

    pair_q3 = {}
    for i in range(len(qids)):
        for j in range(i + 1, len(qids)):
            qi, qj = qids[i], qids[j]
            shared = set(residuals[qi]) & set(residuals[qj])
            if len(shared) < MIN_SHARED_FOR_Q3:
                continue
            r = _pearson([residuals[qi][sid] for sid in shared], [residuals[qj][sid] for sid in shared])
            if r is not None:
                pair_q3[(qi, qj)] = r

    if not pair_q3:
        return {'pairs': {}, 'mean_abs_q3': None, 'max_abs_q3': None, 'flagged_pairs': []}

    abs_values = [abs(v) for v in pair_q3.values()]
    return {
        'pairs': pair_q3,
        'mean_abs_q3': sum(abs_values) / len(abs_values),
        'max_abs_q3': max(abs_values),
        'flagged_pairs': [pair for pair, v in pair_q3.items() if abs(v) >= Q3_FLAG_THRESHOLD],
    }


def _power_iteration(matrix, iterations: int = 200, tol: float = 1e-9):
    """Dominant eigenvalue/eigenvector of a symmetric matrix via power iteration."""
    n = len(matrix)
    vec = [1.0 / math.sqrt(n)] * n
    eigenvalue = 0.0
    for _ in range(iterations):
        new_vec = [sum(matrix[i][j] * vec[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x * x for x in new_vec))
        if norm < 1e-12:
            return 0.0, vec
        new_vec = [x / norm for x in new_vec]
        new_eigenvalue = sum(new_vec[i] * sum(matrix[i][j] * new_vec[j] for j in range(n)) for i in range(n))
        vec = new_vec
        if abs(new_eigenvalue - eigenvalue) < tol:
            eigenvalue = new_eigenvalue
            break
        eigenvalue = new_eigenvalue
    return eigenvalue, vec


def _deflate(matrix, eigenvalue, vec):
    """Removes the given eigenvalue/eigenvector from a symmetric matrix (Hotelling deflation) so the next power_iteration call finds the second-largest one."""
    n = len(matrix)
    return [[matrix[i][j] - eigenvalue * vec[i] * vec[j] for j in range(n)] for i in range(n)]


def unidimensionality_report(response_matrix: dict) -> dict:
    """
    Classical PCA-of-item-correlations unidimensionality check (Reckase, 1979): build
    the inter-item Pearson correlation matrix of RAW item scores and extract its two
    largest eigenvalues via power iteration. A single dominant trait should show a
    first eigenvalue well clear of the second; EIGENVALUE_RATIO_OK is the conventional
    cutoff for "well clear".

    Deliberately uses raw scores, not model residuals: this is the opposite input to
    local_independence_q3/item_fit above, and on purpose — the Rasch/Winsteps "PCA of
    residuals" convention instead flags a *large* residual eigenvalue as a problem
    (a second dimension the fitted model failed to explain), which would invert this
    function's ratio>=EIGENVALUE_RATIO_OK "large ratio is good" direction. Reckase's
    raw-score version keeps one consistent reading across this module: bigger ratio,
    stronger single-factor evidence.
    """
    qids = list(response_matrix)
    n_items = len(qids)
    if n_items < 3:
        return {'available': False, 'reason': 'need at least 3 items to extract 2 eigenvalues'}

    scores = {qid: {sid: float(u) for sid, u in response_matrix[qid]} for qid in qids}
    matrix = [[1.0] * n_items for _ in range(n_items)]
    for i in range(n_items):
        for j in range(i + 1, n_items):
            shared = set(scores[qids[i]]) & set(scores[qids[j]])
            r = 0.0
            if len(shared) >= MIN_SHARED_FOR_Q3:
                r = _pearson([scores[qids[i]][sid] for sid in shared], [scores[qids[j]][sid] for sid in shared]) or 0.0
            matrix[i][j] = matrix[j][i] = r

    eig1, vec1 = _power_iteration(matrix)
    eig2, _vec2 = _power_iteration(_deflate(matrix, eig1, vec1))
    ratio = (eig1 / eig2) if eig2 > 1e-6 else float('inf')
    return {
        'available': True,
        'eigenvalue_1': eig1, 'eigenvalue_2': eig2, 'ratio': ratio,
        'unidimensional': ratio >= EIGENVALUE_RATIO_OK,
    }


def _frange(start, stop, step):
    n = int(round((stop - start) / step))
    return [round(start + i * step, 4) for i in range(n + 1)]


def test_information_curve(item_params: dict, theta_points=None) -> list:
    """Test information / SE / reliability at a grid of theta points — the classic CAT/IRT 'test information function' table, for reporting or plotting."""
    if theta_points is None:
        theta_points = _frange(irt.THETA_MIN, irt.THETA_MAX, 0.5)
    items = list(item_params.values())
    return [
        {
            'theta': theta,
            'information': irt.test_information(theta, items),
            'se': irt.standard_error(theta, items),
            'reliability': irt.reliability(theta, items),
        }
        for theta in theta_points
    ]
