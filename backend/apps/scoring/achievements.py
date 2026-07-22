"""
Badge catalog for the student gamification/achievement system. A badge is
awarded per indicator (see constants.INDICATOR_CHOICES) once its
IndicatorScore crosses a tier threshold — the *same* 55/70/85 cutoffs as
calculators.tier_for, so a badge always lines up with the tier text already
shown on the results/analytics screens, just reframed as bronze/silver/gold
for the gamified collection view (apps.scoring.views.AchievementListView).

Only the highest tier reached per indicator is kept (see models.Achievement's
docstring) — there is no "downgrade" path here, only upgrade-or-nothing.
"""

TIER_THRESHOLDS = [
    (85, 'gold'),
    (70, 'silver'),
    (55, 'bronze'),
]

TIER_ORDER = {'bronze': 1, 'silver': 2, 'gold': 3}

TIER_LABELS = {
    'ru': {'bronze': 'Бронза', 'silver': 'Серебро', 'gold': 'Золото'},
    'uz': {'bronze': 'Bronza', 'silver': 'Kumush', 'gold': 'Oltin'},
}

# Unique, indicator-flavored badge name — distinct from assessmentsMeta.<key>.title
# (the frontend's test-card title) so earning one feels like a reward, not a
# repeated label.
BADGE_NAMES = {
    'ru': {
        'math': 'Мастер чисел',
        'logic': 'Логический ум',
        'algorithmic': 'Архитектор алгоритмов',
        'creative': 'Генератор идей',
        'teamwork': 'Командный игрок',
        'patience': 'Железная выдержка',
        'problem_solving': 'Мастер решений',
        'learning_speed': 'Быстрый ученик',
        'attention': 'Зоркий глаз',
        'iq': 'Вершина интеллекта',
    },
    'uz': {
        'math': 'Sonlar ustasi',
        'logic': 'Mantiq ustasi',
        'algorithmic': 'Algoritm arxitektori',
        'creative': "G'oyalar generatori",
        'teamwork': 'Jamoa yulduzi',
        'patience': 'Temir bardosh',
        'problem_solving': 'Yechim ustasi',
        'learning_speed': "Tezkor o'rganuvchi",
        'attention': "O'tkir nigoh",
        'iq': "Aql cho'qqisi",
    },
}


def tier_for_score(score: int):
    """Highest badge tier `score` qualifies for, or None below the bronze cutoff."""
    for threshold, tier in TIER_THRESHOLDS:
        if score >= threshold:
            return tier
    return None


def badge_name(indicator_key: str, lang: str) -> str:
    return BADGE_NAMES[lang][indicator_key]


def tier_label(tier: str, lang: str) -> str:
    return TIER_LABELS[lang][tier]
