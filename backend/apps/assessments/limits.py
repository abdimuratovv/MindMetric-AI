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
A retake or a fresh start picks up new values; attempts already in progress keep
the time they were started with.
"""

MCQ_KEYS = ('math', 'logic', 'creative', 'problem_solving', 'attention', 'iq')

DEFAULTS = {
    **{key: {'questions': 40, 'minutes': 40} for key in MCQ_KEYS},
    'algorithmic': {'questions': 20, 'codingTasks': 20, 'minutes': 20},
    'teamwork': {'questions': 10},
}

# (min, max) per field.
BOUNDS = {'questions': (5, 100), 'codingTasks': (1, 50), 'minutes': (1, 180)}
BOUNDS_BY_KEY = {'teamwork': {'questions': (1, 30)}}


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
