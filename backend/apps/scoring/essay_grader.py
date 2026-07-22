"""
Heuristic stand-in for AI-graded debate/essay questions.

TODO: replace with a real LLM call. This mirrors the deterministic-stub convention
already established by apps.assessments.views.RunCodingView/SubmitCodingView ("replace
with a real sandboxed JS runner; this stub always passes") — a placeholder that unblocks
the rest of the data flow (question bank, adaptive selection, response storage, indicator
scoring), not real argument analysis.

Scores against the 4-criterion rubric supplied with the source debate-question set:
position (0-2), argument quality (0-3), counter-argument analysis (0-3), conclusion (0-2).
"""

ESSAY_RUBRIC_CRITERIA = [
    {'key': 'position', 'ru': 'Позиция', 'uz': 'Pozitsiya', 'max_points': 2},
    {'key': 'argument_quality', 'ru': 'Качество аргументов', 'uz': 'Argumentlar sifati', 'max_points': 3},
    {'key': 'counter_argument', 'ru': 'Анализ контраргумента', 'uz': "Qarshi argumentni tahlil qilish", 'max_points': 3},
    {'key': 'conclusion', 'ru': 'Заключение и логика', 'uz': 'Xulosa va mantiq', 'max_points': 2},
]
ESSAY_MAX_TOTAL_POINTS = sum(c['max_points'] for c in ESSAY_RUBRIC_CRITERIA)  # 10

# Illustrative RU+UZ keyword lists (a response may be typed in either language) — tunable,
# not exhaustive; a real grader would replace this whole module.
_POSITION_KEYWORDS = [
    'да', 'нет', 'считаю', 'по-моему', 'по моему мнению', 'согласен', 'не согласен', 'я думаю',
    "ha", "yo'q", 'roziman', "rozi emasman", 'fikrimcha', 'menimcha', "deb o'ylayman",
]
_ARGUMENT_MARKERS = [
    'во-первых', 'во-вторых', 'в-третьих', 'потому что', 'так как', 'например', 'поскольку',
    'birinchidan', 'ikkinchidan', 'uchinchidan', 'chunki', 'sababi', 'masalan',
]
_COUNTER_ARGUMENT_CONNECTORS = [
    'но', 'однако', 'тем не менее', 'с другой стороны', 'хотя', 'несмотря на',
    'lekin', 'biroq', 'ammo', "boshqa tomondan", 'garchi',
]
_CONCLUSION_MARKERS = [
    'вывод', 'таким образом', 'следовательно', 'поэтому', 'в итоге', 'в заключение',
    'xulosa', 'demak', 'shuning uchun', 'natijada', 'yakunda',
]


def grade_essay_response(text: str) -> dict:
    normalized = (text or '').strip().lower()
    word_count = len(normalized.split())

    has_stance = any(kw in normalized for kw in _POSITION_KEYWORDS)
    position = 2 if (has_stance and word_count >= 15) else (1 if (has_stance or word_count >= 15) else 0)

    argument_hits = sum(normalized.count(kw) for kw in _ARGUMENT_MARKERS)
    argument_quality = min(3, argument_hits)

    counter_hits = sum(normalized.count(kw) for kw in _COUNTER_ARGUMENT_CONNECTORS)
    counter_argument = 3 if counter_hits >= 2 else (2 if counter_hits == 1 else 0)

    tail = normalized[-max(40, len(normalized) // 5):]
    conclusion = 2 if any(kw in tail for kw in _CONCLUSION_MARKERS) else (
        1 if any(kw in normalized for kw in _CONCLUSION_MARKERS) else 0
    )

    return {
        'position': position, 'argument_quality': argument_quality,
        'counter_argument': counter_argument, 'conclusion': conclusion,
    }


def essay_correctness(rubric_scores: dict) -> float:
    return max(0.0, min(1.0, sum(rubric_scores.values()) / ESSAY_MAX_TOTAL_POINTS))
