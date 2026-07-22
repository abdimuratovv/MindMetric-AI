"""
Pure functions ported 1:1 from the mockup's `tierFor()` / `bandFor()`
(MindMetric AI.dc.html lines 681-693), so the thresholds and copy the UI
already displays stay the single source of truth server-side too.

Each returns a `key` (stable, language-independent — used for bucketing,
e.g. apps.analytics.views.CohortDistributionView) alongside the localized
text for the requested `lang`, so callers that only need to compare bands
(rather than display one) never have to compare translated strings.
"""
from .constants import FIELD_WEIGHTS, PROGRAMMING_APTITUDE_WEIGHTS

_TIERS = [
    (85, 'exceptional', {'ru': 'Исключительный', 'uz': 'Ajoyib'}, '#2E7052', '#DCEFE2'),
    (70, 'strong', {'ru': 'Сильный', 'uz': 'Kuchli'}, '#4FAE83', '#EAF5EE'),
    (55, 'developing', {'ru': 'Развивающийся', 'uz': 'Rivojlanayotgan'}, '#B8862F', '#F5E9D3'),
    (0, 'foundational', {'ru': 'Начальный', 'uz': "Boshlang'ich"}, '#BD5B4C', '#F6E0DC'),
]

_BANDS = [
    (85, 'exceptional', {'ru': 'Исключительные способности', 'uz': 'Ajoyib qobiliyat'}, '#DCEFE2', '#1F4B39'),
    (70, 'high', {'ru': 'Высокие способности', 'uz': 'Yuqori qobiliyat'}, '#EAF5EE', '#2E7052'),
    (55, 'developing', {'ru': 'Развивающиеся способности', 'uz': 'Rivojlanayotgan qobiliyat'}, '#F5E9D3', '#B8862F'),
    (0, 'foundational', {'ru': 'Начальный уровень способностей', 'uz': "Boshlang'ich qobiliyat"}, '#F6E0DC', '#BD5B4C'),
]

# {{ distributionBars }} bucket headings — short form of each band, keyed by
# the same stable `key` as _BANDS above.
BAND_SHORT_LABELS = {
    'ru': {'foundational': 'Начальный', 'developing': 'Развивающийся', 'high': 'Высокий', 'exceptional': 'Исключительный'},
    'uz': {'foundational': "Boshlang'ich", 'developing': 'Rivojlanayotgan', 'high': 'Yuqori', 'exceptional': 'Ajoyib'},
}


def tier_for(score: int, lang: str) -> dict:
    """Per-indicator tier — feeds {{ ind.tier }}/{{ ind.color }} and {{ d.tier }}/{{ d.tierBg }}."""
    for threshold, key, text, color, bg in _TIERS:
        if score >= threshold:
            return {'key': key, 'tier': text[lang], 'color': color, 'bg': bg}
    return {'key': 'foundational', 'tier': _TIERS[-1][2][lang], 'color': _TIERS[-1][3], 'bg': _TIERS[-1][4]}


def band_for(score: int, lang: str) -> dict:
    """Overall band — feeds {{ band }}/{{ bandBg }}/{{ bandColor }} on the results screen."""
    for threshold, key, text, bg, color in _BANDS:
        if score >= threshold:
            return {'key': key, 'band': text[lang], 'bg': bg, 'color': color}
    return {'key': 'foundational', 'band': _BANDS[-1][2][lang], 'bg': _BANDS[-1][3], 'color': _BANDS[-1][4]}


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
