"""
Pure functions originally ported 1:1 from the mockup's `tierFor()` / `bandFor()`
(MindMetric AI.dc.html lines 681-693); thresholds/copy have since diverged from
that file (3-tier rubric: 0-60/61-80/81-100) and calculators.py is now the
single source of truth server-side.

Each returns a `key` (stable, language-independent — used for bucketing,
e.g. apps.analytics.views.CohortDistributionView) alongside the localized
text for the requested `lang`, so callers that only need to compare bands
(rather than display one) never have to compare translated strings.

Note: apps.scoring.achievements.TIER_THRESHOLDS (bronze/silver/gold badges)
intentionally keeps its own 55/70/85 cutoffs — see that module's docstring.
"""
from .constants import FIELD_WEIGHTS, PROGRAMMING_APTITUDE_WEIGHTS

_TIERS = [
    (81, 'high', {'ru': 'Высокий', 'uz': 'Yuqori'}, '#2E7052', '#DCEFE2'),
    (61, 'developing', {'ru': 'Развивающийся', 'uz': 'Rivojlanayotgan'}, '#B8862F', '#F5E9D3'),
    (0, 'foundational', {'ru': 'Слабый', 'uz': 'Iqtidorsiz'}, '#BD5B4C', '#F6E0DC'),
]

# The degree of aptitude, shown as a secondary line *under* the verdict on the
# results screen (see verdict_for) — so these read as "how much", not "whether".
# The whether/not question is answered once, by APTITUDE_THRESHOLD.
_BANDS = [
    (81, 'high', {'ru': 'Высокий уровень', 'uz': 'Yuqori daraja'}, '#DCEFE2', '#1F4B39'),
    (61, 'developing', {'ru': 'Развивающийся уровень', 'uz': 'Rivojlanayotgan daraja'}, '#F5E9D3', '#B8862F'),
    (0, 'foundational', {'ru': 'Начальный уровень', 'uz': "Boshlang'ich daraja"}, '#F6E0DC', '#BD5B4C'),
]

# The headline the results screen leads with: is this student gifted or not?
# Deliberately its own constant rather than `_BANDS[-2][0]` — the verdict is the
# product's primary claim, so re-cutting the degree bands later must not silently
# move the line between "iqtidorli" and "iqtidorli emas".
APTITUDE_THRESHOLD = 61

# Russian intentionally phrases the verdict about the *finding* ("aptitude was /
# was not identified") rather than labeling the student, which is the register
# institutional reports use there; Uzbek "Iqtidorli"/"Iqtidorli emas" is already
# the idiomatic phrasing for the same claim.
_VERDICTS = {
    True: ({'ru': 'Одарённость выявлена', 'uz': 'Iqtidorli'}, '#DCEFE2', '#1F4B39'),
    False: ({'ru': 'Одарённость не выявлена', 'uz': 'Iqtidorli emas'}, '#F6E0DC', '#BD5B4C'),
}

# {{ distributionBars }} bucket headings — short form of each band, keyed by
# the same stable `key` as _BANDS above.
BAND_SHORT_LABELS = {
    'ru': {'foundational': 'Слабый', 'developing': 'Развивающийся', 'high': 'Высокий'},
    'uz': {'foundational': 'Iqtidorsiz', 'developing': 'Rivojlanayotgan', 'high': 'Yuqori'},
}


def tier_for(score: int, lang: str) -> dict:
    """Per-indicator tier — feeds {{ ind.tier }}/{{ ind.color }} and {{ d.tier }}/{{ d.tierBg }}."""
    for threshold, key, text, color, bg in _TIERS:
        if score >= threshold:
            return {'key': key, 'tier': text[lang], 'color': color, 'bg': bg}
    return {'key': 'foundational', 'tier': _TIERS[-1][2][lang], 'color': _TIERS[-1][3], 'bg': _TIERS[-1][4]}


def band_for(score: int, lang: str) -> dict:
    """Degree of aptitude — feeds {{ band }}/{{ bandBg }}/{{ bandColor }}, the
    secondary line under the verdict on the results screen."""
    for threshold, key, text, bg, color in _BANDS:
        if score >= threshold:
            return {'key': key, 'band': text[lang], 'bg': bg, 'color': color}
    return {'key': 'foundational', 'band': _BANDS[-1][2][lang], 'bg': _BANDS[-1][3], 'color': _BANDS[-1][4]}


def verdict_for(score: int, lang: str) -> dict:
    """Headline gifted/not-gifted call — feeds {{ verdict }} on the results screen.

    `talented` travels alongside the localized text so the frontend can style the
    two outcomes differently without string-matching a translation.
    """
    talented = score >= APTITUDE_THRESHOLD
    text, bg, color = _VERDICTS[talented]
    return {'talented': talented, 'verdict': text[lang], 'bg': bg, 'color': color}


def compute_overall_score(indicator_scores) -> int:
    """indicator_scores: iterable of ints. Mirrors renderVals()'s `overallScore` mean."""
    scores = list(indicator_scores)
    if not scores:
        return 0
    return round(sum(scores) / len(scores))


# Below this many completed indicators (of 10), a field recommendation would be
# based on too thin a slice of the profile to be meaningful — see
# apps.scoring.state_tracker.StudentStateTracker for where this gates the write.
MIN_COMPLETED_INDICATORS = 7

# A field is only included in the ranking once at least this fraction of its
# own weight mass has been completed — otherwise a field whose one heavily-
# weighted indicator is still unattempted could rank on a single lucky score.
MIN_FIELD_WEIGHT_COVERAGE = 0.6


def compute_field_fit(scores_by_key: dict) -> dict:
    """
    scores_by_key: {indicator_key: score} for completed indicators only.

    Returns {'available': bool, 'fields': [{'key', 'score'}, ...]} sorted by
    score descending. `available` is False (and `fields` empty) below
    MIN_COMPLETED_INDICATORS — there's no partial/low-confidence result, only
    an all-or-nothing gate, so the frontend has one boolean to check.
    """
    if len(scores_by_key) < MIN_COMPLETED_INDICATORS:
        return {'available': False, 'fields': []}

    fields = []
    for field_key, weights in FIELD_WEIGHTS.items():
        total_weight = sum(weights.values())
        done_weight = sum(w for k, w in weights.items() if k in scores_by_key)
        if done_weight / total_weight < MIN_FIELD_WEIGHT_COVERAGE:
            continue
        weighted = sum(scores_by_key[k] * w for k, w in weights.items() if k in scores_by_key)
        fields.append({'key': field_key, 'score': round(weighted / done_weight)})

    fields.sort(key=lambda f: -f['score'])
    return {'available': bool(fields), 'fields': fields}


def compute_programming_aptitude(scores_by_key: dict):
    """
    scores_by_key: {indicator_key: score} for completed indicators only.

    Weighted mean over PROGRAMMING_APTITUDE_WEIGHTS, normalized by whatever
    weight is actually completed so far — same "only average what's done"
    principle as compute_overall_score's plain mean. Returns None (not 0)
    when nothing scorable has been completed yet, so callers can tell "no
    data" apart from a genuine floor score.
    """
    done_weight = sum(w for k, w in PROGRAMMING_APTITUDE_WEIGHTS.items() if k in scores_by_key)
    if done_weight == 0:
        return None
    weighted = sum(scores_by_key[k] * w for k, w in PROGRAMMING_APTITUDE_WEIGHTS.items() if k in scores_by_key)
    return round(weighted / done_weight)
