"""
Shared, model-free constants. Lives outside apps.scoring.models so that
apps.assessments.models (which tags each CognitiveQuestion/BehavioralItem with
the indicator it feeds) can import it without a circular app dependency —
apps.scoring itself depends on apps.assessments, not the other way around.

The 10 keys are the product's indicator set — each maps 1:1 to one of the 10
assessment cards (apps.assessments.models.AssessmentAttempt.Type): 6 MCQ
indicators, 1 coding indicator, 3 self-report (Likert) indicators.
"""

# Internal Django choice labels — used only for admin/DB introspection, never
# returned by an API response (see INDICATOR_LABELS below for the ru/uz text
# actually shown to students/teachers).
INDICATOR_CHOICES = [
    ('math', 'Math Knowledge'),
    ('logic', 'Logical Reasoning'),
    ('algorithmic', 'Algorithmic Thinking'),
    ('creative', 'Creative Thinking'),
    ('teamwork', 'Teamwork'),
    ('patience', 'Patience & Persistence'),
    ('problem_solving', 'Problem Solving'),
    ('learning_speed', 'Learning Speed'),
    ('attention', 'Attention & Accuracy'),
    ('iq', 'IQ Level'),
]

# Full display label per indicator — {{ ind.label }} on the results/analytics screens.
INDICATOR_LABELS = {
    'ru': {
        'math': 'Математические знания',
        'logic': 'Логическое мышление',
        'algorithmic': 'Алгоритмическое мышление',
        'creative': 'Креативное мышление',
        'teamwork': 'Умение работать в команде',
        'patience': 'Терпение и настойчивость',
        'problem_solving': 'Навык решения проблем',
        'learning_speed': 'Скорость обучения',
        'attention': 'Внимательность и точность',
        'iq': 'Уровень IQ',
    },
    'uz': {
        'math': 'Matematik bilimi darajasi',
        'logic': 'Mantiqiy fikrlash',
        'algorithmic': 'Algoritmik fikrlash',
        'creative': 'Kreativ fikrlash',
        'teamwork': 'Jamoada ishlay olish qobiliyati',
        'patience': "Sabr-toqat va qat'iyatlilik",
        'problem_solving': "Muammoni yechish ko'nikmasi",
        'learning_speed': "O'rganish tezligi",
        'attention': 'Diqqat va aniqlik qobiliyati',
        'iq': 'IQ test darajasi',
    },
}

# One-word/short label — {{ tag.label }} on the teacher review's indicator chips.
INDICATOR_SHORT_LABELS = {
    'ru': {
        'math': 'Математика', 'logic': 'Логика', 'algorithmic': 'Алгоритмы', 'creative': 'Креативность',
        'teamwork': 'Команда', 'patience': 'Терпение', 'problem_solving': 'Решение задач',
        'learning_speed': 'Обучаемость', 'attention': 'Внимание', 'iq': 'IQ',
    },
    'uz': {
        'math': 'Matematika', 'logic': 'Mantiq', 'algorithmic': 'Algoritmlar', 'creative': 'Kreativlik',
        'teamwork': 'Jamoaviylik', 'patience': 'Sabr', 'problem_solving': 'Muammo yechish',
        'learning_speed': "O'rganish", 'attention': 'Diqqat', 'iq': 'IQ',
    },
}

# The 6 specialization tracks a student's indicator profile is matched against
# (apps.scoring.calculators.compute_field_fit) — a fixed product taxonomy, not
# user-editable, so plain choices rather than a DB-backed model.
FIELD_CHOICES = [
    ('backend', 'Backend/Algorithms'),
    ('frontend', 'Frontend'),
    ('data_ai', 'Data Science/AI'),
    ('qa', 'QA/Testing'),
    ('team_lead', 'Team Lead/PM'),
    ('devops', 'DevOps/Systems'),
]

FIELD_LABELS = {
    'ru': {
        'backend': 'Backend-разработка / Алгоритмы',
        'frontend': 'Frontend-разработка',
        'data_ai': 'Data Science / AI',
        'qa': 'QA / Тестирование',
        'team_lead': 'Тимлид / Управление проектами',
        'devops': 'DevOps / Системное администрирование',
    },
    'uz': {
        'backend': 'Backend dasturlash / Algoritmlar',
        'frontend': 'Frontend dasturlash',
        'data_ai': 'Data Science / AI',
        'qa': 'QA / Testlash',
        'team_lead': "Jamoa boshqaruvi / Loyiha menejmenti",
        'devops': 'DevOps / Tizim ma\'muriyati',
    },
}

# Per-field indicator weights: only indicators that meaningfully signal fit for
# that field carry a weight; every indicator omitted from a field's dict is an
# implicit 0, not an error — apps.scoring.calculators.compute_field_fit relies
# on this to normalize by the weight actually completed for that field.
FIELD_WEIGHTS = {
    'backend': {'algorithmic': 3, 'logic': 2, 'math': 2, 'problem_solving': 2, 'attention': 1},
    'frontend': {'creative': 3, 'attention': 2, 'algorithmic': 1, 'learning_speed': 1},
    'data_ai': {'math': 3, 'iq': 2, 'logic': 2, 'algorithmic': 1, 'learning_speed': 1},
    'qa': {'attention': 3, 'patience': 2, 'problem_solving': 2, 'algorithmic': 1},
    'team_lead': {'teamwork': 3, 'problem_solving': 2, 'patience': 2, 'learning_speed': 1},
    'devops': {'patience': 3, 'problem_solving': 2, 'attention': 2, 'algorithmic': 1},
}

# Weights for the "programming aptitude" headline score — a second, narrower
# metric alongside OverallScore's plain mean of all 10 indicators. teamwork is
# deliberately absent (a pure collaboration/soft-skill trait, not a signal of
# programming ability itself); creative/patience stay at low weight since they
# still bear on coding practice (design creativity, debugging persistence).
PROGRAMMING_APTITUDE_WEIGHTS = {
    'algorithmic': 3, 'logic': 3, 'math': 2, 'problem_solving': 2, 'iq': 2,
    'learning_speed': 1, 'attention': 1, 'creative': 1, 'patience': 1,
}
