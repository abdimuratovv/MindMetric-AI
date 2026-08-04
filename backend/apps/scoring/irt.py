"""
Core 2-parameter logistic (2PL) IRT math — pure Python, no numpy/scipy (see
requirements.txt: this project has neither). Every other module that touches ability
or item parameters (engine.py, calibration.py, validation.py) is built on these
primitives, so there is exactly one implementation of the probability/information/
estimation formulas backing the methodology section of the dissertation.

A "response" throughout this module is a 4-tuple `(a, b, u, w)`:
  a — item discrimination, b — item difficulty,
  u — observed correctness in [0, 1] (1.0/0.0 for MCQ; a fractional rubric score
      for essay items, treated as a Bernoulli-style expectation — see essay_grader.py),
  w — a case weight in (0, 1], default 1.0. This is a *response-confidence* weight
      (e.g. from AdaptiveTestingEngine's speed-agreement signal), distinct from Warm's
      (1989) weighted-likelihood *bias correction* — see engine.py's docstring on why
      the two aren't the same technique despite the similar name.
"""
import math

# Population prior for Bayesian (EAP) estimation: ability ~ N(0, 1), the standard IRT
# convention absent other information (Baker & Kim, 2004, ch. 4).
PRIOR_MEAN = 0.0
PRIOR_SD = 1.0

# Plausible theta range — both the EAP quadrature bounds and an MLE divergence guard
# (an all-correct/all-incorrect response set has no finite MLE; Newton-Raphson running
# off this range is how that degeneracy is detected — see mle_theta).
THETA_MIN, THETA_MAX = -4.0, 4.0

_MLE_MAX_ITER = 50
_MLE_TOL = 1e-4
_MLE_STEP_CLAMP = 1.0  # per-iteration Newton-Raphson step clamp, guards overshoot near p->0/1
_EAP_GRID_STEP = 0.05  # quadrature resolution over [THETA_MIN, THETA_MAX]


def probability_2pl(theta: float, a: float, b: float) -> float:
    """2PL probability of a correct response: P(theta) = 1 / (1 + e^(-a(theta-b)))."""
    z = a * (theta - b)
    if z > 35:   # overflow guard — probability is already ~1.0 well before this
        return 1.0
    if z < -35:
        return 0.0
    return 1.0 / (1.0 + math.exp(-z))


def item_information(theta: float, a: float, b: float) -> float:
    """Fisher information a single 2PL item carries at theta: I(theta) = a^2 * P * (1-P)."""
    p = probability_2pl(theta, a, b)
    return (a ** 2) * p * (1.0 - p)


def test_information(theta: float, items) -> float:
    """
    Total test information at theta: sum of each item's information. items: iterable
    of (a, b) pairs. Valid under local independence (see apps.scoring.validation) —
    Fisher information is additive across conditionally independent items.
    """
    return sum(item_information(theta, a, b) for a, b in items)


def standard_error(theta: float, items) -> float | None:
    """Asymptotic SE(theta) = 1/sqrt(I(theta)). None where information is ~0 (no signal)."""
    info = test_information(theta, items)
    if info <= 1e-8:
        return None
    return 1.0 / math.sqrt(info)


def reliability(theta: float, items) -> float | None:
    """
    Marginal reliability at theta: rho = 1 - 1/I(theta) (Green, Bock, Humphreys, Linn &
    Reckase, 1984), the CAT-appropriate analogue of Cronbach's alpha — meaningful only
    where information is at least 1; None otherwise so callers don't report a negative
    "reliability".
    """
    info = test_information(theta, items)
    if info < 1.0:
        return None
    return 1.0 - 1.0 / info


def _weighted_log_likelihood_derivatives(theta, responses):
    """
    First and second derivatives of the *weighted* response log-likelihood at theta:
    d1 = sum w*a*(u-P), d2 = sum w*a^2*P*(1-P) — one Newton-Raphson step's numerator/
    denominator. With all w=1 this is the textbook (unweighted) 2PL MLE score/information.
    """
    d1 = 0.0
    d2 = 0.0
    for a, b, u, w in responses:
        p = probability_2pl(theta, a, b)
        d1 += w * a * (u - p)
        d2 += w * (a ** 2) * p * (1.0 - p)
    return d1, d2


