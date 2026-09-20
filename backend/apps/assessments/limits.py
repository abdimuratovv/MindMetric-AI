"""
Admin-tunable question counts and time limits per indicator. Stored as one JSON
blob on the InstitutionSettings singleton ({indicator: {field: int}}); anything
missing falls back to DEFAULTS, so an untouched install behaves exactly as the
old hard-coded caps did.

Fields per indicator:
  questions    — MCQ questions (MCQ types, algorithmic's MCQ phase) or SJT scenarios (teamwork)
  codingTasks  — algorithmic only: coding tasks in its second phase
  minutes      — hard time limit for the MCQ phase (MCQ types + algorithmic). Teamwork,
                 patience, learning_speed and the coding phase have no total timer.
A retake or a fresh start picks up new values; an attempt already in progress keeps
every number it started with — start_or_restart_attempt freezes the effective config
onto AssessmentAttempt.config_snapshot and `for_attempt` reads it back from there.
"""

MCQ_KEYS = ('math', 'logic', 'creative', 'problem_solving', 'attention', 'iq')

DEFAULTS = {
    **{key: {'questions': 40, 'minutes': 40} for key in MCQ_KEYS},
    'algorithmic': {'questions': 20, 'codingTasks': 20, 'minutes': 20},
    'teamwork': {'questions': 10},
}

# (min, max) per field. The upper bounds are capped by what the banks can actually
# serve: 100 coding tasks (content.CODING_PROBLEMS) and 100 SJT scenarios
# (sjt_content.SJT_SCENARIOS) — both pools can now be scheduled whole. The MCQ
# pools are larger still (200 per indicator, 100 for algorithmic), so 'questions'
# stays at 100 as a sitting-length cap rather than a bank-size one.
BOUNDS = {'questions': (5, 100), 'codingTasks': (1, 100), 'minutes': (1, 180)}
BOUNDS_BY_KEY = {'teamwork': {'questions': (1, 100)}}


def bounds(indicator: str, field: str) -> tuple[int, int]:
    return BOUNDS_BY_KEY.get(indicator, {}).get(field, BOUNDS[field])


def _stored() -> dict:
    from apps.analytics.models import InstitutionSettings
    return InstitutionSettings.load().assessment_config or {}


def get_config(indicator: str) -> dict:
    """Effective settings for one indicator (defaults overlaid with the admin's stored values)."""
    stored = _stored().get(indicator, {})
    return {field: stored.get(field, default) for field, default in DEFAULTS[indicator].items()}


def get_all_config() -> dict:
    stored = _stored()
    return {
        key: {field: stored.get(key, {}).get(field, default) for field, default in fields.items()}
        for key, fields in DEFAULTS.items()
    }


def snapshot(indicator: str) -> dict:
    """The effective config to freeze onto an attempt as it starts. Empty for the
    indicators with nothing tunable (patience, learning_speed), which keeps this safe
    to call for every Type without special-casing the caller."""
    return dict(get_config(indicator)) if indicator in DEFAULTS else {}


def for_attempt(attempt, field: str) -> int:
    """
    One tunable as *this attempt* started with it, not as the admin has it set right
    now. A student partway through 20 coding tasks shouldn't suddenly owe 5 because an
    admin moved the dial underneath them — worse, lowering it below what they'd already
    done used to leave nothing left to serve and no way to finish (see
    views._pick_coding_problem).

    Attempts started before config_snapshot existed carry an empty one and fall back to
    the live setting, exactly as every attempt behaved before.
    """
    snapshot = attempt.config_snapshot or {}
    if field in snapshot:
        return snapshot[field]
    return get_config(attempt.assessment_type)[field]


def mcq_cap(indicator: str) -> int:
    return get_config(indicator)['questions']


def mcq_time_limit_seconds(indicator: str) -> int:
    return get_config(indicator)['minutes'] * 60


def coding_task_cap() -> int:
    return get_config('algorithmic')['codingTasks']


def sjt_scenario_cap() -> int:
    return get_config('teamwork')['questions']


def validate(payload) -> tuple[dict | None, str | None]:
    """Returns (clean {indicator: {field: int}}, None) or (None, error message)."""
    if not isinstance(payload, dict):
        return None, 'assessmentConfig: expected an object'
    clean = {}
    for indicator, fields in payload.items():
        if indicator not in DEFAULTS or not isinstance(fields, dict):
            return None, f'{indicator}: unknown indicator'
        clean[indicator] = {}
        for field, value in fields.items():
            if field not in DEFAULTS[indicator]:
                return None, f'{indicator}.{field}: unknown field'
            low, high = bounds(indicator, field)
            if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
                return None, f'{indicator}.{field}: must be an integer from {low} to {high}'
            clean[indicator][field] = value
    return clean, None