def mle_theta(responses, start: float = 0.0):
    """
    Maximum Likelihood estimate of theta via Newton-Raphson on the (weighted) 2PL
    likelihood. Returns None when it doesn't converge to an interior point — this is
    the expected outcome for an all-correct or all-incorrect response set, where the
    likelihood rises monotonically and the true MLE is +/-infinity (Baker & Kim, 2004,
    ch. 3). Callers should fall back to eap_theta in that case; see estimate_theta.
    """
    if not responses:
        return None
    theta = start
    for _ in range(_MLE_MAX_ITER):
        d1, d2 = _weighted_log_likelihood_derivatives(theta, responses)
        if d2 <= 1e-8:
            return None
        step = d1 / d2
        step = max(-_MLE_STEP_CLAMP, min(_MLE_STEP_CLAMP, step))
        theta += step
        if theta <= THETA_MIN or theta >= THETA_MAX:
            return None  # ran off the plausible range: degenerate pattern, use EAP instead
        if abs(step) < _MLE_TOL:
            return theta
    return None  # didn't converge within the iteration budget


def _normal_density(x: float, mean: float, sd: float) -> float:
    z = (x - mean) / sd
    return math.exp(-0.5 * z * z) / (sd * math.sqrt(2 * math.pi))


def eap_theta(responses, prior_mean: float = PRIOR_MEAN, prior_sd: float = PRIOR_SD):
    """
    Expected a Posteriori estimate: posterior mean of theta under an N(prior_mean,
    prior_sd) prior, by numerical (fixed-grid Riemann) quadrature over
    [THETA_MIN, THETA_MAX] — standing in for Gauss-Hermite quadrature since this
    project has no numpy/scipy dependency. Always finite, including for all-correct/
    all-incorrect response sets (the prior regularizes it), which is why the engine
    uses EAP for interim/online ability tracking and only prefers mle_theta once a
    response pattern lets it converge.

    Returns (theta_hat, posterior_sd) — posterior_sd is EAP's own uncertainty (the
    posterior's dispersion), not the MLE asymptotic 1/sqrt(information) formula.
    """
    if not responses:
        return prior_mean, prior_sd

    n_points = int(round((THETA_MAX - THETA_MIN) / _EAP_GRID_STEP)) + 1
    numerator = 0.0
    denominator = 0.0
    second_moment = 0.0
    for i in range(n_points):
        theta = THETA_MIN + i * _EAP_GRID_STEP
        prior = _normal_density(theta, prior_mean, prior_sd)
        likelihood = 1.0
        for a, b, u, w in responses:
            p = probability_2pl(theta, a, b)
            # w as an exponent on the per-response likelihood contribution — a case-weighted
            # (quasi-)likelihood; w=1 reduces to the standard Bernoulli likelihood P^u*(1-P)^(1-u).
            likelihood *= (p ** u * (1.0 - p) ** (1.0 - u)) ** w
        weight = likelihood * prior
        numerator += theta * weight
        denominator += weight
        second_moment += theta * theta * weight

    if denominator <= 1e-300:
        return prior_mean, prior_sd  # numeric underflow (very long response strings): fall back to the prior
    mean = numerator / denominator
    variance = max(0.0, second_moment / denominator - mean * mean)
    return mean, math.sqrt(variance)


def estimate_theta(responses, start: float = 0.0):
    """
    Combined estimator: try MLE first (asymptotically unbiased — the textbook default,
    Lord 1980), fall back to EAP when MLE is undefined or hasn't converged (extreme
    response patterns, or too few responses so far for the likelihood to have an
    interior maximum).

    responses: iterable of (a, b, u, w) — see module docstring.
    Returns (theta, se, method) where method is 'mle' or 'eap', matching
    apps.scoring.models.StudentAbilityEstimate.EstimationMethod.
    """
    if not responses:
        return PRIOR_MEAN, PRIOR_SD, 'eap'

    theta = mle_theta(responses, start=start)
    if theta is not None:
        items = [(a, b) for a, b, _u, _w in responses]
        se = standard_error(theta, items)
        if se is not None:
            return theta, se, 'mle'

    theta, sd = eap_theta(responses)
    return theta, sd, 'eap'
