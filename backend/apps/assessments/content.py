"""
Seed content — Russian and Uzbek only (the product ships no English; see
apps.i18n).

`key`/`slug` fields are stable, language-independent identifiers used by the
seed command's upsert lookup — upserting on translated text would treat the
Russian and Uzbek version of "the same" question as two different rows.

Shape:
- MCQ_QUESTIONS: dict keyed by one of AssessmentAttempt.MCQ_TYPES' values
  (math/logic/algorithmic/creative/problem_solving/attention/iq), each a list
  of question dicts with `difficulty` (IRT-style, roughly -1..1) for the
  adaptive engine. `algorithmic` (20 questions), `creative` (25 questions),
  and `math` (61 questions) carry larger banks than the rest (5 each),
  sourced from dedicated algorithmic-thinking, creative-thinking, and math
  test sets.
- CODING_PROBLEM: a coding problem, seeded but currently unused — `algorithmic`
  moved from AssessmentAttempt.CODING_TYPES to MCQ_TYPES, so no indicator's
  ASSESSMENT_PATTERN routes to the coding screen anymore. Left in place in
  case a future indicator adopts the coding pattern.
- LIKERT_CATEGORIES: dict keyed by one of AssessmentAttempt.LIKERT_TYPES'
  values (teamwork/patience/learning_speed), each a dict with a display
  label plus a list of Likert statement items (reverse_scored flips the
  1-5 scale before averaging into the indicator — see
  apps.scoring.state_tracker._score_likert).

Load with:  python manage.py seed_assessment_content
"""

MCQ_QUESTIONS = {
    # Sourced from a dedicated "Matematikadan test savollari tizimi" bank (3 difficulty
    # tiers: oson/o'rtacha/murakkab — easy/medium/hard), 61 questions total. Difficulty
    # (b) values are assigned per-tier bands (easy -1.00..-0.05, medium 0.00..0.95,
    # hard 1.00..1.60) rather than derived from real IRT calibration; discrimination (a)
    # is left at CognitiveQuestion's default (1.0, i.e. uncalibrated) for the same reason.
    # See apps.scoring.calibration / the `calibrate_items` management command for how
    # real response data eventually replaces both with JMLE-estimated values.
    'math': [
        # -- Oson (easy) — 20 questions -------------------------------------------------
        {
            'key': 'math-easy-1', 'difficulty': -1.0,
            'category_ru': 'Проценты', 'category_uz': 'Foizlar',
            'prompt_ru': 'Сколько составляет 30% от 150?', 'prompt_uz': '150 ning 30% i nechaga teng?',
            'options_ru': ['25', '30', '45', '50'], 'options_uz': ['25', '30', '45', '50'],
            'correct_indices': [2],
        },
        {
            'key': 'math-easy-2', 'difficulty': -0.95,
            'category_ru': 'Арифметика', 'category_uz': 'Arifmetika',
            'prompt_ru': 'Вычислите: 120∙(65-45)=?', 'prompt_uz': 'Hisoblang: 120∙(65-45)=?',
            'options_ru': ['1500', '2400', '1200', '2100'], 'options_uz': ['1500', '2400', '1200', '2100'],
            'correct_indices': [1],
        },
        {
            'key': 'math-easy-3', 'difficulty': -0.9,
            'category_ru': 'Числовые последовательности', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 2, 5, 11, 23, ?', 'prompt_uz': 'Qatorni davom ettiring: 2, 5, 11, 23, ?',
            'options_ru': ['45', '49', '48', '47'], 'options_uz': ['45', '49', '48', '47'],
            'correct_indices': [3],
        },
        {
            'key': 'math-easy-4', 'difficulty': -0.85,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Если x+1/x=5, найдите x²+1/x².', 'prompt_uz': 'x+1/x=5 boʻlsa, x²+1/x² ni toping.',
            'options_ru': ['21', '23', '25', '27'], 'options_uz': ['21', '23', '25', '27'],
            'correct_indices': [1],
        },
        {
            'key': 'math-easy-5', 'difficulty': -0.8,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Если |a+b|=12 и ab=32, найдите a²+b².',
            'prompt_uz': 'Agar |a+b|=12 va ab=32 boʻlsa, a²+b² ni toping.',
            'options_ru': ['80', '90', '100', '70'], 'options_uz': ['80', '90', '100', '70'],
            'correct_indices': [0],
        },
        {
            'key': 'math-easy-6', 'difficulty': -0.75,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Решите уравнение |x-2|=3. Чему равен x?',
            'prompt_uz': '|x-2|=3 tenglamani yeching. x nechaga teng?',
            'options_ru': ['-2 и 2', '2 и 3', '-1 и 5', '3 и -2'], 'options_uz': ['-2 va 2', '2 va 3', '-1 va 5', '3 va -2'],
            'correct_indices': [2],
        },
        {
            'key': 'math-easy-7', 'difficulty': -0.7,
            'category_ru': 'Теория чисел', 'category_uz': 'Sonlar nazariyasi',
            'prompt_ru': 'Сколько чисел от 1 до 100 кратны 3?', 'prompt_uz': '1 dan 100 gacha nechta son 3 ga karrali?',
            'options_ru': ['32', '33', '34', '35'], 'options_uz': ['32', '33', '34', '35'],
            'correct_indices': [1],
        },
        {
            'key': 'math-easy-8', 'difficulty': -0.65,
            'category_ru': 'Степени', 'category_uz': 'Daraja',
            'prompt_ru': 'Вычислите 4⁵/4³.', 'prompt_uz': '4⁵/4³ ni hisoblang.',
            'options_ru': ['16', '18', '24', '32'], 'options_uz': ['16', '18', '24', '32'],
            'correct_indices': [0],
        },
        {
            'key': 'math-easy-9', 'difficulty': -0.6,
            'category_ru': 'Числовые последовательности', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 7, 15, 31, 63, ?', 'prompt_uz': 'Qatorni davom ettiring: 7, 15, 31, 63, ?',
            'options_ru': ['150', '64', '126', '127'], 'options_uz': ['150', '64', '126', '127'],
            'correct_indices': [3],
        },
        {
            'key': 'math-easy-10', 'difficulty': -0.55,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Если 2x+3y=12 и x=3, чему равен y?', 'prompt_uz': '2x+3y=12 va x=3 boʻlsa, y nechaga teng?',
            'options_ru': ['4', '12', '2', '3'], 'options_uz': ['4', '12', '2', '3'],
            'correct_indices': [2],
        },
        {
            'key': 'math-easy-11', 'difficulty': -0.5,
            'category_ru': 'Арифметика', 'category_uz': 'Arifmetika',
            'prompt_ru': 'Вычислите 1/3+1/6+1/12.', 'prompt_uz': '1/3+1/6+1/12 ni hisoblang.',
            'options_ru': ['5/12', '7/12', '9/12', '11/12'], 'options_uz': ['5/12', '7/12', '9/12', '11/12'],
            'correct_indices': [1],
        },
        {
            'key': 'math-easy-12', 'difficulty': -0.45,
            'category_ru': 'Комбинаторика', 'category_uz': 'Kombinatorika',
            'prompt_ru': 'Чему равно 5!-4!?', 'prompt_uz': '5!-4! nechaga teng?',
            'options_ru': ['120', '100', '96', '5'], 'options_uz': ['120', '100', '96', '5'],
            'correct_indices': [2],
        },
        {
            'key': 'math-easy-13', 'difficulty': -0.4,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Если x³=64, чему равен x?', 'prompt_uz': 'Agar x³=64 boʻlsa, x nechaga teng?',
            'options_ru': ['2', '3', '4', '5'], 'options_uz': ['2', '3', '4', '5'],
            'correct_indices': [2],
        },
        {
            'key': 'math-easy-14', 'difficulty': -0.35,
            'category_ru': 'Числовые последовательности', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 5, 13, 29, 61, ?', 'prompt_uz': 'Qatorni davom ettiring: 5, 13, 29, 61, ?',
            'options_ru': ['125', '84', '122', '73'], 'options_uz': ['125', '84', '122', '73'],
            'correct_indices': [0],
        },
        {
            'key': 'math-easy-15', 'difficulty': -0.3,
            'category_ru': 'Логарифмы', 'category_uz': 'Logarifm',
            'prompt_ru': 'Вычислите log₃81.', 'prompt_uz': 'log₃81 ni hisoblang.',
            'options_ru': ['3', '4', '5', '6'], 'options_uz': ['3', '4', '5', '6'],
            'correct_indices': [1],
        },
        {
            'key': 'math-easy-16', 'difficulty': -0.25,
            'category_ru': 'Теория чисел', 'category_uz': 'Sonlar nazariyasi',
            'prompt_ru': 'Сколько простых чисел не больше 100?', 'prompt_uz': '100 dan katta boʻlmagan tub sonlar nechta?',
            'options_ru': ['23', '24', '25', '26'], 'options_uz': ['23', '24', '25', '26'],
            'correct_indices': [3],
        },
        {
            'key': 'math-easy-17', 'difficulty': -0.2,
            'category_ru': 'Степени', 'category_uz': 'Daraja',
            'prompt_ru': 'Вычислите 3⁰+3¹+3².', 'prompt_uz': '3⁰+3¹+3² ni hisoblang.',
            'options_ru': ['10', '11', '13', '15'], 'options_uz': ['10', '11', '13', '15'],
            'correct_indices': [2],
        },
        {
            'key': 'math-easy-18', 'difficulty': -0.15,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Найдите сумму корней уравнения x²-3x-4=0.',
            'prompt_uz': 'x²-3x-4=0 tenglamaning ildizlari yigʻindisini toping.',
            'options_ru': ['3', '7', '11', '0'], 'options_uz': ['3', '7', '11', '0'],
            'correct_indices': [0],
        },
        {
            'key': 'math-easy-19', 'difficulty': -0.1,
            'category_ru': 'Системы счисления', 'category_uz': 'Sanoq sistemalari',
            'prompt_ru': 'Сколько чисел можно записать с помощью 4 бит?', 'prompt_uz': '4 ta bit bilan nechta son yozish mumkin?',
            'options_ru': ['8', '16', '24', '64'], 'options_uz': ['8', '16', '24', '64'],
            'correct_indices': [1],
        },
        {
            'key': 'math-easy-20', 'difficulty': -0.05,
            'category_ru': 'Проценты', 'category_uz': 'Foizlar',
            'prompt_ru': 'Что больше: 30% от 120 или 25% от 150?', 'prompt_uz': '120 ning 30% i kattami yoki 150 ning 25% i kattami?',
            'options_ru': ['Оба равны', '30% от 120', '25% от 150', 'Сравнить невозможно'],
            'options_uz': ['Ikkalasi teng', '120 ning 30% i', '150 ning 25% i', 'Solishtirib boʻlmaydi'],
            'correct_indices': [2],
        },
        # -- O'rtacha (medium) — 20 questions ---------------------------------------------
        {
            'key': 'math-medium-1', 'difficulty': 0.0,
            'category_ru': 'Комбинаторика', 'category_uz': 'Kombinatorika',
            'prompt_ru': 'Чему равно число перестановок n элементов?',
            'prompt_uz': 'n ta elementning tartiblash (permutatsiya) soni nimaga teng?',
            'options_ru': ['n²', 'n!', '2ⁿ', 'n'], 'options_uz': ['n²', 'n!', '2ⁿ', 'n'],
            'correct_indices': [1],
        },
        {
            'key': 'math-medium-2', 'difficulty': 0.05,
            'category_ru': 'Уравнения со степенями', 'category_uz': 'Daraja tenglamalari',
            'prompt_ru': 'Если 3ⁿ=81, чему равен n?', 'prompt_uz': '3ⁿ=81 boʻlsa, n nechaga teng?',
            'options_ru': ['6', '5', '4', '3'], 'options_uz': ['6', '5', '4', '3'],
            'correct_indices': [2],
        },
        {
            'key': 'math-medium-3', 'difficulty': 0.1,
            'category_ru': 'Комбинаторика', 'category_uz': 'Kombinatorika',
            'prompt_ru': 'Сколькими способами можно выбрать 3 элемента из 10?',
            'prompt_uz': '10 elementdan 3 tasini tanlash nechta yoʻl bilan amalga oshiriladi?',
            'options_ru': ['140', '120', '145', '110'], 'options_uz': ['140', '120', '145', '110'],
            'correct_indices': [1],
        },
        {
            'key': 'math-medium-4', 'difficulty': 0.15,
            'category_ru': 'Теория чисел (НОД)', 'category_uz': 'Sonlar nazariyasi (EKUB)',
            'prompt_ru': 'Найдите наибольший общий делитель (НОД) чисел 24 и 36.',
            'prompt_uz': '24 va 36 ning eng katta umumiy boʻluvchisini (EKUB) toping.',
            'options_ru': ['12', '18', '72', '48'], 'options_uz': ['12', '18', '72', '48'],
            'correct_indices': [0],
        },
        {
            'key': 'math-medium-5', 'difficulty': 0.2,
            'category_ru': 'Теория чисел (НОК)', 'category_uz': 'Sonlar nazariyasi (EKUK)',
            'prompt_ru': 'Найдите наименьшее общее кратное (НОК) чисел 12 и 8.',
            'prompt_uz': '12 va 8 sonlarining eng kichik umumiy karralisini (EKUK) toping.',
            'options_ru': ['4', '8', '12', '24'], 'options_uz': ['4', '8', '12', '24'],
            'correct_indices': [3],
        },
        {
            'key': 'math-medium-6', 'difficulty': 0.25,
            'category_ru': 'Теория чисел', 'category_uz': 'Sonlar nazariyasi',
            'prompt_ru': 'Сколько простых чисел от 1 до 70?', 'prompt_uz': '1 dan 70 gacha boʻlgan tub sonlar nechta?',
            'options_ru': ['16', '17', '18', '19'], 'options_uz': ['16', '17', '18', '19'],
            'correct_indices': [1],
        },
        {
            'key': 'math-medium-7', 'difficulty': 0.3,
            'category_ru': 'Степени', 'category_uz': 'Daraja',
            'prompt_ru': 'Чему равно 4⁴?', 'prompt_uz': '4⁴ nechaga teng?',
            'options_ru': ['16', '64', '128', '256'], 'options_uz': ['16', '64', '128', '256'],
            'correct_indices': [3],
        },
        {
            'key': 'math-medium-8', 'difficulty': 0.35,
            'category_ru': 'Комбинаторика (факториал)', 'category_uz': 'Kombinatorika (faktorial)',
            'prompt_ru': 'Чему равно 6!?', 'prompt_uz': '6! nechaga teng?',
            'options_ru': ['360', '480', '720', '840'], 'options_uz': ['360', '480', '720', '840'],
            'correct_indices': [2],
        },
        {
            'key': 'math-medium-9', 'difficulty': 0.4,
            'category_ru': 'Степени', 'category_uz': 'Daraja',
            'prompt_ru': 'Чему равно 3⁴+4³?', 'prompt_uz': '3⁴+4³ nechaga teng?',
            'options_ru': ['145', '250', '75', '225'], 'options_uz': ['145', '250', '75', '225'],
            'correct_indices': [0],
        },
        {
            'key': 'math-medium-10', 'difficulty': 0.45,
            'category_ru': 'Степени', 'category_uz': 'Daraja',
            'prompt_ru': 'Чему равно 2¹⁰?', 'prompt_uz': '2¹⁰ nechaga teng?',
            'options_ru': ['512', '1024', '2048', '4096'], 'options_uz': ['512', '1024', '2048', '4096'],
            'correct_indices': [1],
        },
        {
            'key': 'math-medium-11', 'difficulty': 0.5,
            'category_ru': 'Степени', 'category_uz': 'Daraja',
            'prompt_ru': 'Чему равно 2⁴∙2⁵?', 'prompt_uz': '2⁴∙2⁵ nechaga teng?',
            'options_ru': ['2²⁰', '2¹⁰', '2¹', '2⁹'], 'options_uz': ['2²⁰', '2¹⁰', '2¹', '2⁹'],
            'correct_indices': [3],
        },
        {
            'key': 'math-medium-12', 'difficulty': 0.55,
            'category_ru': 'Комбинаторика', 'category_uz': 'Kombinatorika',
            'prompt_ru': 'Сколько трёхзначных чисел можно составить из цифр 1, 2, 3?',
            'prompt_uz': '1,2,3 sonlaridan nechta 3 xonali son tuzish mumkin?',
            'options_ru': ['6', '8', '4', '5'], 'options_uz': ['6', '8', '4', '5'],
            'correct_indices': [0],
        },
        {
            'key': 'math-medium-13', 'difficulty': 0.6,
            'category_ru': 'Комбинаторика', 'category_uz': 'Kombinatorika',
            'prompt_ru': 'Сколько двузначных чисел можно составить из цифр 1, 2, 3, 4?',
            'prompt_uz': '1,2,3,4 sonlaridan nechta ikki xonali son tuzish mumkin?',
            'options_ru': ['6', '12', '24', '18'], 'options_uz': ['6', '12', '24', '18'],
            'correct_indices': [1],
        },
        {
            'key': 'math-medium-14', 'difficulty': 0.65,
            'category_ru': 'Теория чисел (остатки)', 'category_uz': 'Sonlar nazariyasi (qoldiqlar)',
            'prompt_ru': (
                'Число при делении на 2 даёт остаток 1, при делении на 3 — остаток 2, при делении '
                'на 4 — остаток 3. Число меньше 50. Чему оно равно?'
            ),
            'prompt_uz': (
                'Bir son 2 ga boʻlinganda 1 qoldiq, 3 ga boʻlinganda 2 qoldiq, 4 ga boʻlinganda 3 '
                'qoldiq beradi. Bu son 50 dan kichik. Bu son nechaga teng?'
            ),
            'options_ru': ['25', '36', '47', '49'], 'options_uz': ['25', '36', '47', '49'],
            'correct_indices': [2],
        },
        {
            'key': 'math-medium-15', 'difficulty': 0.7,
            'category_ru': 'Текстовые задачи', 'category_uz': 'Matnli masalalar',
            'prompt_ru': 'Если число умножить на 5 и прибавить 15, получится 65. Найдите исходное число.',
            'prompt_uz': 'Bir sonni 5 ga koʻpaytirib, 15 qoʻshilsa, 65 chiqadi. Boshlangʻich sonni toping.',
            'options_ru': ['8', '10', '12', '15'], 'options_uz': ['8', '10', '12', '15'],
            'correct_indices': [1],
        },
        {
            'key': 'math-medium-16', 'difficulty': 0.75,
            'category_ru': 'Текстовые задачи', 'category_uz': 'Matnli masalalar',
            'prompt_ru': (
                'В классе меньше 40 учеников. Если их разделить по 4, останется 3 человека; если '
                'по 5 — останется 2 человека. Сколько учеников в классе?'
            ),
            'prompt_uz': (
                'Bir sinfda oʻquvchilar soni 40 dan kam. Ularni 4 tadan ajratsak, 3 kishi ortadi; 5 '
                'tadan ajratsak, 2 kishi ortadi. Sinfda nechta oʻquvchi bor?'
            ),
            'options_ru': ['25', '29', '27', '38'], 'options_uz': ['25', '29', '27', '38'],
            'correct_indices': [2],
        },
        {
            'key': 'math-medium-17', 'difficulty': 0.8,
            'category_ru': 'Геометрия', 'category_uz': 'Geometriya',
            'prompt_ru': 'Длина прямоугольника 12 см, ширина 8 см. Сколько квадратов 4×4 максимум поместится внутри него?',
            'prompt_uz': 'Toʻgʻri toʻrtburchakning uzunligi 12 sm, eni 8 sm. Shu toʻrtburchak ichiga koʻpi bilan nechta 4×4 kvadrat joylashtirish mumkin?',
            'options_ru': ['5', '6', '7', '8'], 'options_uz': ['5', '6', '7', '8'],
            'correct_indices': [1],
        },
        {
            'key': 'math-medium-18', 'difficulty': 0.85,
            'category_ru': 'Геометрия', 'category_uz': 'Geometriya',
            'prompt_ru': 'Сторона квадрата равна 10 см. Чему равно расстояние от точки пересечения диагоналей до вершины?',
            'prompt_uz': 'Bir kvadratning tomoni 10 sm. Diagonallar kesishgan nuqtadan burchaklarigacha boʻlgan masofa nechaga teng?',
            'options_ru': ['5√2', '5', '10√2', '2√5'], 'options_uz': ['5√2', '5', '10√2', '2√5'],
            'correct_indices': [0],
        },
        {
            'key': 'math-medium-19', 'difficulty': 0.9,
            'category_ru': 'Геометрия', 'category_uz': 'Geometriya',
            'prompt_ru': 'Все рёбра куба равны 4 см. Найдите радиус наибольшего шара, вписанного в куб.',
            'prompt_uz': 'Kubning barcha qirralari 4 sm. Kub ichiga sigʻadigan eng katta shar radiusini toping.',
            'options_ru': ['4', '3', '2', '1'], 'options_uz': ['4', '3', '2', '1'],
            'correct_indices': [2],
        },
        {
            'key': 'math-medium-20', 'difficulty': 0.95,
            'category_ru': 'Текстовые задачи (совместная работа)', 'category_uz': 'Matnli masalalar (ish unumdorligi)',
            'prompt_ru': 'Первый рабочий выполняет работу за 6 дней, второй — за 3 дня. За сколько дней они выполнят работу вместе?',
            'prompt_uz': 'Bir ishni 1-ishchi 6 kunda, 2-ishchi esa 3 kunda bajaradi. Ikkalasi birga shu ishni necha kunda bajaradi?',
            'options_ru': ['3', '4', '6', '2'], 'options_uz': ['3', '4', '6', '2'],
            'correct_indices': [3],
        },
        # -- Murakkab (hard) — 21 questions -----------------------------------------------
        {
            'key': 'math-hard-1', 'difficulty': 1.0,
            'category_ru': 'Теория чисел (остатки)', 'category_uz': 'Sonlar nazariyasi (qoldiqlar)',
            'prompt_ru': (
                'Число при делении на 3 даёт остаток 1, при делении на 4 — остаток 2, при делении '
                'на 5 — остаток 3. Найдите наименьшее такое число.'
            ),
            'prompt_uz': (
                'Bir son 3 ga boʻlinganda 1 qoldiq, 4 ga boʻlinganda 2 qoldiq, 5 ga boʻlinganda 3 '
                'qoldiq beradi. Eng kichik shunday sonni toping.'
            ),
            'options_ru': ['55', '58', '59', '60'], 'options_uz': ['55', '58', '59', '60'],
            'correct_indices': [1],
        },
        {
            'key': 'math-hard-2', 'difficulty': 1.03,
            'category_ru': 'Логические задачи', 'category_uz': 'Mantiqiy masalalar',
            'prompt_ru': (
                'В комнате 100 дверей. 1-й человек открывает все двери. 2-й меняет состояние '
                'каждой 2-й двери (открытую закрывает, закрытую открывает). 3-й меняет каждую 3-ю '
                'дверь. Так продолжается до 100-го человека. Сколько дверей останется открытыми в конце?'
            ),
            'prompt_uz': (
                'Bir xonada 100 ta eshik bor. 1-odam barcha eshiklarni ochadi. 2-odam har bir '
                '2-eshikni oʻzgartiradi (ochiqni yopadi, yopiqni ochadi). 3-odam har 3-eshikni '
                'oʻzgartiradi. Shu tarzda 100-odamgacha davom etadi. Oxirida nechta eshik ochiq qoladi?'
            ),
            'options_ru': ['5', '10', '9', '8'], 'options_uz': ['5', '10', '9', '8'],
            'correct_indices': [1],
        },
        {
            'key': 'math-hard-3', 'difficulty': 1.06,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Если к квадрату числа прибавить 6, получится число, в 5 раз большее самого числа. Найдите это число.',
            'prompt_uz': 'Bir sonning kvadratiga 6 qoʻshilsa, shu sonning 5 barobariga teng boʻladi. Sonni toping.',
            'options_ru': ['2 или 3', '1 или 6', '3 или 7', '2 или 8'], 'options_uz': ['2 yoki 3', '1 yoki 6', '3 yoki 7', '2 yoki 8'],
            'correct_indices': [0],
        },
        {
            'key': 'math-hard-4', 'difficulty': 1.09,
            'category_ru': 'Текстовые задачи (совместная работа)', 'category_uz': 'Matnli masalalar (ish unumdorligi)',
            'prompt_ru': 'Работу А выполняет за 10 дней, В — за 15 дней. Они работали вместе 3 дня, затем А ушёл. За сколько дней В закончит оставшуюся работу?',
            'prompt_uz': 'Bir ishni A 10 kunda, B 15 kunda bajaradi. Ular birgalikda 3 kun ishladi, keyin A ketdi. Qolgan ishni B necha kunda tugatadi?',
            'options_ru': ['5', '6', '7', '8'], 'options_uz': ['5', '6', '7', '8'],
            'correct_indices': [2],
        },
        {
            'key': 'math-hard-5', 'difficulty': 1.12,
            'category_ru': 'Числовые последовательности', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 2, 6, 7, 21, 22, 66, ?', 'prompt_uz': 'Qatorni davom ettiring: 2, 6, 7, 21, 22, 66, ?',
            'options_ru': ['67', '68', '132', '198'], 'options_uz': ['67', '68', '132', '198'],
            'correct_indices': [0],
        },
        {
            'key': 'math-hard-6', 'difficulty': 1.15,
            'category_ru': 'Геометрия', 'category_uz': 'Geometriya',
            'prompt_ru': 'Стороны треугольника равны 5 см, 12 см и 13 см. Какой это треугольник?',
            'prompt_uz': 'Uchburchakning uchta tomoni 5 sm, 12 sm va 13 sm. Bu qanday uchburchak?',
            'options_ru': ['Равнобедренный', 'Равносторонний', 'Остроугольный', 'Прямоугольный'],
            'options_uz': ['Teng yonli', 'Teng tomonli', 'Oʻtkir burchakli', 'Toʻgʻri burchakli'],
            'correct_indices': [3],
        },
        {
            'key': 'math-hard-7', 'difficulty': 1.18,
            'category_ru': 'Геометрия', 'category_uz': 'Geometriya',
            'prompt_ru': 'Радиус окружности равен 7 см. Хорда, перпендикулярная диаметру, находится на расстоянии 3 см от центра. Найдите длину хорды.',
            'prompt_uz': 'Aylananing radiusi 7 sm. Diametrga perpendikulyar oʻtkazilgan vatar markazdan 3 sm uzoqlikda joylashgan. Vatar uzunligini toping.',
            'options_ru': ['8', '10', '4√10', '2√40'], 'options_uz': ['8', '10', '4√10', '2√40'],
            'correct_indices': [2],
        },
        {
            'key': 'math-hard-8', 'difficulty': 1.21,
            'category_ru': 'Текстовые задачи', 'category_uz': 'Matnli masalalar',
            'prompt_ru': 'Сумма двух чисел равна 50. Одно из них на 10 больше другого. Найдите большее число.',
            'prompt_uz': 'Ikki sonning yigʻindisi 50. Ulardan biri ikkinchisidan 10 ga katta. Katta sonni toping.',
            'options_ru': ['20', '25', '30', '35'], 'options_uz': ['20', '25', '30', '35'],
            'correct_indices': [2],
        },
        {
            'key': 'math-hard-9', 'difficulty': 1.24,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Сумма половины и трети некоторого числа равна 10. Найдите это число.',
            'prompt_uz': 'Bir sonning yarmi va uchdan birining yigʻindisi 10 ga teng. Sonni toping.',
            'options_ru': ['12', '15', '20', '30'], 'options_uz': ['12', '15', '20', '30'],
            'correct_indices': [0],
        },
        {
            'key': 'math-hard-10', 'difficulty': 1.27,
            'category_ru': 'Текстовые задачи (движение)', 'category_uz': 'Matnli masalalar (harakat)',
            'prompt_ru': 'Поезд едет со скоростью 60 км/ч в течение 2 часов, затем 80 км/ч в течение 1 часа. Найдите среднюю скорость.',
            'prompt_uz': 'Poyezd 60 km/soat tezlik bilan 2 soat, keyin 80 km/soat bilan 1 soat yuradi. Oʻrtacha tezlikni toping.',
            'options_ru': ['65.5 км/ч', '66.6 км/ч', '70.5 км/ч', '75.5 км/ч'],
            'options_uz': ['65.5 km/soat', '66.6 km/soat', '70.5 km/soat', '75.5 km/soat'],
            'correct_indices': [1],
        },
        {
            'key': 'math-hard-11', 'difficulty': 1.3,
            'category_ru': 'Теория вероятностей', 'category_uz': 'Ehtimollar nazariyasi',
            'prompt_ru': 'В коробке красные и синие шары. При выборе любых 3 шаров хотя бы 1 всегда красный. Какое максимальное число синих шаров может быть в коробке?',
            'prompt_uz': 'Bir qutida qizil va koʻk rangli sharlar bor. Agar 3 ta shar olinsa, har doim kamida 1 ta qizil chiqadi. Qutida maksimal nechta koʻk shar boʻlishi mumkin?',
            'options_ru': ['1', '2', '3', '4'], 'options_uz': ['1', '2', '3', '4'],
            'correct_indices': [1],
        },
        {
            'key': 'math-hard-12', 'difficulty': 1.33,
            'category_ru': 'Теория чисел', 'category_uz': 'Sonlar nazariyasi',
            'prompt_ru': 'Число делится на 4 и на 3, но не делится на 5. Какое из чисел подходит?',
            'prompt_uz': 'Bir son 4 ga va 3 ga boʻlinadi, lekin 5 ga boʻlinmaydi. Quyidagilarning qaysi biri mos keladi?',
            'options_ru': ['24', '36', '48', '60'], 'options_uz': ['24', '36', '48', '60'],
            'correct_indices': [2],
        },
        {
            'key': 'math-hard-13', 'difficulty': 1.36,
            'category_ru': 'Алгебра', 'category_uz': 'Algebra',
            'prompt_ru': 'Сумма трёх последовательных чисел равна 72. Найдите наименьшее число.',
            'prompt_uz': 'Uchta ketma-ket sonning yigʻindisi 72 ga teng. Eng kichik sonni toping.',
            'options_ru': ['22', '23', '24', '25'], 'options_uz': ['22', '23', '24', '25'],
            'correct_indices': [1],
        },
        {
            'key': 'math-hard-14', 'difficulty': 1.39,
            'category_ru': 'Тригонометрия', 'category_uz': 'Trigonometriya',
            'prompt_ru': 'Если sinα=3/5 и угол острый, найдите cosα.', 'prompt_uz': 'Agar sinα=3/5 boʻlsa va burchak oʻtkir boʻlsa, cosα ni toping.',
            'options_ru': ['2/5', '1/5', '3/5', '4/5'], 'options_uz': ['2/5', '1/5', '3/5', '4/5'],
            'correct_indices': [3],
        },
        {
            'key': 'math-hard-15', 'difficulty': 1.42,
            'category_ru': 'Геометрия (окружность)', 'category_uz': 'Geometriya (aylana)',
            'prompt_ru': 'Радиус окружности равен 5. Центральный угол равен 60°. Найдите длину дуги.',
            'prompt_uz': 'Aylananing radiusi 5 ga teng. Markaziy burchak 60° boʻlsa, yoy uzunligini toping.',
            'options_ru': ['5π/3', '10π/3', '7π/3', '2π/3'], 'options_uz': ['5π/3', '10π/3', '7π/3', '2π/3'],
            'correct_indices': [0],
        },
        {
            'key': 'math-hard-16', 'difficulty': 1.45,
            'category_ru': 'Геометрия', 'category_uz': 'Geometriya',
            'prompt_ru': 'В равнобедренном треугольнике боковые стороны равны 13, основание равно 10. Найдите высоту, проведённую к основанию.',
            'prompt_uz': 'Teng yonli uchburchakda yon tomonlar 13 ga, asos 10 ga teng. Asosga tushirilgan balandlikni toping.',
            'options_ru': ['16', '13', '12', '11'], 'options_uz': ['16', '13', '12', '11'],
            'correct_indices': [2],
        },
        {
            'key': 'math-hard-17', 'difficulty': 1.48,
            'category_ru': 'Числовые последовательности (функциональные)', 'category_uz': 'Sonli qatorlar (funksional)',
            'prompt_ru': 'Если 2→6, 3→12, 4→20, то 5→?', 'prompt_uz': 'Agar 2→6, 3→12, 4→20 boʻlsa, 5→?',
            'options_ru': ['25', '26', '28', '30'], 'options_uz': ['25', '26', '28', '30'],
            'correct_indices': [3],
        },
        {
            'key': 'math-hard-18', 'difficulty': 1.51,
            'category_ru': 'Комбинаторика', 'category_uz': 'Kombinatorika',
            'prompt_ru': 'Сколькими способами можно выбрать 2 книги из 6 разных книг?',
            'prompt_uz': '6 ta turli kitobdan 2 tasini necha xil usulda tanlash mumkin?',
            'options_ru': ['12', '13', '14', '15'], 'options_uz': ['12', '13', '14', '15'],
            'correct_indices': [3],
        },
        {
            'key': 'math-hard-19', 'difficulty': 1.54,
            'category_ru': 'Комбинаторика', 'category_uz': 'Kombinatorika',
            'prompt_ru': 'Сколько трёхзначных чисел можно составить из цифр 1, 2, 3, 4, 5?',
            'prompt_uz': '1,2,3,4,5 sonlaridan nechta uch xonali son tuzish mumkin?',
            'options_ru': ['60', '50', '40', '30'], 'options_uz': ['60', '50', '40', '30'],
            'correct_indices': [0],
        },
        {
            'key': 'math-hard-20', 'difficulty': 1.57,
            'category_ru': 'Теория вероятностей', 'category_uz': 'Ehtimollar nazariyasi',
            'prompt_ru': 'В коробке 4 чёрных и 6 красных шаров. Найдите вероятность того, что оба случайно выбранных шара окажутся красными.',
            'prompt_uz': 'Qutida 4 ta qora va 6 ta qizil shar bor. Tasodifiy olingan ikkita sharning ikkalasi ham qizil boʻlish ehtimolini toping.',
            'options_ru': ['1/2', '1/3', '1/4', '1/5'], 'options_uz': ['1/2', '1/3', '1/4', '1/5'],
            'correct_indices': [1],
        },
        {
            'key': 'math-hard-21', 'difficulty': 1.6,
            'category_ru': 'Текстовые задачи (совместная работа)', 'category_uz': 'Matnli masalalar (ish unumdorligi)',
            'prompt_ru': 'За 1 час 2 кошки ловят 2 мышей. За сколько часов 4 кошки поймают 4 мышей?',
            'prompt_uz': 'Bir soatda 2 ta mushuk 2 ta sichqonni tutadi. 4 ta mushuk 4 ta sichqonni necha soatda tutadi?',
            'options_ru': ['4', '2', '1', '8'], 'options_uz': ['4', '2', '1', '8'],
            'correct_indices': [2],
        },
    ],
    'logic': [
        # -- Classic single-answer MCQ (16) ---------------------------------------------
        {
            'key': 'logic-books-interesting-1', 'difficulty': -1.0,
            'category_ru': 'Силлогизм', 'category_uz': 'Sillogizm',
            'prompt_ru': 'Все книги полезны. Некоторые книги интересны. Значит:',
            'prompt_uz': "Barcha kitoblar foydali. Ba'zi kitoblar qiziqarli. Demak:",
            'options_ru': ['Все интересные вещи — книги', 'Некоторые полезные вещи интересны', 'Книги бесполезны', 'Ничего из этого не верно'],
            'options_uz': ["Barcha qiziqarli narsalar kitob", "Ba'zi foydali narsalar qiziqarli", 'Kitoblar foydasiz', "Hech biri to'g'ri emas"],
            'correct_indices': [1],
        },
        {
            'key': 'logic-powers-of-2-1', 'difficulty': -0.9,
            'category_ru': 'Числовые ряды', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 1, 2, 4, 8, 16, ?', 'prompt_uz': 'Qatorni davom ettiring: 1, 2, 4, 8, 16, ?',
            'options_ru': ['24', '30', '32', '64'], 'options_uz': ['24', '30', '32', '64'],
            'correct_indices': [2],
        },
        {
            'key': 'logic-fibonacci-1', 'difficulty': 0.3,
            'category_ru': 'Числовые ряды', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 2, 3, 5, 8, 13, ?', 'prompt_uz': 'Qatorni davom ettiring: 2, 3, 5, 8, 13, ?',
            'options_ru': ['18', '20', '21', '22'], 'options_uz': ['18', '20', '21', '22'],
            'correct_indices': [2],
        },
        {
            'key': 'logic-squares-1', 'difficulty': -0.7,
            'category_ru': 'Числовые ряды', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 1, 4, 9, 16, 25, ?', 'prompt_uz': 'Qatorni davom ettiring: 1, 4, 9, 16, 25, ?',
            'options_ru': ['30', '35', '36', '49'], 'options_uz': ['30', '35', '36', '49'],
            'correct_indices': [2],
        },
        {
            'key': 'logic-halving-1', 'difficulty': -0.8,
            'category_ru': 'Числовые ряды', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 128, 64, 32, 16, ?', 'prompt_uz': 'Qatorni davom ettiring: 128, 64, 32, 16, ?',
            'options_ru': ['4', '6', '8', '10'], 'options_uz': ['4', '6', '8', '10'],
            'correct_indices': [2],
        },
        {
            'key': 'logic-doubling-1', 'difficulty': -0.6,
            'category_ru': 'Числовые ряды', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 3, 6, 12, 24, 48, ?', 'prompt_uz': 'Qatorni davom ettiring: 3, 6, 12, 24, 48, ?',
            'options_ru': ['72', '84', '96', '102'], 'options_uz': ['72', '84', '96', '102'],
            'correct_indices': [2],
        },
        {
            'key': 'logic-diff-pattern-1', 'difficulty': 0.5,
            'category_ru': 'Числовые ряды', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 3, 5, 9, 17, 33, ?', 'prompt_uz': 'Qatorni davom ettiring: 3, 5, 9, 17, 33, ?',
            'options_ru': ['45', '65', '55', '66'], 'options_uz': ['45', '65', '55', '66'],
            'correct_indices': [1],
        },
        {
            'key': 'logic-books-paper-1', 'difficulty': 0.6,
            'category_ru': 'Силлогизм', 'category_uz': 'Sillogizm',
            'prompt_ru': (
                'Если все книги являются источниками знаний, а некоторые источники знаний '
                'сделаны из бумаги, какое из следующих утверждений абсолютно верно?'
            ),
            'prompt_uz': (
                "Agar barcha kitoblar bilim manbai bo'lsa, va ba'zi bilim manbalari qog'ozdan "
                "tayyorlangan bo'lsa, quyidagilarning qaysi biri mutloq to'g'ri bo'ladi?"
            ),
            'options_ru': [
                'Все книги сделаны из бумаги.', 'Некоторые книги могут быть сделаны из бумаги.',
                'Всё, что сделано из бумаги, — книга.', 'Книги и источники знаний — совершенно разные вещи.',
            ],
            'options_uz': [
                "Barcha kitoblar qog'ozdan tayyorlangan.", "Ba'zi kitoblar qog'ozdan tayyorlangan bo'lishi mumkin.",
                "Qog'ozdan tayyorlangan har bir narsa kitobdir.", 'Kitoblar va bilim manbalari umuman boshqa narsalar.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'logic-antonym-1', 'difficulty': -0.5,
            'category_ru': 'Вербальные аналогии', 'category_uz': "Og'zaki analogiyalar",
            'prompt_ru': (
                'Найдите соответствие в логической цепочке: отношение слова «Большой» к слову '
                '«Маленький» такое же, как отношение слова «Старый» к какому слову?'
            ),
            'prompt_uz': (
                'Mantiqiy zanjirdagi moslikni toping: "Katta" so\'zining "Kichik" so\'ziga nisbati, '
                '"Eski" so\'zining qaysi so\'zga nisbatiga teng?'
            ),
            'options_ru': ['Древний', 'Новый', 'Исторический', 'Красивый'],
            'options_uz': ['Qadimiy', 'Yangi', 'Tarixiy', 'Chiroyli'],
            'correct_indices': [1],
        },
        {
            'key': 'logic-family-1', 'difficulty': 0.8,
            'category_ru': 'Семейная логика', 'category_uz': 'Oilaviy mantiq',
            'prompt_ru': (
                'Информация о членах семьи: Акмаль — сын Карима. Карим — старший брат Сардора. '
                'Сардор — отец Джамшида. Кем приходится Джамшид Акмалю?'
            ),
            'prompt_uz': (
                "Oila a'zolari haqida ma'lumot: Akmal Karimning o'g'li. Karim esa Sardorning akasi. "
                "Sardor Jamshidning otasi. Jamshid Akmalga kim bo'ladi?"
            ),
            'options_ru': ['Дядя', 'Племянник', 'Двоюродный брат', 'Старший брат'],
            'options_uz': ['Amaki', 'Jiyan', 'Amakivachcha', 'Aka'],
            'correct_indices': [2],
        },
        {
            'key': 'logic-race-position-1', 'difficulty': -0.3,
            'category_ru': 'Логическая головоломка', 'category_uz': 'Mantiqiy topishmoq',
            'prompt_ru': 'На забеге вы обогнали спортсмена, который был на 2-м месте. На каком месте вы сейчас?',
            'prompt_uz': "Bir yugurish musobaqasida siz ikkinchi o'rindagi sportchini quvib o'tdingiz. Hozir siz nechanchi o'rindasiz?",
            'options_ru': ['Первое', 'Второе', 'Третье', 'Последнее'],
            'options_uz': ['Birinchi', 'Ikkinchi', 'Uchinchi', 'Oxirgi'],
            'correct_indices': [1],
        },
        {
            'key': 'logic-word-relation-1', 'difficulty': -0.4,
            'category_ru': 'Вербальные аналогии', 'category_uz': "Og'zaki analogiyalar",
            'prompt_ru': 'Определите логическую связь между словами: если ЗДАНИЕ → КИРПИЧ, то ТКАНЬ → ?',
            'prompt_uz': "So'zlar o'rtasidagi mantiqiy bog'liqlikni aniqlang: Agar BINO -> G'ISHT bo'lsa, MATO -> ?",
            'options_ru': ['Одежда', 'Нить', 'Портной', 'Ножницы'],
            'options_uz': ['Kiyim', 'Ip', 'Tikuvchi', 'Qaychi'],
            'correct_indices': [1],
        },
        {
            'key': 'logic-siblings-1', 'difficulty': 0.2,
            'category_ru': 'Логическая головоломка', 'category_uz': 'Mantiqiy topishmoq',
            'prompt_ru': 'У Акмаля 4 дочери. У каждой из них есть один и тот же старший брат. Сколько всего детей у Акмаля?',
            'prompt_uz': "Akmalning 4 ta qizi bor. Ularning har birining bittadan akasi bor. Akmalning jami nechta farzandi bor?",
            'options_ru': ['8', '5', '4', '7'], 'options_uz': ['8 ta', '5 ta', '4 ta', '7 ta'],
            'correct_indices': [1],
        },
        {
            'key': 'logic-contrapositive-1', 'difficulty': 0.9,
            'category_ru': 'Формальная логика', 'category_uz': 'Formal mantiq',
            'prompt_ru': 'Какое из следующих утверждений всегда логически верно? «Если идёт дождь, улицы становятся мокрыми.»',
            'prompt_uz': 'Quyidagi mulohazalardan qaysi biri har doim mantiqan to\'g\'ri? "Agar yomg\'ir yog\'sa, ko\'chalar nam bo\'ladi."',
            'options_ru': [
                'Если улицы мокрые, значит, шёл дождь.', 'Если дождь не шёл, улицы не мокрые.',
                'Если улицы не мокрые, значит, дождя не было.', 'Дождь идёт только для того, чтобы намочить улицы.',
            ],
            'options_uz': [
                "Agar ko'chalar nam bo'lsa, demak yomg'ir yog'gan.", "Agar yomg'ir yog'magan bo'lsa, ko'chalar nam emas.",
                "Agar ko'chalar nam bo'lmasa, demak yomg'ir yog'magan.", "Yomg'ir faqat ko'chalarni namlash uchun yog'adi.",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'logic-clock-hands-1', 'difficulty': 0.7,
            'category_ru': 'Логическая головоломка', 'category_uz': 'Mantiqiy topishmoq',
            'prompt_ru': 'Сколько раз в сутки (за 24 часа) стрелки часов накладываются друг на друга (угол 0 градусов)?',
            'prompt_uz': "Soat millari bir sutkada (24 soatda) necha marta ustma-ust (0 daraja burchak ostida) keladi?",
            'options_ru': ['24 раза', '22 раза', '12 раз', '20 раз'], 'options_uz': ['24 marta', '22 marta', '12 marta', '20 marta'],
            'correct_indices': [1],
        },
        {
            'key': 'logic-letter-pattern-1', 'difficulty': 1.0,
            'category_ru': 'Буквенные закономерности', 'category_uz': 'Harf qonuniyatlari',
            'prompt_ru': 'Определите закономерность и найдите букву вместо знака вопроса (?): A, D, H, M, ?',
            'prompt_uz': "Qonuniyatni aniqlang va so'roq belgisi (?) o'rnidagi harfni toping: A, D, H, M, ?",
            'options_ru': ['O', 'P', 'R', 'S'], 'options_uz': ['O', 'P', 'R', 'S'],
            'correct_indices': [3],
        },
        # -- Multi-select scenarios (10) -------------------------------------------------
        {
            'key': 'logic-multi-load-balancing-1', 'difficulty': 0.1, 'question_type': 'multi',
            'category_ru': 'Системная архитектура', 'category_uz': 'Tizim arxitekturasi',
            'prompt_ru': 'Из-за большого количества пользователей онлайн-платформа обучения работает медленно. Какие решения полезны?',
            'prompt_uz': "Online ta'lim platformasiga juda ko'p foydalanuvchi kirgani sababli tizim sekin ishlamoqda. Qaysi yechimlar foydali?",
            'options_ru': ['Использовать Load balancing', 'Применить Cache', 'Database indexing', 'Удалить все изображения', 'Увеличить ресурсы сервера'],
            'options_uz': ["Load balancing ishlatish", "Cache qo'llash", 'Database indexing', "Barcha rasmlarni o'chirish", 'Server resurslarini oshirish'],
            'correct_indices': [0, 1, 2, 4],
        },
        {
            'key': 'logic-multi-query-optimization-1', 'difficulty': 0.2, 'question_type': 'multi',
            'category_ru': 'Оптимизация баз данных', 'category_uz': "Ma'lumotlar bazasini optimallashtirish",
            'prompt_ru': 'Запрос к базе данных выполняется очень медленно. Какие методы помогут?',
            'prompt_uz': "Database query juda sekin ishlamoqda. Qaysi usullar yordam beradi?",
            'options_ru': ['Создать индекс', 'Query optimization', 'Normalization', 'Уменьшить HTML-код', 'Использовать Pagination'],
            'options_uz': ["Index yaratish", 'Query optimization', 'Normalization', "HTML kodni kamaytirish", "Pagination ishlatish"],
            'correct_indices': [0, 1, 2, 4],
        },
        {
            'key': 'logic-multi-api-security-1', 'difficulty': 0.3, 'question_type': 'multi',
            'category_ru': 'Кибербезопасность', 'category_uz': 'Kiberxavfsizlik',
            'prompt_ru': 'К API поступают запросы от неизвестных пользователей. Какие меры повышают безопасность?',
            'prompt_uz': "API ga noma'lum foydalanuvchilar request yubormoqda. Qaysi choralar xavfsizlikni oshiradi?",
            'options_ru': ['JWT authentication', 'Использовать HTTPS', 'Rate limiting', 'API key validation', 'Сделать админ-панель публичной'],
            'options_uz': ['JWT authentication', "HTTPS ishlatish", 'Rate limiting', 'API key validation', "Admin panelni public qilish"],
            'correct_indices': [0, 1, 2, 3],
        },
        {
            'key': 'logic-multi-code-quality-1', 'difficulty': -0.1, 'question_type': 'multi',
            'category_ru': 'Качество кода', 'category_uz': 'Kod sifati',
            'prompt_ru': 'Код проекта стал очень беспорядочным и непонятным. Какие подходы полезны?',
            'prompt_uz': "Loyiha kodi juda tartibsiz va tushunarsiz bo'lib ketgan. Qaysi yondashuvlar foydali?",
            'options_ru': ['Refactoring', 'Coding standards', 'Code review', 'Писать весь код в одном файле', 'Написать документацию'],
            'options_uz': ['Refactoring', 'Coding standards', 'Code review', "Hamma kodni bitta faylda yozish", 'Documentation yozish'],
            'correct_indices': [0, 1, 2, 4],
        },
        {
            'key': 'logic-multi-web-performance-1', 'difficulty': 0.0, 'question_type': 'multi',
            'category_ru': 'Производительность веб', 'category_uz': 'Veb unumdorligi',
            'prompt_ru': 'Веб-сайт загружается очень медленно. Какие методы повышают производительность?',
            'prompt_uz': "Web sayt juda sekin yuklanmoqda. Qaysi usullar performance'ni oshiradi?",
            'options_ru': ['Использовать CDN', 'Image compression', 'Lazy loading', 'Использовать Cache', 'Добавить лишние анимации'],
            'options_uz': ["CDN ishlatish", 'Image compression', 'Lazy loading', "Cache ishlatish", "Keraksiz animatsiyalar qo'shish"],
            'correct_indices': [0, 1, 2, 3],
        },
        {
            'key': 'logic-multi-debugging-1', 'difficulty': 0.4, 'question_type': 'multi',
            'category_ru': 'Отладка', 'category_uz': 'Debagging',
            'prompt_ru': 'Программа иногда работает, а иногда выдаёт ошибку. Что нужно сделать, чтобы найти проблему?',
            'prompt_uz': "Dastur ba'zan ishlaydi, ba'zan error beradi. Muammoni topish uchun nima qilish kerak?",
            'options_ru': ['Проверить логи', 'Написать тесты', 'Мониторинг', 'Reproduce (воспроизвести)', 'Полностью удалить код'],
            'options_uz': ["Loglarni tekshirish", 'Test yozish', 'Monitoring qilish', 'Reproduce qilish', "Kodni to'liq o'chirib tashlash"],
            'correct_indices': [0, 1, 2, 3],
        },
        {
            'key': 'logic-multi-git-collab-1', 'difficulty': -0.2, 'question_type': 'multi',
            'category_ru': 'Командная разработка', 'category_uz': 'Jamoaviy dasturlash',
            'prompt_ru': 'Несколько программистов работают над одним проектом. Какие методы полезны?',
            'prompt_uz': "Bir nechta dasturchi bitta project ustida ishlamoqda. Qaysi usullar foydali?",
            'options_ru': ['Branch strategy', 'Pull request', 'Git workflow', 'Отправлять код через Telegram', 'Merge review'],
            'options_uz': ['Branch strategy', 'Pull request', 'Git workflow', "Kodni Telegram orqali yuborish", 'Merge review'],
            'correct_indices': [0, 1, 2, 4],
        },
        {
            'key': 'logic-multi-battery-drain-1', 'difficulty': 0.5, 'question_type': 'multi',
            'category_ru': 'Мобильная разработка', 'category_uz': 'Mobil dasturlash',
            'prompt_ru': 'Мобильное приложение очень быстро разряжает батарею телефона. Какие факторы могут быть причиной?',
            'prompt_uz': "Mobil ilova telefon battery'ni juda tez tugatmoqda. Qaysi omillar bunga sabab bo'lishi mumkin?",
            'options_ru': ['Infinite loop', 'Background service', 'Excessive API request', 'Memory leak', 'Тёмная тема (Dark mode)'],
            'options_uz': ['Infinite loop', 'Background service', 'Excessive API request', 'Memory leak', 'Dark mode'],
            'correct_indices': [0, 1, 2, 3],
        },
        {
            'key': 'logic-multi-data-privacy-1', 'difficulty': 0.15, 'question_type': 'multi',
            'category_ru': 'Этика ИИ', 'category_uz': 'AI etikasi',
            'prompt_ru': 'Система ИИ собирает данные пользователей. Какие принципы важны?',
            'prompt_uz': "AI tizimi foydalanuvchi ma'lumotlarini yig'moqda. Qaysi prinsiplar muhim?",
            'options_ru': ['Privacy', 'User consent', 'Data encryption', 'Transparency', 'Хранить все данные бесконечно'],
            'options_uz': ['Privacy', 'User consent', 'Data encryption', 'Transparency', "Barcha ma'lumotni cheksiz saqlash"],
            'correct_indices': [0, 1, 2, 3],
        },
        {
            'key': 'logic-multi-search-scale-1', 'difficulty': 0.35, 'question_type': 'multi',
            'category_ru': 'Алгоритмы поиска', 'category_uz': 'Qidiruv algoritmlari',
            'prompt_ru': 'Нужно быстро выполнить поиск среди 10 миллионов записей. Какие методы эффективны?',
            'prompt_uz': "10 millionta yozuv ichidan tez qidiruv qilish kerak. Qaysi usullar samarali?",
            'options_ru': ['Binary search', 'Database indexing', 'Hash table', 'Caching', 'Каждый раз использовать linear search'],
            'options_uz': ['Binary search', 'Database indexing', 'Hash table', 'Caching', "Har safar linear search ishlatish"],
            'correct_indices': [0, 1, 2, 3],
        },
        # -- Step-ordering scenarios (10, folded into single-answer: options are full
        # orderings, 3 distractor permutations invented since the source only supplies the
        # one correct order — same pattern already used for algorithmic-sequence-1 above) --
        {
            'key': 'logic-order-website-slow-1', 'difficulty': 0.0,
            'category_ru': 'Диагностика процессов', 'category_uz': 'Jarayonlarni diagnostika qilish',
            'prompt_ru': (
                'Web-сайт внезапно стал медленным. Расставьте следующие этапы в правильном порядке: '
                'A) Проверить логи. B) Воспроизвести проблему. C) Мониторить ресурсы сервера. D) Применить решение.'
            ),
            'prompt_uz': (
                "Web sayt birdan sekinlashdi. Quyidagi bosqichlarni to'g'ri tartiblang: A) Loglarni tekshirish. "
                "B) Muammoni reproduksiya qilish. C) Server resurslarini monitoring qilish. D) Yechimni qo'llash."
            ),
            'options_ru': ['B → C → A → D', 'A → B → C → D', 'D → A → C → B', 'C → B → D → A'],
            'options_uz': ['B → C → A → D', 'A → B → C → D', 'D → A → C → B', 'C → B → D → A'],
            'correct_indices': [0],
        },
        {
            'key': 'logic-order-crash-debug-1', 'difficulty': 0.1,
            'category_ru': 'Диагностика процессов', 'category_uz': 'Jarayonlarni diagnostika qilish',
            'prompt_ru': (
                'Программа иногда работает, а иногда падает (crash). Расставьте этапы по порядку: '
                'A) Написать тест-кейс. B) Воспроизвести ошибку. C) Проанализировать логи. D) Исправить (fix).'
            ),
            'prompt_uz': (
                "Dastur ba'zan ishlaydi, ba'zan crash bo'ladi. Bosqichlarni tartiblang: A) Test case yozish. "
                "B) Xatoni qayta hosil qilish. C) Loglarni tahlil qilish. D) Fix qilish."
            ),
            'options_ru': ['A → B → C → D', 'D → A → C → B', 'C → B → D → A', 'B → C → A → D'],
            'options_uz': ['A → B → C → D', 'D → A → C → B', 'C → B → D → A', 'B → C → A → D'],
            'correct_indices': [3],
        },
        {
            'key': 'logic-order-app-dev-1', 'difficulty': -0.3,
            'category_ru': 'Жизненный цикл разработки', 'category_uz': 'Dasturlash hayot sikli',
            'prompt_ru': (
                'Вы хотите создать новое мобильное приложение. Расставьте этапы по порядку: '
                'A) Определить требования. B) Спроектировать дизайн (UI/UX). C) Написать код. D) Тестирование.'
            ),
            'prompt_uz': (
                "Yangi mobil ilova yaratmoqchisiz. Bosqichlarni tartiblang: A) Talablarni aniqlash. "
                "B) Dizayn qilish (UI/UX). C) Kod yozish. D) Testing."
            ),
            'options_ru': ['B → A → C → D', 'A → B → C → D', 'A → C → B → D', 'D → C → B → A'],
            'options_uz': ['B → A → C → D', 'A → B → C → D', 'A → C → B → D', 'D → C → B → A'],
            'correct_indices': [1],
        },
        {
            'key': 'logic-order-query-slow-1', 'difficulty': 0.4,
            'category_ru': 'Диагностика процессов', 'category_uz': 'Jarayonlarni diagnostika qilish',
            'prompt_ru': (
                'Запрос (query) работает очень медленно. Расставьте этапы по порядку: '
                'A) Проанализировать запрос. B) Добавить индекс. C) Проверить производительность. D) Оптимизировать.'
            ),
            'prompt_uz': (
                "Query juda sekin ishlamoqda. Bosqichlarni tartiblang: A) Queryni analiz qilish. "
                "B) Index qo'shish. C) Performance tekshirish. D) Optimallashtirish."
            ),
            'options_ru': ['A → B → C → D', 'C → B → D → A', 'A → D → B → C', 'B → A → D → C'],
            'options_uz': ['A → B → C → D', 'C → B → D → A', 'A → D → B → C', 'B → A → D → C'],
            'correct_indices': [2],
        },
        {
            'key': 'logic-order-debate-prep-1', 'difficulty': 0.2,
            'category_ru': 'Аргументация', 'category_uz': 'Argumentatsiya',
            'prompt_ru': (
                'Дебаты на тему «ИИ заменит людей». Расставьте этапы по порядку: A) Проанализировать '
                'контраргументы. B) Сформировать своё мнение. C) Собрать доводы. D) Сделать вывод.'
            ),
            'prompt_uz': (
                '"AI insonlarni almashtiradi" mavzusida debat. Bosqichlarni tartiblang: A) Qarshi argumentlarni '
                "tahlil qilish. B) O'z fikrini shakllantirish. C) Dalillarni yig'ish. D) Xulosa qilish."
            ),
            'options_ru': ['B → C → A → D', 'A → B → C → D', 'D → A → C → B', 'C → B → D → A'],
            'options_uz': ['B → C → A → D', 'A → B → C → D', 'D → A → C → B', 'C → B → D → A'],
            'correct_indices': [0],
        },
        {
            'key': 'logic-order-security-incident-1', 'difficulty': 0.5,
            'category_ru': 'Реагирование на инциденты', 'category_uz': 'Insidentga javob berish',
            'prompt_ru': (
                'Обнаружены несанкционированные входы в систему. Расставьте этапы по порядку: '
                'A) Определить источник угрозы. B) Проверить логи. C) Применить меры защиты. D) Настроить мониторинг.'
            ),
            'prompt_uz': (
                "Tizimga ruxsatsiz kirishlar aniqlandi. Bosqichlarni tartiblang: A) Xavf manbasini aniqlash. "
                "B) Loglarni tekshirish. C) Himoya choralarini qo'llash. D) Monitoring o'rnatish."
            ),
            'options_ru': ['A → B → C → D', 'D → C → A → B', 'C → D → A → B', 'B → A → C → D'],
            'options_uz': ['A → B → C → D', 'D → C → A → B', 'C → D → A → B', 'B → A → C → D'],
            'correct_indices': [3],
        },
        {
            'key': 'logic-order-problem-solving-1', 'difficulty': -0.2,
            'category_ru': 'Решение задач', 'category_uz': 'Muammo yechish',
            'prompt_ru': (
                'Нужно решить сложную задачу. Расставьте этапы по порядку: A) Проанализировать данные. '
                'B) Выбрать формулу. C) Произвести вычисления. D) Проверить результат.'
            ),
            'prompt_uz': (
                "Murakkab masalani yechish kerak. Bosqichlarni tartiblang: A) Ma'lumotlarni tahlil qilish. "
                "B) Formula tanlash. C) Hisoblash. D) Natijani tekshirish."
            ),
            'options_ru': ['B → A → C → D', 'A → B → C → D', 'A → C → B → D', 'D → C → B → A'],
            'options_uz': ['B → A → C → D', 'A → B → C → D', 'A → C → B → D', 'D → C → B → A'],
            'correct_indices': [1],
        },
        {
            'key': 'logic-order-team-project-1', 'difficulty': -0.4,
            'category_ru': 'Управление проектом', 'category_uz': 'Loyihani boshqarish',
            'prompt_ru': (
                'Командный проект идёт беспорядочно. Расставьте этапы по порядку: A) Распределить роли. '
                'B) Назначить задачи. C) Мониторить прогресс. D) Итоговый обзор (review).'
            ),
            'prompt_uz': (
                "Jamoa loyihasi tartibsiz ketmoqda. Bosqichlarni tartiblang: A) Rollarni taqsimlash. "
                "B) Vazifalarni belgilash. C) Progressni monitoring qilish. D) Yakuniy review."
            ),
            'options_ru': ['B → A → D → C', 'A → C → B → D', 'A → B → C → D', 'D → C → B → A'],
            'options_uz': ['B → A → D → C', 'A → C → B → D', 'A → B → C → D', 'D → C → B → A'],
            'correct_indices': [2],
        },
        {
            'key': 'logic-order-profiling-1', 'difficulty': 0.3,
            'category_ru': 'Диагностика процессов', 'category_uz': 'Jarayonlarni diagnostika qilish',
            'prompt_ru': (
                'Веб-приложение работает очень медленно. Расставьте этапы по порядку: A) Найти узкое место '
                '(bottleneck). B) Провести профилирование (profiling). C) Оптимизировать. D) Проверить результат.'
            ),
            'prompt_uz': (
                "Web ilova juda sekin ishlamoqda. Bosqichlarni tartiblang: A) Bottleneckni topish. "
                "B) Profiling qilish. C) Optimallashtirish. D) Natijani tekshirish."
            ),
            'options_ru': ['B → A → C → D', 'A → B → C → D', 'D → C → A → B', 'C → D → B → A'],
            'options_uz': ['B → A → C → D', 'A → B → C → D', 'D → C → A → B', 'C → D → B → A'],
            'correct_indices': [0],
        },
        {
            'key': 'logic-order-time-management-1', 'difficulty': -0.1,
            'category_ru': 'Тайм-менеджмент', 'category_uz': 'Vaqtni boshqarish',
            'prompt_ru': (
                'Студенту нужно одновременно готовиться к экзамену и работать. Расставьте этапы по порядку: '
                'A) Определить приоритеты. B) Составить расписание. C) Распределить задачи. D) Оценить результат.'
            ),
            'prompt_uz': (
                "Talaba imtihon va ishni bir vaqtda boshqarishi kerak. Bosqichlarni tartiblang: "
                "A) Prioritetlarni aniqlash. B) Vaqt jadvali tuzish. C) Vazifalarni bo'lish. D) Natijani baholash."
            ),
            'options_ru': ['B → A → C → D', 'A → C → D → B', 'D → C → B → A', 'A → B → C → D'],
            'options_uz': ['B → A → C → D', 'A → C → D → B', 'D → C → B → A', 'A → B → C → D'],
            'correct_indices': [3],
        },
        # -- Essay / debate questions (10, AI-graded via apps.scoring.essay_grader) -------
        {
            'key': 'logic-essay-ai-jobs-1', 'difficulty': 0.5, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                '«Искусственный интеллект уничтожит множество рабочих мест» — согласны ли вы с этим мнением? '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Sun'iy intellekt ko'plab ish o'rinlarini yo'q qiladi\" degan fikrga qo'shilasizmi? "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-online-education-1', 'difficulty': 0.4, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                'Как вы оцениваете утверждение «Онлайн-образование эффективнее традиционного»? '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Online ta'lim an'anaviy ta'limdan samaraliroq\" degan fikrni qanday baholaysiz? "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-smartphones-1', 'difficulty': 0.3, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                'Ваше отношение к мнению «Смартфоны снижают эффективность учёбы студентов»? '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Smartfonlar talabalar o'qish samaradorligini pasaytiradi\" fikriga munosabatingiz? "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-python-vs-cpp-1', 'difficulty': 0.6, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                'Оцените утверждение «Python лучше C++ для начинающих». '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Yangi boshlovchilar uchun Python C++ dan yaxshiroq\" fikrini baholang. "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-homework-1', 'difficulty': 0.35, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                '«Домашние задания задавать не нужно» — согласны ли вы с этим мнением? '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Uy vazifasi berish kerak emas\" degan fikrga qo'shilasizmi? "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-future-programmers-1', 'difficulty': 0.7, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                'Проанализируйте утверждение «В будущем программисты не понадобятся». '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Kelajakda dasturchilar kerak bo'lmaydi\" fikrini tahlil qiling. "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-social-media-1', 'difficulty': 0.45, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                'Ваше отношение к мнению «Социальные сети вредят обществу»? '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Ijtimoiy tarmoqlar jamiyatga zarar keltiradi\" fikriga munosabatingiz? "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-programmer-salary-1', 'difficulty': 0.55, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                '«Программисты получают слишком высокую зарплату — справедливо ли это?» '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                '"Dasturchilar juda yuqori maosh oladi, bu adolatlimi?" '
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-technology-life-1', 'difficulty': 0.5, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                'Оцените утверждение «Технологии только улучшают жизнь человека». '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Texnologiya inson hayotini faqat yaxshilaydi\" fikrini baholang. "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
        {
            'key': 'logic-essay-it-education-1', 'difficulty': 0.65, 'question_type': 'essay',
            'category_ru': 'Дебаты и аргументация', 'category_uz': 'Debat va argumentatsiya',
            'prompt_ru': (
                '«В будущем всё образование будет через IT» — согласны ли вы с этим мнением? '
                'В своём ответе: 1) чётко обозначьте свою позицию; 2) приведите не менее 2 аргументов; '
                '3) проанализируйте противоположную точку зрения; 4) сделайте вывод.'
            ),
            'prompt_uz': (
                "\"Kelajakda barcha ta'lim IT orqali bo'ladi\" fikriga qo'shilasizmi? "
                "Javobingizda: 1) aniq pozitsiyangizni bildiring; 2) kamida 2 ta dalil keltiring; "
                "3) qarshi fikrni tahlil qiling; 4) xulosa chiqaring."
            ),
            'options_ru': [], 'options_uz': [], 'correct_indices': [],
        },
    ],
    'creative': [
        {
            'key': 'creative-plan-b-1', 'difficulty': -0.6,
            'category_ru': 'Гибкость мышления', 'category_uz': 'Fikrlash moslashuvchanligi',
            'prompt_ru': (
                'Вы работаете над групповым проектом, но ключевой ресурс (например, нужная программа или '
                'оборудование) внезапно перестал работать. Как поступит студент с креативным подходом в первую очередь?'
            ),
            'prompt_uz': (
                "Jamoaviy loyiha ustida ishlayapsiz, biroq eng asosiy resurs (masalan, kerakli dastur yoki jihoz) "
                "to'satdan ishlamay qoldi. Kreativ yondashuvga ega talabaning birinchi harakati qanday bo'ladi?"
            ),
            'options_ru': [
                'Остановит проект и попросит у преподавателя помощи или продления срока.',
                'Будет искать виноватых и устроит разбирательство в команде.',
                'Отложит проблему в сторону и задастся вопросом «Как добиться того же результата без этого ресурса?», ища альтернативные варианты (план Б).',
                'Начнёт проект заново, выбрав совершенно другую тему.',
            ],
            'options_uz': [
                "Loyihani to'xtatib, o'qituvchidan yordam yoki vaqt uzaytirilishini so'raydi.",
                'Aybdorlarni qidiradi va jamoada bahs tashkil qiladi.',
                'Muammoni chetga surib, "Ushbu resursiz ham xuddi shu natijaga qanday erishish mumkin?" degan savol ustida muqobil variantlarni (B rejani) qidiradi.',
                'Loyihani boshidan, mutloq boshqa mavzuda qayta boshlaydi.',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'creative-presentation-hook-1', 'difficulty': -0.3,
            'category_ru': 'Творческая подача', 'category_uz': 'Ijodiy taqdimot',
            'prompt_ru': (
                'Вам поручили сделать презентацию на совершенно новую и незнакомую тему. Какой креативный подход '
                'эффективнее всего заинтересует аудиторию с первой минуты?'
            ),
            'prompt_uz': (
                "Sizga mutloq yangi va notanish mavzuda taqdimot (prezentatsiya) qilish topshirildi. Auditoriyani "
                "birinchi daqiqadanoq jalb qilish uchun qaysi kreativ yondashuv eng samarali?"
            ),
            'options_ru': [
                'Зачитать официальное определение темы и план слайдов.',
                'Начать с неожиданного, удивительного факта по теме или провокационного вопроса, связанного с личным опытом аудитории.',
                'Показывать только картинки, чтобы быстрее закончить презентацию.',
                'Говорить, не глядя на аудиторию, а только на экран.',
            ],
            'options_uz': [
                "Mavzuning rasmiy ta'rifi va slaydlar rejasini o'qib berish.",
                "Mavzuga aloqador kutilmagan, hayratlanarli fakt yoki auditoriyaning shaxsiy tajribasiga bog'liq provokatsion savol bilan boshlash.",
                "Taqdimotni tezroq tugatish uchun faqat rasm ko'rsatish.",
                "Auditoriyaga qaramasdan, faqat ekanga qarab gapirish.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-thesis-interdisciplinary-1', 'difficulty': 0.4,
            'category_ru': 'Междисциплинарный подход', 'category_uz': 'Fanlararo yondashuv',
            'prompt_ru': (
                'Тема выпускной квалификационной работы студента слишком стандартна и скучна. Как лучше всего '
                'привнести в неё научную новизну и креативный подход?'
            ),
            'prompt_uz': (
                "Talabaning bitiruv malakaviy ishi (dissertatsiyasi) mavzusi juda standart va zerikarli. Unga ilmiy "
                "yangilik va kreativ yondashuv olib kirishning eng yaxshi yo'li nima?"
            ),
            'options_ru': [
                'Полностью сменить тему.', 'Дословно скопировать чужую работу, оформив её красивым дизайном.',
                'Связать эту традиционную тему с совершенно другой областью (например, педагогику с искусственным интеллектом или IT-инструментами), применив междисциплинарный подход.',
                'Ограничиться только местной литературой.',
            ],
            'options_uz': [
                'Mavzuni butunlay o\'zgartirish.', "Boshqa olimlarning ishini so'zma-so'z ko'chirib, chiroyli dizayn berish.",
                "Ushbu an'anaviy mavzuni mutloq boshqa soha bilan (masalan, pedagogikani sun'iy intellekt yoki IT-instrumentlar bilan) bog'lab, fanlararo (interdisiplinar) yondashuvni qo'llash.",
                'Faqat mahalliy adabiyotlar bilan cheklanish.',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'creative-app-marketing-1', 'difficulty': 0.0,
            'category_ru': 'Креативный маркетинг', 'category_uz': 'Kreativ marketing',
            'prompt_ru': (
                'Представьте, вы создали новое образовательное мобильное приложение, но студенты не хотят его '
                'скачивать. Какой креативный маркетинговый подход даст лучший результат для его продвижения?'
            ),
            'prompt_uz': (
                "Tasavvur qiling, siz yangi ta'lim mobil ilovasini yaratdingiz, lekin talabalar uni yuklab olishni "
                "xohlashmayapti. Uni ommalashtirish uchun qaysi kreativ marketing yondashuvi eng yaxshi natija beradi?"
            ),
            'options_ru': [
                'Раздавать в коридорах университета бумажные флаеры с названием приложения.',
                'Добавить в приложение геймификацию (игровые элементы) и рейтинговое соревнование между студентами, пообещав победителям реальные бонусы (например, подарки от кафедры).',
                'Заставлять студентов скачивать приложение в обязательном порядке.', 'Повысить цену приложения.',
            ],
            'options_uz': [
                "Universitet yo'laklariga ilova nomi yozilgan qog'oz flayerlarni tarqatish.",
                "Ilovaga geymifikatsiya (o'yin elementlari) va talabalar o'rtasida reyting musobaqasini e'lon qilib, g'oliblarga real bonuslar (masalan, kafedra sovg'alari) va'da qilish.",
                "Talabalarni majburiy ravishda yuklab olishga majburlash.", 'Ilovaning narxini oshirish.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-stairs-gamification-1', 'difficulty': -0.4,
            'category_ru': 'Творческое решение проблем', 'category_uz': 'Muammoni ijodiy hal qilish',
            'prompt_ru': (
                'В учебном корпусе не работает лифт, и студенты постоянно жалуются, скучая при подъёме на верхние '
                'этажи. Как решить эту проблему дёшево и креативно?'
            ),
            'prompt_uz': (
                "O'quv binosida lift ishlamayapti va talabalar yuqori qavatlarga chiqishda doim zerikib, shikoyat "
                "qilishadi. Ushbu muammoni arzon va kreativ yondashuv bilan qanday hal qilish mumkin?"
            ),
            'options_ru': [
                'Требовать покупки нового лифта.', 'Полностью закрыть лестницы.',
                'Разрисовать ступени лестницы интересными логическими вопросами, мотивационными фразами или счётчиком сожжённых калорий (превратив каждую ступеньку в увлекательный опыт).',
                'Отменить занятия на верхних этажах.',
            ],
            'options_uz': [
                'Yangi lift sotib olishni talab qilish.', "Zinalarni butunlay yopib qo'yish.",
                "Zina poyalariga qiziqarli mantiqiy savollar, motivatsion iboralar yoki kaloriya yo'qotish ko'rsatkichlarini chizish (har bir zinani qiziqarli tajribaga aylantirish).",
                'Yuqori qavatdagi darslarni bekor qilish.',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'creative-cross-domain-1', 'difficulty': 0.5,
            'category_ru': 'Перенос знаний', 'category_uz': 'Bilimlarni ko\'chirish',
            'prompt_ru': (
                'Студенту поручили решить проблему не из его области (например, IT-студенту — маркетинговую '
                'задачу). Как проявляется креативный подход в этой ситуации?'
            ),
            'prompt_uz': (
                "Talabaga o'z sohasiga oid bo'lmagan muammoni yechish topshirildi (masalan, IT talabasiga marketing "
                "masalasi). Kreativ yondashuv bu vaziyatda qanday namoyon bo'ladi?"
            ),
            'options_ru': [
                'Отказаться от задания со словами «это не моя область».',
                'Перенести методологию и алгоритмы из своей области (например, системный анализ) на проблему другой сферы, предложив нестандартное решение.',
                'Просто найти готовое решение проблемы в интернете.', 'Написать случайный ответ, не поняв вопроса.',
            ],
            'options_uz': [
                '"Bu mening soham emas" deb topshiriqdan bosh tortishda.',
                "O'z sohasidagi metodologiya va algoritmlarni (masalan, tizimli tahlilni) boshqa soha muammosiga ko'chirib, noodatiy yechim taklif qilishda.",
                'Muammoni shunchaki internetdan tayyor holda qidirishda.', 'Savolni tushunmasdan tasodifiy javob yozishda.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-brainstorm-question-1', 'difficulty': 0.2,
            'category_ru': 'Техника мозгового штурма', 'category_uz': "Beyn-shtorm texnikasi",
            'prompt_ru': (
                'При групповой работе все выдвигают одинаковые шаблонные идеи. Какой креативный вопрос нужно '
                'задать, чтобы полностью развернуть направление идей?'
            ),
            'prompt_uz': (
                "Guruh bo'lib ishlashda hamma bir xil andozaviy g'oyalarni beryapti. G'oyalar yo'nalishini butunlay "
                "yangi tomonga burish uchun qanday kreativ savol berish kerak?"
            ),
            'options_ru': [
                '«Подумайте получше, разве эти идеи не плохи?»',
                '«Если бы у нас был неограниченный бюджет и абсолютно волшебные возможности, как бы мы решили эту проблему?» (дать максимальную свободу).',
                '«У кого самая дешёвая идея?»', '«Давайте перестанем думать над идеей и попьём чаю?»',
            ],
            'options_uz': [
                '"Yaxshiroq o\'ylab ko\'ringlar, bu g\'oyalar yomon-ku?"',
                '"Agar bizda cheksiz budjet va mutloq sehrli imkoniyatlar bo\'lsa, bu muammoni qanday yechgan bo\'lardik?" (Maksimal erkinlik berish).',
                '"Kimda eng arzon g\'oya bor?"', '"Kelinglar, g\'oya o\'ylashni to\'xtatib, choy ichamiz?"',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-criticism-1', 'difficulty': -0.5,
            'category_ru': 'Отношение к критике', 'category_uz': 'Tanqidga munosabat',
            'prompt_ru': (
                'На занятии преподаватель резко раскритиковал выдвинутую студентом инновационную идею. Что сделает '
                'студент с креативным и профессиональным подходом?'
            ),
            'prompt_uz': (
                "Dars paytida o'qituvchi siz ilgari surgan innovatsion g'oyani keskin tanqid qildi. Kreativ va "
                "professional yondashuvga ega talaba nima qiladi?"
            ),
            'options_ru': [
                'Обидится на преподавателя и перестанет ходить на занятия.',
                'Воспримет критику как бесплатный тест (фидбэк) для улучшения идеи и проанализирует: «Какая именно часть идеи слаба и как её исправить?»',
                'Будет пытаться доказать свою правоту криком.', 'Полностью откажется от идеи и пойдёт стандартным путём.',
            ],
            'options_uz': [
                "O'qituvchidan xafa bo'lib, darsga kelmay qo'yadi.",
                'Tanqidni g\'oyani mukammallashtirish uchun bepul test (faydbek) deb qabul qiladi va "G\'oyaning aynan qaysi qismi zaif va uni qanday to\'g\'rilash mumkin?" deb tahlil qiladi.',
                "O'z fikrini baqirib isbotlashga harakat qiladi.", "G'oyasidan butunlay voz kechib, standart yo'ldan ketadi.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-dorm-project-1', 'difficulty': -0.7,
            'category_ru': 'Социальные проекты', 'category_uz': 'Ijtimoiy loyihalar',
            'prompt_ru': (
                'Как организовать социальный проект на основе креативного подхода для продуктивного использования '
                'свободного времени в студенческом общежитии?'
            ),
            'prompt_uz': (
                "Talabalar turar joyida (obshajida) bo'sh vaqtdan unumli foydalanish uchun kreativ yondashuv "
                "asosida qanday ijtimoiy loyiha tashkil qilish mumkin?"
            ),
            'options_ru': [
                'Каждый день проводить только турниры по компьютерным играм.',
                'Организовать уголок «Буккроссинга» (обмена книгами) и еженедельный «Вечер нестандартных идей» (TED-комнату).',
                'Заставлять студентов по очереди убирать комнаты.', 'Шуметь по ночам.',
            ],
            'options_uz': [
                "Har kuni faqat kompyuter o'yinlari turnirini o'tkazish.",
                '"Book Crossing" (kitob almashish) burchagi va haftalik "Nostandart g\'oyalar kechasi" (TED xonasi) tashkil etish.',
                "Talabalarni navbatma-navbat xonalarni tozalashga majburlash.", 'Kechalari shovqin solish.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-mind-maps-1', 'difficulty': -0.8,
            'category_ru': 'Визуальное мышление', 'category_uz': 'Vizual fikrlash',
            'prompt_ru': (
                'Какой креативный визуальный метод помогает систематизировать и запоминать информацию при '
                'подготовке к экзамену вместо сухой зубрёжки?'
            ),
            'prompt_uz': (
                "Imtihonga tayyorlanishda quruq yodlash (zubryajka) o'rniga qaysi kreativ vizual usul ma'lumotlarni "
                "tizimlashtirishga va eslab qolishga yordam beradi?"
            ),
            'options_ru': [
                'Перечитывать учебник несколько раз.', 'Просто подчёркивать важные места.',
                'Интеллект-карты (Mind Maps) — рисование понятий в виде древовидных сетей и ассоциативных пиктограмм.',
                'Дословно переписывать конспекты.',
            ],
            'options_uz': [
                "Kitobni bir necha marta qayta o'qish.", "Muhim joylarning tagiga shunchaki chizib chiqish.",
                "Intellekt-xaritalar (Mind Maps) — tushunchalarni daraxtsimon tarmoqlar va assotsiativ piktogrammalar yordamida chizish.",
                "Konspektlarni so'zma-so'z ko'chirish.",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'creative-startup-no-designer-1', 'difficulty': 0.6,
            'category_ru': 'Использование ресурсов', 'category_uz': 'Resurslardan foydalanish',
            'prompt_ru': (
                'Вы хотите создать стартап-проект, но в вашей команде нет дизайнера. Каким будет креативный '
                'подход в этой ситуации?'
            ),
            'prompt_uz': (
                "Siz startup loyiha yaratmoqchisiz, lekin jamoangizda dizayner yo'q. Kreativ yondashuv bu "
                "vaziyatda qanday bo'ladi?"
            ),
            'options_ru': [
                'Полностью остановить проект до нахождения дизайнера.',
                'Представить некрасивый продукт без дизайна, состоящий только из чёрного текста.',
                'Используя нейросети (AI-визуализаторы) и готовые no-code шаблоны, самостоятельно подготовить прототип минимально готового продукта (MVP).',
                'Напрямую украсть дизайн другой компании.',
            ],
            'options_uz': [
                'Dizayner topilguncha loyihani butunlay to\'xtatish.',
                "Dizaynsiz, faqat qora matnlardan iborat xunuk mahsulot taqdim etish.",
                "Neyrotarmoqlar (AI vizualizatorlar) va tayyor no-code shablonlardan foydalanib, minimal tayyor mahsulot (MVP) prototipini o'zi tayyorlash.",
                'Boshqa kompaniyaning dizaynini to\'g\'ridan-to\'g\'ri o\'g\'irlash.',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'creative-inversion-1', 'difficulty': 0.7,
            'category_ru': 'Метод инверсии', 'category_uz': 'Inversiya metodi',
            'prompt_ru': (
                'Согласно креативному методу «Инверсия» (переворачивание вещей), как изменится вопрос «Что нужно '
                'сделать, чтобы студенты чаще посещали занятия?» при креативном подходе?'
            ),
            'prompt_uz': (
                '"Narsalarni teskari o\'girish" (Inversion) kreativ metodiga ko\'ra, "Talabalar darsga ko\'proq '
                'kelishi uchun nima qilish kerak?" degan savol kreativ yondashuvda qanday o\'zgartiriladi?'
            ),
            'options_ru': [
                '«Как наказать тех, кто не пришёл на занятие?»',
                '«Как нужно организовать занятие, чтобы студенты мечтали сбежать с него и вообще не приходить?» (прийти к решению через поиск ошибок).',
                '«Как можно сократить часы занятий?»', '«Как повысить зарплату преподавателя?»',
            ],
            'options_uz': [
                '"Darsga kelmaganlarni qanday jazolash kerak?"',
                '"Darsni qanday tashkil qilsak, talabalar undan qochib ketishni va umuman kelmaslikni orzu qiladi?" (Xatolarni topish orqali yechimga kelish).',
                '"Dars soatlarini qanday kamaytirish mumkin?"', '"O\'qituvchining oyligini qanday oshirish kerak?"',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-automate-task-1', 'difficulty': 0.1,
            'category_ru': 'Автоматизация процессов', 'category_uz': 'Jarayonlarni avtomatlashtirish',
            'prompt_ru': (
                'Во время учебной практики (стажировки) вам дали очень скучное и однообразно повторяющееся '
                'механическое задание (например, ввод данных в таблицу). Как креативный студент подойдёт к этой ситуации?'
            ),
            'prompt_uz': (
                "O'quv amaliyoti (stajirovka) davomida sizga juda zerikarli va bir xil takrorlanadigan mexanik "
                "topshiriq berildi (masalan, ma'lumotlarni jadvalga kiritish). Kreativ talaba bu vaziyatga qanday yondashadi?"
            ),
            'options_ru': [
                'Будет выполнять работу максимально медленно, тратя время.',
                'Придумает способы автоматизировать этот механический процесс (например, с помощью небольшого скрипта или макросов Excel) и сэкономит время.',
                'Откажется от выполнения задания.', 'Попросит другого студента выполнить его за деньги.',
            ],
            'options_uz': [
                "Ishni imkon qadar sekin bajarib, vaqt o'tkazadi.",
                "Ushbu mexanik jarayonni avtomatlashtirish yo'llarini (masalan, kichik skript yoki Excel makroslari yordamida) o'ylab topadi va vaqtni tejaydi.",
                'Topshiriqni bajarishdan bosh tortadi.', "Boshqa talabadan pul evaziga bajarib berishni so'raydi.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-constraint-teaching-1', 'difficulty': 0.8,
            'category_ru': 'Творчество в условиях ограничений', 'category_uz': 'Cheklovlar ostida ijodkorlik',
            'prompt_ru': (
                'Тест «Ограничение ресурсов»: если у вас нет компьютера, интернета и света, как объяснить '
                'студентам урок программирования?'
            ),
            'prompt_uz': (
                '"Resurslarni cheklash" testi: Agar sizda kompyuter, internet va chiroq bo\'lmasa, talabalar uchun '
                'dasturlash darsini qanday tushuntirish mumkin?'
            ),
            'options_ru': [
                'Отменить урок до появления света.',
                'Предложить студентам сыграть роли «элементов компьютера и переменных», объяснив шаги алгоритма в виде интерактивной живой игры (театра).',
                'Просто зачитывать правила из книги вслух.', 'Сидеть и жаловаться на отсутствие света.',
            ],
            'options_uz': [
                'Darsni chiroq yonguncha bekor qilish.',
                'Talabalarni "kompyuter elementlari va o\'zgaruvchilar" rolini o\'ynashga taklif qilib, algoritm qadamlarini interaktiv jonli o\'yin (teatr) ko\'rinishida tushuntirish.',
                "Kitobdan faqat qoidalarni ovoz chiqarib o'qib berish.", "Chiroq yo'qligidan shikoyat qilib o'tirish.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-idea-journal-1', 'difficulty': -0.9,
            'category_ru': 'Творческие привычки', 'category_uz': 'Ijodiy odatlar',
            'prompt_ru': 'Какая личная привычка наиболее эффективна для формирования банка креативных идей?',
            'prompt_uz': "Kreativ g'oyalar bankini shakllantirish uchun eng samarali shaxsiy odat qaysi?",
            'options_ru': [
                'Читать книги только по своей специальности.',
                'Вести «Дневник идей» и записывать любые мысли, пришедшие в голову за день (даже самые безумные).',
                'Сразу забывать пришедшие идеи.', 'Следить только за тем, что говорят знаменитости.',
            ],
            'options_uz': [
                "Faqat o'z mutaxassisligiga oid kitoblarni o'qish.",
                '"G\'oyalar kundaligi"ni yuritish va har kuni xayolga kelgan har qanday (hatto eng aqldan ozgan bo\'lsa ham) fikrlarni qayd etib borish.',
                "Kelgan g'oyalarni darhol unutish.", "Faqat mashhurlar nima deyotganini kuzatish.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-empathy-conflict-1', 'difficulty': 0.3,
            'category_ru': 'Творческая эмпатия', 'category_uz': 'Kreativ empatiya',
            'prompt_ru': (
                'Как лидер группы вы хотите творчески разрешить конфликт между одногруппниками. Какой метод '
                'выражает креативную эмпатию?'
            ),
            'prompt_uz': (
                "Guruh sardori sifatida guruhdoshlaringiz o'rtasidagi ziddiyatni (konfliktni) ijodiy hal "
                "qilmoqchisiz. Qaysi uslub kreativ empatiyani ifodalaydi?"
            ),
            'options_ru': [
                'Наказать обе стороны.',
                'Поменять стороны ролями (ролевая игра) и попросить взглянуть на проблему глазами противоположной стороны.',
                'Вообще не вмешиваться в конфликт.', 'Встать на сторону того, кто сильнее.',
            ],
            'options_uz': [
                'Ikkala tomonni ham jazolash.',
                "Tomonlarni bir-birlarining roliga o'tkazish (roli o'yin) va muammoga qarshi tomon ko'zi bilan qarashni so'rash.",
                'Ziddiyatga umuman aralashmaslik.', "Kim kuchli bo'lsa, o'shaning yonini olish.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-systemic-test-1', 'difficulty': 0.9,
            'category_ru': 'Системная креативность', 'category_uz': 'Tizimli kreativlik',
            'prompt_ru': 'Как вы проверите свой проект с точки зрения «системной креативности», чтобы он оказался успешным?',
            'prompt_uz': 'Loyihangiz muvaffaqiyatli chiqishi uchun uni "Tizimli kreativlik" nuqtai nazaridan qanday tekshirasiz?',
            'options_ru': [
                'Решите, что если нравится вам, значит понравится всем.',
                'Покажете его людям совершенно другого возраста и интересов (например, маленьким детям или пожилым) и понаблюдаете за их реакцией.',
                'Будете хранить в тайне, никому не показывая.', 'Спросите мнение только у близких друзей.',
            ],
            'options_uz': [
                'Faqat o\'zingizga yoqsa, demak hammaga yoqadi deb hisoblaysiz.',
                "Uni mutloq boshqa yoshdagi, boshqa qiziqishdagi insonlarga (masalan, kichik bolalarga yoki qariyalarga) ko'rsatib, ularning reaksiyasini kuzatasiz.",
                'Hech kimga ko\'rsatmasdan sir saqlaysiz.', "Faqat yaqin do'stlaringizdan fikr so'raysiz.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-eco-art-1', 'difficulty': -0.2,
            'category_ru': 'Творческие мероприятия', 'category_uz': 'Ijodiy tadbirlar',
            'prompt_ru': (
                'В университете нужно провести неделю «Экологической культуры». Какое креативное мероприятие '
                'оставит у студентов наибольшее впечатление?'
            ),
            'prompt_uz': (
                'Universitetda "Ekologik madaniyat" haftaligini o\'tkazish kerak. Qaysi kreativ tadbir talabalarda '
                'eng ko\'p taassurot qoldiradi?'
            ),
            'options_ru': [
                'Прослушать двухчасовую лекцию про экологию.',
                'Организовать выставку скульптур и одежды в стиле «Эко-арт» из пластиковых и бумажных отходов, оставленных студентами.',
                'Просто нарисовать обычные плакаты и повесить на стену.', 'Ограничиться только уборкой улицы (субботником).',
            ],
            'options_uz': [
                'Ekologiya haqida 2 soatlik ma\'ruza eshitish.',
                'Talabalar tashlab ketgan plastik va qog\'oz chiqindilaridan "Eko-art" haykaltaroshlik va kiyimlar ko\'rgazmasini tashkil etish.',
                'Oddiy plakatlar chizib devorga ilish.', "Faqat ko'cha tozalash (subbotnik) bilan cheklanish.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-combination-game-1', 'difficulty': 1.0,
            'category_ru': 'Комбинирование идей', 'category_uz': "G'oyalarni birlashtirish",
            'prompt_ru': (
                '«Неожиданная комбинация»: если бы вы были создателем компьютерных игр и вам поручили объединить '
                'предметы «История» и «Химия», какую креативную игру вы бы придумали?'
            ),
            'prompt_uz': (
                '"Kutilmagan kombinatsiya": Agar siz kompyuter o\'yinlari yaratuvchisi bo\'lsangiz va sizga '
                '"Tarix" va "Kimyo" fanlarini birlashtirish topshirilsa, qanday kreativ o\'yin o\'ylab topgan bo\'lardingiz?'
            ),
            'options_ru': [
                'Создал бы исторический учебник только с химическими формулами.',
                'RPG-игру о древних алхимиках, которые в прошлом искали вещества, влияющие на исторические события.',
                'Никакую игру придумать невозможно.', 'Составил бы обычную тестовую программу.',
            ],
            'options_uz': [
                'Faqat kimyoviy formulalar yozilgan tarixiy kitob yaratardim.',
                'Qadimgi kimyogarlar (alximiklar) o\'tmishda tarixiy voqealarga ta\'sir qiladigan moddalarni qidirishi haqidagi RPG o\'yini.',
                "Hech qanday o'yin o'ylab topib bo'lmaydi.", 'Oddiy test dasturi tuzardim.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-presentation-closing-1', 'difficulty': -0.1,
            'category_ru': 'Завершение презентации', 'category_uz': 'Taqdimotni yakunlash',
            'prompt_ru': 'Как креативный студент завершит свою презентацию, чтобы победить в конкурсе инновационных проектов?',
            'prompt_uz': "Innovatsion loyihalar tanlovida g'olib bo'lish uchun kreativ talaba o'z taqdimotini qanday yakunlaydi?",
            'options_ru': [
                'Надписью «Спасибо за внимание».',
                'Призывом к действию (Call to Action) с визуальным обращением, показывающим реальный результат проекта через год.',
                'Просто выключив слайды.', 'Поблагодарив жюри.',
            ],
            'options_uz': [
                '"E\'tiboringiz uchun rahmat" degan yozuv bilan.',
                'Tinglovchilarni harakatga keltiruvchi (Call to Action), loyihaning kelajakdagi 1 yillik real natijasini ko\'rsatuvchi vizual chaqiriq bilan.',
                'Slaydlarni shunchaki o\'chirib qo\'yish bilan.', "Hakamlar hay'atiga rahmat aytish bilan.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-team-motivation-1', 'difficulty': 0.45,
            'category_ru': 'Командная мотивация', 'category_uz': 'Jamoaviy motivatsiya',
            'prompt_ru': (
                'Ваши одногруппники не проявляют интереса к учебному проекту. Что вы сделаете, чтобы пробудить у '
                'них креативную мотивацию (внутренний интерес)?'
            ),
            'prompt_uz': (
                "Guruhdoshlaringiz dars loyihasiga qiziqish bildirmayapti. Ularda kreativ motivatsiya (ichki "
                "qiziqish) uyg'otish uchun nima qilasiz?"
            ),
            'options_ru': [
                'Напугаете их низкой оценкой.',
                'Учтёте личные интересы каждого одногруппника (например, кто-то любит рисовать, кто-то — писать тексты) и распределите задачи креативно.',
                'Выполните всю работу сами.', 'Пожалуетесь преподавателю на группу.',
            ],
            'options_uz': [
                "Ularga past baho olishlarini aytib qo'rqitasiz.",
                "Har bir guruhdoshingizning shaxsiy qiziqishlarini (masalan, biri rasm chizishni, biri matn yozishni yoqtirsa) inobatga olib, vazifalarni kreativ taqsimlaysiz.",
                "Ishning hammasini o'zingiz bajarasiz.", "O'qituvchiga guruh ustidan shikoyat qilasiz.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-turn-weakness-1', 'difficulty': -1.0,
            'category_ru': 'Превращение недостатка в преимущество', 'category_uz': 'Kamchilikni afzallikka aylantirish',
            'prompt_ru': (
                'Креативный принцип «превращение недостатка в преимущество»: созданная вами программа или мобильное '
                'приложение работает очень медленно, и пока это невозможно исправить. Какой креативный подход '
                'применить, чтобы пользователи не нервничали?'
            ),
            'prompt_uz': (
                '"Kamchilikni afzallikka aylantirish" kreativ prinsipi: Siz yaratgan dastur yoki mobil ilova juda '
                'sekin ishlayapti va buni hozircha to\'g\'rilashning iloji yo\'q. Foydalanuvchilar asabiylashmasligi '
                'uchun qanday kreativ yondashuv qo\'llash mumkin?'
            ),
            'options_ru': [
                'Полностью удалить программу.',
                'Разместить во время загрузки (Loading) интересную мини-игру (например, игру с динозавром в Google Chrome) или полезные афоризмы.',
                'Не обращать внимания на пользователей.', 'Сделать интерфейс программы тёмным.',
            ],
            'options_uz': [
                'Dasturni butunlay o\'chirib tashlash.',
                'Yuklanish (Loading) jarayoniga qiziqarli mini-o\'yin (masalan, Google Chrome dagi dinozavr o\'yini) yoki foydali aforizmlar joylashtirish.',
                "Foydalanuvchilarga e'tibor bermaslik.", 'Dastur interfeysini qoraytirish.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-readiness-failure-1', 'difficulty': 0.55,
            'category_ru': 'Готовность к неудачам', 'category_uz': 'Muvaffaqiyatsizlikka tayyorlik',
            'prompt_ru': 'Преодоление препятствий: к чему нужно быть готовым в первую очередь при воплощении креативных идей в жизнь?',
            'prompt_uz': "To'siqlarni yengish: Kreativ g'oyalarni hayotga tatbiq etishda eng birinchi navbatda nimaga tayyor bo'lish kerak?",
            'options_ru': [
                'К тому, что сразу разбогатеете.', 'К первым неудачам, ошибкам и скептическому отношению (критике) окружающих.',
                'К тому, что все вас поддержат.', 'К тому, что не будет никаких ошибок.',
            ],
            'options_uz': [
                'Darhol boyib ketishga.', "Dastlabki muvaffaqiyatsizliklar, xatolar va atrofdagilarning skeptik munosabatiga (tanqidiga).",
                'Hamma sizni qo\'llab-quvvatlashiga.', 'Hech qanday xatolik bo\'lmasligiga.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-nature-analogy-1', 'difficulty': 0.75,
            'category_ru': 'Аналогическое мышление', 'category_uz': 'Analogik fikrlash',
            'prompt_ru': (
                '«Поиск аналогий»: если бы вы создавали систему управления учебным процессом (LMS) и хотели '
                'сравнить её архитектуру с какой-либо системой из природы, какая креативная аналогия подошла бы больше всего?'
            ),
            'prompt_uz': (
                '"Analogiyalar topish": Agar siz o\'quv jarayonini boshqarish tizimini (LMS) yaratmoqchi bo\'lsangiz '
                've uning arxitekturasini tabiatdagi biror tizimga o\'xshatmoqchi bo\'lsangiz, eng mos kreativ '
                'analogiya qaysi?'
            ),
            'options_ru': [
                'Обычный шкаф или полка.',
                'Муравейник или улей (у каждого члена есть чёткая роль, и все симметрично работают ради общей цели).',
                'Куча камней.', 'Проточная вода.',
            ],
            'options_uz': [
                'Shunchaki oddiy javon yoki shkaf.',
                "Chumolilar uyasi yoki asalarilar uyasi (har bir a'zoning aniq roli bor va umumiy maqsad sari simmetrik ishlaydi).",
                'Toshlar to\'plami.', 'Oqar suv.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'creative-soft-skill-value-1', 'difficulty': 0.95,
            'category_ru': 'Значение креативности', 'category_uz': 'Kreativlikning ahamiyati',
            'prompt_ru': (
                'Почему креативный подход считается одним из важнейших гибких навыков (soft skills) для '
                'современного выпускника (специалиста)?'
            ),
            'prompt_uz': (
                "Nima uchun kreativ yondashuv zamonaviy bitiruvchi (mutaxassis) uchun eng muhim ko'nikmalardan "
                "(Soft Skills) biri hisoblanadi?"
            ),
            'options_ru': [
                'Потому что креативные люди вообще не соблюдают правила.',
                'Потому что стандартную и алгоритмизированную работу вскоре займут искусственный интеллект и роботы, и способность человека находить решения в нестандартных ситуациях станет бесценной.',
                'Потому что креативность нужна только людям искусства.', 'Чтобы легко сдавать экзамены.',
            ],
            'options_uz': [
                'Kreativ insonlar qoidalarni umuman buzishgani uchun.',
                "Standart va algoritmlashgan ishlarni tez orada sun'iy intellekt va robotlar egallashi sababli, insonning nostandart vaziyatlarda yechim topish qobiliyati beqiyos bo'lib qoladi.",
                'Kreativlik faqat san\'atkorlarga kerak bo\'lgani uchun.', 'Imtihonlardan oson o\'tish uchun.',
            ],
            'correct_indices': [1],
        },
    ],
    # Sourced from a dedicated "Muammoni yechish ko'nikmasini aniqlash testlari" bank —
    # 21 standalone MCQ scenarios ('ps-core-*') plus 10 longer "[Vaziyat]" situational
    # scenarios ('ps-scenario-*'), 31 questions total. The source already flags the
    # correct option inline (bracketed "To'g'ri javob"/"Toʻgʻri javob" tag), so no
    # difficulty-tier structure to preserve — difficulty is assigned as a smooth band
    # per section (core -1.00..0.30, scenario 0.40..1.12).
    'problem_solving': [
        # -- Core MCQ scenarios — 21 questions ---------------------------------------------
        {
            'key': 'ps-core-1', 'difficulty': -1.0,
            'category_ru': 'Определение проблемы', 'category_uz': 'Muammoni aniqlash',
            'prompt_ru': 'Какой самый первый и самый важный этап успешного решения проблемы?',
            'prompt_uz': 'Muammoni muvaffaqiyatli hal qilishning eng birinchi va eng muhim bosqichi qaysi?',
            'options_ru': [
                'Сразу составить план из нескольких решений',
                'Чётко сформулировать проблему и проанализировать её первопричину',
                'Попросить помощи у окружающих', 'Ждать, пока проблема решится сама собой',
            ],
            'options_uz': [
                'Darhol bir nechta yechimlar rejasini yozish',
                'Muammoni aniq taʼriflash va uning kelib chiqish ildizini (sababini) tahlil qilish',
                'Atrofdagilardan yordam soʻrash', 'Muammoning oʻz-oʻzidan hal boʻlishini kutish',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-2', 'difficulty': -0.94,
            'category_ru': 'Командная работа', 'category_uz': 'Jamoada ishlash',
            'prompt_ru': (
                'Во время групповой работы одногруппник, отвечающий за важную часть проекта, '
                'сообщил, что не успевает к дедлайну. Какое действие является наиболее правильным решением проблемы?'
            ),
            'prompt_uz': (
                'Guruh boʻlib ishlayotganingizda, loyihaning muhim qismiga masʼul boʻlgan guruhdoshingiz '
                'belgilangan muddatga (dedlaynga) ulgura olmasligini aytdi. Qaysi harakat eng toʻgʻri muammoli yechim hisoblanadi?'
            ),
            'options_ru': [
                'Исключить его из группы и пожаловаться преподавателю',
                'Перераспределить задачи между оставшимися членами группы и помочь ему завершить оставшуюся часть',
                'Пропустить срок сдачи проекта', 'Сделать всю работу самому вместо него и перестать с ним разговаривать',
            ],
            'options_uz': [
                'Uni guruhdan chetlashtirish va oʻqituvchiga shikoyat qilish',
                'Guruhning qolgan aʼzolari oʻrtasida vazifalarni qayta taqsimlab, unga qolgan qismni yakunlashga koʻmaklashish',
                'Loyihani topshirish muddatini oʻtkazib yuborish', 'Uning oʻrniga hamma ishni bir oʻzi bajarish va guruhdoshi bilan gaplashmay qoʻyish',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-3', 'difficulty': -0.87,
            'category_ru': 'Научный метод', 'category_uz': 'Ilmiy metod',
            'prompt_ru': (
                'Во время научного исследования или работы над проектом ваша исходная гипотеза '
                'неожиданно оказалась полностью неверной. Что вы сделаете в этой ситуации?'
            ),
            'prompt_uz': (
                'Ilmiy tadqiqot yoki loyiha ustida ishlayotganingizda, kutilmaganda dastlabki gipotezangiz '
                '(taxminingiz) mutloq xato boʻlib chiqdi. Bu vaziyatda nima qilasiz?'
            ),
            'options_ru': [
                'Полностью прекратите исследование', 'Подделаете реальные цифры и результаты, чтобы они соответствовали гипотезе',
                'Примете неверный результат как научный факт, проанализируете причину ошибки и разработаете новую гипотезу',
                'Свалите вину на лабораторное оборудование',
            ],
            'options_uz': [
                'Tadqiqotni butunlay toʻxtatasiz', 'Gipotezaga mos kelishi uchun real raqamlar va natijalarni soxtalashtirasiz',
                'Notoʻgʻri chiqqan natijani ham ilmiy fakt deb qabul qilib, xatolik sababini tahlil qilasiz va yangi gipoteza ishlab chiqasiz',
                'Aybni laboratoriya jihozlariga agʻdaradi',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-core-4', 'difficulty': -0.81,
            'category_ru': 'Реакция на критику', 'category_uz': 'Tanqidga munosabat',
            'prompt_ru': (
                'Жюри дало очень резкий, негативный отзыв о вашей презентации программного продукта или '
                'проекта. Какой будет реакция студента, конструктивно решающего проблемы?'
            ),
            'prompt_uz': (
                'Siz tayyorlagan dasturiy taʼminot yoki loyiha taqdimotiga hakamlar hayʼati juda keskin, salbiy '
                'fikr bildirishdi. Konstruktiv muammo yechuvchi talabaning reaksiyasi qanday boʻladi?'
            ),
            'options_ru': [
                'Спорить с жюри, обвиняя их в некомпетентности',
                'Отложить эмоции в сторону, выделить обоснованные пункты критики и составить план доработки проекта',
                'Выбросить проект и больше не возвращаться к этой сфере', 'Проигнорировать критику и оставить проект без изменений',
            ],
            'options_uz': [
                'Hakamlar hayʼati bilan tortishib, ularni maʼlumotsizlikda ayblaydi',
                'Hissiyotlarni chetga surib, tanqidlardagi asosli punktlarni ajratib oladi va loyihani takomillashtirish rejasini tuzadi',
                'Loyihani axlatga tashlab, boshqa bu sohaga qaytmaydi', 'Tanqidlarga eʼtibor bermay, loyihani oʻzgarishsiz qoldiradi',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-5', 'difficulty': -0.74,
            'category_ru': 'Системное решение', 'category_uz': 'Tizimli yechim',
            'prompt_ru': (
                'В университетской библиотеке студенты подолгу стоят в очереди, что вызывает недовольство. '
                'Какой подход наиболее правильно системно решает эту проблему?'
            ),
            'prompt_uz': (
                'Universitet kutubxonasida talabalar juda koʻp navbat kutib qolishmoqda va bu norozilik '
                'tugʻdirmoqda. Ushbu muammoni tizimli hal qilish uchun qaysi yondashuv eng toʻgʻri?'
            ),
            'options_ru': [
                'Ограничить доступ студентов в библиотеку', 'Нанять охранника для наведения порядка в очереди',
                'Проанализировать процесс и оцифровать выдачу/приём книг (внедрить QR-коды или электронный каталог)',
                'Полностью закрыть библиотеку',
            ],
            'options_uz': [
                'Kutubxonaga talabalarni kiritishni cheklash', 'Navbatda turganlarni tartibga solish uchun qoʻriqchi yollash',
                'Jarayonni tahlil qilib, kitob olish/topshirishni raqamlashtirish (QR-kod yoki elektron katalog tizimini joriy etish)',
                'Kutubxonani butunlay yopib qoʻyish',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-core-6', 'difficulty': -0.68,
            'category_ru': 'Управление кризисом', 'category_uz': 'Inqiroz boshqaruvi',
            'prompt_ru': (
                'Во время сдачи экзамена компьютерная система внезапно отключилась, и все введённые вами '
                'ответы стёрлись. Что вы сделаете в первую очередь?'
            ),
            'prompt_uz': (
                'Imtihon topshirish jarayonida kompyuter tizimi toʻsatdan oʻchib qoldi va siz kiritgan barcha '
                'javoblar oʻchib ketdi. Birinchi navbatda nima qilasiz?'
            ),
            'options_ru': [
                'Устроите скандал и уйдёте из здания, где проходит экзамен',
                'Немедленно сообщите о ситуации проверяющему (или технику) и зафиксируете проблему актом',
                'Попытаетесь сами разобрать компьютер и починить его', 'Будете просто сидеть и плакать',
            ],
            'options_uz': [
                'Baqir-chaqir qilib, imtihon binosidan chiqib ketasiz',
                'Vaziyatni darhol nazoratchiga (yoki texnik xodimga) xabar qilib, muammoni bayonnoma (akt) orqali qayd ettirasiz',
                'Kompyuterni oʻzingiz ochib, tuzatishga harakat qilasiz', 'Yigʻlab oʻtiraverasiz',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-7', 'difficulty': -0.61,
            'category_ru': 'Когнитивные искажения', 'category_uz': 'Kognitiv xatoliklar',
            'prompt_ru': (
                'Если по проблеме есть только один вариант решения и члены группы слепо следуют ему, '
                'к какой негативной когнитивной ошибке это может привести?'
            ),
            'prompt_uz': (
                'Agar muammoning yechimi haqida faqat bitta variant boʻlsa va guruh aʼzolari unga koʻr-koʻrona '
                'ergashishayotgan boʻlsa, ushbu holat qanday salbiy kognitiv xatolikka olib kelishi mumkin?'
            ),
            'options_ru': [
                'К избытку информации', 'К групповому мышлению (Groupthink) — потере критического подхода',
                'К алгоритмизации', 'К экономии времени',
            ],
            'options_uz': [
                'Maʼlumotlar koʻpligiga', 'Guruhbozlik fikrlashi (Groupthink) — tanqidiy yondashuvning yoʻqolishi',
                'Algoritmlashishga', 'Vaqtni tejashga',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-8', 'difficulty': -0.55,
            'category_ru': 'Разрешение конфликтов', 'category_uz': 'Nizolarni hal qilish',
            'prompt_ru': (
                'Между двумя лидерами в команде возник непримиримый конфликт по поводу стратегии реализации '
                'проекта. Как вы поступите в роли решающего проблему (медиатора)?'
            ),
            'prompt_uz': (
                'Jamoada ikki yetakchi talaba oʻrtasida loyihani amalga oshirish strategiyasi boʻyicha '
                'murosasiz nizo kelib chiqdi. Muammoni yechuvchi (mediator) sifatida qanday yoʻl tutasiz?'
            ),
            'options_ru': [
                'Встанете на сторону более сильного лидера', 'Отстраните обоих лидеров от проекта',
                'Сведёте аргументы обеих сторон в таблицу и оцените по объективным критериям, что больше соответствует цели проекта',
                'Оставите проблему без внимания',
            ],
            'options_uz': [
                'Kuchliroq yetakchining tarafini olasiz', 'Ikkala yetakchini ham loyihadan chetlatasiz',
                'Har ikki tomonning argumentlarini jadvalga solib, loyiha maqsadiga qaysi biri eng koʻp mos kelishini xolis mezonlar asosida baholaysiz',
                'Muammoni oʻz holiga tashlab qoʻyasiz',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-core-9', 'difficulty': -0.48,
            'category_ru': 'Декомпозиция', 'category_uz': 'Dekompozitsiya',
            'prompt_ru': 'Что означает метод «Декомпозиции» при решении сложной математической или программистской задачи?',
            'prompt_uz': "Murakkab matematik yoki dasturlash masalasini yechishda 'Dekompozitsiya' metodi nimani anglatadi?",
            'options_ru': [
                'Полностью отказаться от решения задачи',
                'Разделить большую и сложную проблему на более мелкие части (подзадачи), которые легче решать последовательно',
                'Искать ответ на задачу в интернете', 'Рассказывать формулы наизусть',
            ],
            'options_uz': [
                'Masalani yechishdan butunlay voz kechishni',
                'Katta va murakkab muammoni ketma-ket yechilishi oson boʻlgan kichikroq boʻlaklarga (sub-muammolarga) boʻlishni',
                'Masalaning javobini internetdan izlashni', 'Formulalarni yoddan aytib berishni',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-10', 'difficulty': -0.42,
            'category_ru': 'Навыки презентации', 'category_uz': 'Taqdimot koʻnikmalari',
            'prompt_ru': (
                'Вам нужно выступить перед инвесторами по вашему стартап-проекту, но отведённое время '
                'неожиданно сократили с 15 минут до 3 минут. Как вы решите эту проблему?'
            ),
            'prompt_uz': (
                'Startup loyihangiz uchun investorlar oldida nutq soʻzlashingiz kerak, biroq sizga berilgan '
                'vaqt kutilmaganda 15 daqiqadan 3 daqiqaga qisqartirildi. Muammoni qanday yechasiz?'
            ),
            'options_ru': [
                'Откажетесь от презентации из-за нехватки времени', 'Попытаетесь очень быстро проговорить стандартные слайды',
                'Перейдёте в формат «Elevator Pitch» и объясните только проблему, ваше решение и экономическую выгоду проекта (самую суть)',
                'Начнёте спорить с инвесторами, требуя не сокращать время',
            ],
            'options_uz': [
                'Vaqt kamligi uchun taqdimot qilishdan bosh tortasiz', 'Standart slaydlarni juda tez gapirib oʻqishga harakat qilasiz',
                "'Elevator Pitch' formatiga oʻtib, faqat muammo, sizning yechimingiz va loyihaning iqtisodiy foydasini (eng asosiy magʻzini) tushuntirasiz",
                'Investorlardan vaqtni qisqartirmaslikni talab qilib bahslashasiz',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-core-11', 'difficulty': -0.35,
            'category_ru': 'Анализ первопричины', 'category_uz': 'Ildiz sabab tahlili',
            'prompt_ru': (
                'У студентов в течение учебного года наблюдаются хроническая усталость и снижение '
                'успеваемости. Как работает метод «5 Почему?» для поиска истинной причины этой проблемы?'
            ),
            'prompt_uz': (
                "Talabalarda oʻquv yili davomida surunkali charchoq va dars oʻzlashtirishning pasayishi "
                "kuzatilmoqda. Ushbu muammoning haqiqiy sababini topish uchun '5 Nega?' metodi qanday ishlaydi?"
            ),
            'options_ru': [
                'Проведя со студентами 5 экзаменов',
                'Последовательно задавая вопрос «Почему?» к каждой выявленной причине, дойдя до истинного корня проблемы (например, до неправильно составленного расписания)',
                'Разделив проблему на 5 групп', 'Обсуждая проблему в течение 5 дней',
            ],
            'options_uz': [
                'Talabalardan 5 marta imtihon olish orqali',
                'Har bir aniqlangan sababga ketma-ket "Nima uchun?" savolini berish orqali muammoning tub ildiziga (masalan, notoʻgʻri tuzilgan dars jadvaliga) yetib borish',
                'Muammoni 5 ta guruhga boʻlish orqali', 'Muammoni 5 kun davomida muhokama qilish orqali',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-12', 'difficulty': -0.29,
            'category_ru': 'Диагностика', 'category_uz': 'Diagnostika',
            'prompt_ru': (
                'Разработанный вами программный инструмент не дал ожидаемого результата на пробном '
                'испытании (оценки студентов не выросли). Каким должен быть ваш первый технический шаг?'
            ),
            'prompt_uz': (
                'Siz ishlab chiqqan dasturiy vosita sinov imtihonida kutilgan natijani bermadi (talabalarning '
                'bahosi koʻtarilmadi). Birinchi texnik qadamingiz nima boʻlishi kerak?'
            ),
            'options_ru': [
                'Полностью удалить программу', 'Свалить вину на уровень знаний студентов',
                'Провести диагностику: собрать обратную связь, чтобы определить, какой модуль программы (методический, визуальный или тестовый) не работает',
                'Заново испытать программу без изменений в другой группе',
            ],
            'options_uz': [
                'Dasturni butunlay oʻchirib tashlash', 'Aybni talabalarning bilim darajasiga toʻnkash',
                'Diagnostika oʻtkazish: Dasturning qaysi moduli (metodologik, vizual yoki test qismi) ish bermayotganini aniqlash uchun qayta aloqa (faydbek) yigʻish',
                'Dasturni oʻzgartirmasdan boshqa guruhda qayta sinab koʻrish',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-core-13', 'difficulty': -0.22,
            'category_ru': 'Навыки коммуникации', 'category_uz': 'Muloqot koʻnikmalari',
            'prompt_ru': (
                'Одногруппник рассказал вам непонятную и запутанную проблему и попросил помощи. Какая '
                'техника общения нужна, чтобы правильно понять её и направить к решению?'
            ),
            'prompt_uz': (
                'Kursdoshingiz sizga tushunarsiz va chalkash muammoni aytib, yordam soʻradi. Uni toʻgʻri '
                'tushunish va muammo yechimiga yoʻnaltirish uchun qaysi muloqot texnikasi kerak?'
            ),
            'options_ru': [
                'Дать свои советы, не выслушав его',
                'Активное слушание — задавать вопросы и переспрашивать его слова своими словами (перефразирование), уточняя проблему',
                'Не воспринимать проблему всерьёз', 'Сразу перевести разговор на другую тему',
            ],
            'options_uz': [
                'Uni eshitmasdan oʻz maslahatlaringizni berish',
                'Faol eshitish (Active listening) — savollar berish va uning gaplarini oʻz soʻzlaringiz bilan qayta soʻrab (parafraz), muammoni aniqlashtirish',
                'Muammoni jiddiy qabul qilmaslik', 'Suhbatni darhol boshqa mavzuga burish',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-14', 'difficulty': -0.16,
            'category_ru': 'Групповая динамика', 'category_uz': 'Guruh dinamikasi',
            'prompt_ru': (
                'Если во время решения проблемы в команде все члены лишь одобряют мнение руководителя и '
                'никто не высказывает критики, как называется этот синдром?'
            ),
            'prompt_uz': (
                'Agar jamoada muammoni yechish davomida hamma aʼzolar faqat rahbarning fikrini maʼqullasa va '
                'hech kim tanqidiy fikr bildirmasa, bu qanday sindrom hisoblanadi?'
            ),
            'options_ru': [
                'Профессионализм', 'Синдром «Да, начальник» (Yes-man) или конформизм',
                'Алгоритмическое мышление', 'Латеральное мышление',
            ],
            'options_uz': [
                'Professionalizm', '"Ha, janob" (Yes-man) sindromi yoki konformizm',
                'Algoritmik fikrlash', 'Lateral fikrlash',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-15', 'difficulty': -0.09,
            'category_ru': 'Внешние ограничения', 'category_uz': 'Tashqi cheklovlar',
            'prompt_ru': (
                'Если решение какой-либо проблемы застопорилось из-за внешних причин, не зависящих от вас '
                '(например, из-за законодательства или отсутствия официального разрешения), какой путь наиболее разумен?'
            ),
            'prompt_uz': (
                'Agar biron-bir muammoning yechimi sizga bogʻliq boʻlmagan tashqi sabablar tufayli toʻxtab '
                'qolsa (masalan, qonunchilik yoki rasmiy ruxsatnoma yoʻqligi), eng oqilona yoʻl nima?'
            ),
            'options_ru': [
                'Продолжить работу, даже нарушая правила',
                'Временно заморозить эту часть проекта и развивать альтернативные модули, не требующие разрешения, или отправить официальные запросы',
                'Полностью закрыть проект', 'Ничего не делать, выражая недовольство ситуацией',
            ],
            'options_uz': [
                'Qoidalarni buzib boʻlsa ham ishni davom ettirish',
                'Loyihaning oʻsha qismini vaqtincha muzlatib, ruxsat talab qilmaydigan muqobil modullarini rivojlantirish yoki rasmiy soʻrovlar yuborish',
                'Loyihani butunlay yopish', 'Vaziyatdan norozi boʻlib, hech narsa qilmaslik',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-16', 'difficulty': -0.03,
            'category_ru': 'Поведенческая экономика', 'category_uz': 'Xulq-atvor iqtisodiyoti',
            'prompt_ru': (
                'Как можно применить «Технику подталкивания» (Nudge — логику маленького толчка) для '
                'решения проблемы пропуска занятий студентами?'
            ),
            'prompt_uz': (
                "Talabalarning dars qoldirish muammosini hal qilish uchun 'Nudge texnikasi' (Kichik turtki "
                "berish mantiqi) qanday qoʻllanilishi mumkin?"
            ),
            'options_ru': [
                'Запугивать пропустивших занятия немедленным отчислением',
                'Через автоматизированную систему отправлять студентам с полной посещаемостью интересные поощрительные сообщения и небольшие льготы (создавая позитивную среду)',
                'Усложнить рейтинговую систему', 'Вызывать родителей в университет',
            ],
            'options_uz': [
                'Dars qoldirganlarni darhol oʻqishdan haydash bilan qoʻrqitish',
                'Darsga toʻliq kelgan talabalarga avtomatlashtirilgan tizim orqali qiziqarli ragʻbatlantiruvchi xabarlar va kichik imtiyozlar berish (ijobiy muhit yaratish)',
                'Reyting tizimini murakkablashtirish', 'Ota-onalarini universitetga chaqirish',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-17', 'difficulty': 0.04,
            'category_ru': 'Абстрактное мышление', 'category_uz': 'Abstrakt fikrlash',
            'prompt_ru': 'Когда «Абстрактное мышление» помогает при решении технической проблемы?',
            'prompt_uz': "Biror texnik muammoni yechishda 'Abstrakt fikrlash' qachon yordam beradi?",
            'options_ru': [
                'Только при работе с точными цифрами',
                'Когда нужно отойти от мелких деталей проблемы и увидеть на макроуровне её общую структуру и связь с другими системами',
                'Когда в процессе написания кода возникает ошибка', 'При подписании документов',
            ],
            'options_uz': [
                'Faqat aniq raqamlar bilan ishlaganda',
                "Muammoning mayda detallaridan uzoqlashib, uning umumiy tuzilishi va boshqa tizimlar bilan aloqasini makro-darajada ko'ra bilishda",
                'Kod yozish jarayonida xatolik chiqqanda', 'Hujjatlarni imzolashda',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-18', 'difficulty': 0.1,
            'category_ru': 'Управление форс-мажором', 'category_uz': 'Fors-major boshqaruvi',
            'prompt_ru': (
                'В процессе реализации проекта произошёл «Неожиданный форс-мажор» (например, полностью '
                'пропал интернет). Что в первую очередь делает руководитель с высоким навыком решения проблем?'
            ),
            'prompt_uz': (
                "Loyihani amalga oshirish jarayonida 'Kutilmagan fors-major' holat yuz berdi (masalan, "
                "internet butunlay oʻchdi). Muammoni yechish koʻnikmasi yuqori boʻlgan rahbar birinchi boʻlib nima qiladi?"
            ),
            'options_ru': [
                'Впадает в панику и отменяет работу',
                'Собирает команду и запускает план альтернативных действий, спрашивая: «Какие задачи мы можем выполнять в офлайн-режиме?»',
                'Начинает судиться с интернет-провайдером', 'Отвечает всем, что подождёт, пока не появится интернет',
            ],
            'options_uz': [
                'Vahima koʻtarib, ishni bekor qiladi',
                'Jamoani toʻplab, "Oflayn rejimda qaysi topshiriqlarni bajarib turishimiz mumkin?" deb muqobil harakatlar rejasini ishga tushiradi',
                'Internet provayderi bilan sudlashishni boshlaydi', 'Internet yonguncha barchaga javob berib yuboradi',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-19', 'difficulty': 0.17,
            'category_ru': 'Логическое мышление', 'category_uz': 'Mantiqiy fikrlash',
            'prompt_ru': 'Как «Логические ошибки» (Fallacies) негативно влияют на решение проблем?',
            'prompt_uz': "'Mantiqiy xatolar' (Fallacies) muammoni yechishga qanday salbiy taʼsir koʻrsatadi?",
            'options_ru': [
                'Помогают быстрее решить проблему',
                'Приводят к неверной трактовке фактов и принятию неверных/необоснованных решений под влиянием эмоций',
                'Уточняют математические расчёты', 'Улучшают общение в команде',
            ],
            'options_uz': [
                'Muammoni tezroq hal qilishga yordam beradi',
                'Faktlarni notoʻgʻri talqin qilish va hissiyotlarga berilib, notoʻgʻri/asossiz qarorlar qabul qilishga olib keladi',
                'Matematik hisob-kitoblarni aniqlashtiradi', 'Jamoada muloqotni yaxshilaydi',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-20', 'difficulty': 0.23,
            'category_ru': 'Оценка результатов', 'category_uz': "Natijalarni baholash",
            'prompt_ru': 'После нахождения решения проблемы какой способ проверки его эффективности наиболее объективен?',
            'prompt_uz': 'Muammoning yechimini topgandan soʻng, uning samaradorligini tekshirishning eng xolis usuli qaysi?',
            'options_ru': [
                'Полагаться только на собственное мнение',
                'Сравнить состояние «до проблемы» и «после проблемы» с помощью KPI (ключевых показателей эффективности) и конкретных метрик (цифр, опросов)',
                'Сразу завершить проект и перейти к следующему', 'Услышать похвалу от других команд',
            ],
            'options_uz': [
                'Faqat oʻz fikringizga ishonish',
                'KPI (Asosiy samaradorlik koʻrsatkichlari) va aniq metrikalar (raqamlar, soʻrovnomalar) yordamida "Muammodan oldingi" va "Muammodan keyingi" holatni solishtirish',
                'Loyihani darhol yakunlab, keyingi loyihaga oʻtib ketish', 'Boshqa jamoalardan maqtov eshitish',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-core-21', 'difficulty': 0.3,
            'category_ru': 'Навыки будущего', 'category_uz': 'Kelajak koʻnikmalari',
            'prompt_ru': 'Почему навык «Решения проблем» (Problem-solving) считается самым востребованным качеством на рынке труда будущего?',
            'prompt_uz': "Nima uchun 'Muammoni yechish' (Problem-solving) koʻnikmasi kelajak mehnat bozorida eng talabgir xususiyat hisoblanadi?",
            'options_ru': [
                'Потому что люди с этим навыком никогда не ошибаются',
                'Потому что мир и технологии меняются очень быстро, готовые шаблоны быстро устаревают, и растёт потребность в специалистах, находящих решения нестандартных проблем',
                'Потому что это нужно только руководителям', 'Потому что это обязательный предмет в университетской программе',
            ],
            'options_uz': [
                'Bu koʻnikmaga ega insonlar hech qachon xato qilishmagani uchun',
                'Dunyo va texnologiyalar juda tez oʻzgarayotgani sababli, tayyor andozalar tezda eskiradi va nostandart muammolarga yechim topuvchi mutaxassislarga ehtiyoj yuqori boʻlib qolaveradi',
                'Faqat rahbarlarga kerak boʻlgani uchun', 'Universitet dasturida majburiy fan boʻlgani uchun',
            ],
            'correct_indices': [1],
        },
        # -- Longer "[Vaziyat]" situational scenarios — 10 questions -----------------------
        {
            'key': 'ps-scenario-1', 'difficulty': 0.4,
            'category_ru': 'Командная ответственность', 'category_uz': "Jamoaviy mas'uliyat",
            'prompt_ru': (
                'Вы вместе с одногруппником работаете над важным проектом. Завтра день сдачи проекта, но '
                'он сегодня внезапно заболел и сказал, что не сможет закончить свою часть. Ваши действия?'
            ),
            'prompt_uz': (
                "Kursdoshingiz bilan birgalikda muhim loyiha ustida ishlayapsiz. Ertaga loyihani topshirish "
                "kuni, biroq u bugun to'satdan kasal bo'lib qoldi va o'ziga tegishli qismni yakunlay olmasligini aytdi. Sizning harakatingiz?"
            ),
            'options_ru': [
                'Умоляю преподавателя перенести сдачу проекта на следующую неделю.',
                'Категорически требую от одногруппника закончить работу, даже несмотря на болезнь.',
                'Беру выполненную им часть и сам самостоятельно завершаю недостающие важные места ради общей цели, даже если придётся не спать всю ночь.',
                'Отказываюсь сдавать проект и сваливаю вину на одногруппника.',
            ],
            'options_uz': [
                "Loyihani topshirishni keyingi haftaga qoldirishni so'rab o'qituvchiga yolvoraman.",
                "Kursdoshimdan kasal bo'lsa ham ishni amallab tugatishini qat'iy talab qilaman.",
                "U bajargan qismini olib, yetishmayotgan muhim joylarini jamoaviy maqsad uchun tuni bilan bo'lsa ham o'zim mustaqil yakunlayman.",
                "Loyihani topshirishdan bosh tortaman va aybni kursdoshimga ag'daraman.",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-scenario-2', 'difficulty': 0.48,
            'category_ru': 'Пользовательский опыт', 'category_uz': "Foydalanuvchi tajribasi",
            'prompt_ru': (
                'Вы испытываете на уроке разработанную вами новую педагогическую программу. Но половина '
                'студентов испытывает трудности с использованием сложного интерфейса программы и не может выполнять задания. '
                'Как вы решите эту проблему?'
            ),
            'prompt_uz': (
                "Siz ishlab chiqqan yangi pedagogik dasturni darsda sinab ko'ryapsiz. Biroq talabalarning "
                "yarmi dastur interfeysi murakkabligi sababli undan foydalanishga qiynalib, topshiriqlarni bajara olmayapti. Muammoni qanday hal qilasiz?"
            ),
            'options_ru': [
                'Обвиняю студентов в том, что они плохо изучили программу, и отказываюсь её менять.',
                'Делаю использование программы обязательным, а тем, кто не справляется, ставлю низкую оценку.',
                'Прямо на уроке даю простую поясняющую мини-инструкцию (визуальную схему) по сложным частям, а после урока упрощаю программу на основе отзывов пользователей.',
                'Полностью удаляю программу и возвращаюсь к традиционной лекции.',
            ],
            'options_uz': [
                "Talabalarni yaxshilab o'rganmaganlikda ayblab, dasturni o'zgartirishdan bosh tortaman.",
                "Dasturdan foydalanishni majburiy qilib qo'yaman, kim bajara olmasa past baho qo'yaman.",
                "Darsning o'zida qiyin bo'lgan qismlarni sodda tushuntiruvchi mini-qo'llanma (vizual sxema) beraman va darsdan so'ng foydalanuvchilar fikri (faydbek) asosida dasturni soddalashtiraman.",
                "Dasturni butunlay o'chirib tashlab, an'anaviy ma'ruza darsiga qaytaman.",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-scenario-3', 'difficulty': 0.56,
            'category_ru': 'Управление кризисом (экзамен)', 'category_uz': "Inqiroz boshqaruvi (imtihon)",
            'prompt_ru': (
                'Во время сдачи экзамена в компьютерной системе произошёл сбой, и все ваши ответы, '
                'введённые за последние 20 минут, стёрлись. А времени до конца остаётся совсем мало. Что вы сделаете в первую очередь?'
            ),
            'prompt_uz': (
                "Imtihon topshirayotgan paytingizda kompyuter tizimida nosozlik yuz berdi va siz oxirgi 20 "
                "daqiqa davomida kiritgan barcha javoblaringiz o'chib ketdi. Vaqt tugashiga esa juda oz qoldi. Birinchi navbatda nima qilasiz?"
            ),
            'options_ru': [
                'Разнервничавшись, разобью монитор компьютера и выйду из аудитории.',
                'Немедленно позову проверяющего или технического сотрудника в аудитории, зафиксирую проблему (составлю акт) и попрошу возможность пересдать.',
                'Никому не сказав, за оставшееся короткое время наугад быстро отмечу все варианты.',
                'Сам самостоятельно попытаюсь разобрать и починить компьютерную систему.',
            ],
            'options_uz': [
                "Asabiylashib, kompyuter monitorini urib sindiraman va xonadan chiqib ketaman.",
                "Darhol xonadagi nazoratchi yoki texnik xodimni chaqirib, muammoni qayd ettiraman (akt tuzaman) va qayta topshirish imkonini so'rayman.",
                "Hech kimga aytmasdan, qolgan oz fursat ichida tavakkaliga hamma variantlarni tez-tez belgilab chiqaman.",
                "Kompyuter tizimini o'zim mustaqil ravishda ichini ochib tuzatishga harakat qilaman.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-scenario-4', 'difficulty': 0.64,
            'category_ru': 'Разрешение конфликтов (лидер)', 'category_uz': "Nizolarni hal qilish (rahbar)",
            'prompt_ru': (
                'Вы лидер в командном проекте. Два талантливых студента в группе высказали полностью '
                'противоположные мнения о стратегии реализации проекта, и между ними возник конфликт. Работа остановилась. '
                'Как вы решите эту проблему?'
            ),
            'prompt_uz': (
                "Jamoaviy loyihada siz yetakchisiz. Guruhdagi ikki iqtidorli talaba loyihani amalga oshirish "
                "strategiyasi bo'yicha mutloq qarama-qarshi fikr bildirdi va o'rtada nizo kelib chiqdi. Ish to'xtab qoldi. Muammoni qanday yechasiz?"
            ),
            'options_ru': [
                'Поддержу мнение того, у кого выше авторитет в группе.',
                'Исключу из группы обоих студентов за то, что не смогли разрешить конфликт.',
                'Составлю таблицу для объективного анализа аргументов обеих сторон и предложу гибридное решение, объединив элементы, наиболее подходящие и эффективные для цели проекта.',
                'Выберу совершенно случайный третий вариант, который понравится мне самому, не учитывая их мнение.',
            ],
            'options_uz': [
                "Kimning guruhda obro'si balandroq bo'lsa, o'shaning fikrini qo'llab-quvvatlayman.",
                "Nizoni hal qilolmaganliklari uchun ikkala talabani ham guruhdan haydayman.",
                "Ikkala tomonning ham argumentlarini xolis tahlil qilish uchun jadval tuzaman va loyiha maqsadiga eng mos, samarali keladigan elementlarni birlashtirib, gibrid yechim taklif qilaman.",
                "O'zimga yoqqan mutloq uchinchi tasodifiy yo'lni tanlayman va ularning fikrini inobatga olmayman.",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-scenario-5', 'difficulty': 0.72,
            'category_ru': 'Научный поиск', 'category_uz': "Ilmiy izlanish",
            'prompt_ru': (
                'Вам поручили сформировать список литературы для выпускной квалификационной работы '
                '(диссертации). Но выяснилось, что по искомой теме почти нет местных источников и книг. Как вы поступите?'
            ),
            'prompt_uz': (
                "Sizga bitiruv malakaviy ishi (dissertatsiya) uchun adabiyotlar ro'yxatini shakllantirish "
                "topshirildi. Biroq siz qidirayotgan mavzu bo'yicha mahalliy manbalar va kitoblar deyarli yo'q ekanligi ma'lum bo'ldi. Qanday yo'l tutasiz?"
            ),
            'options_ru': [
                'Сочту тему слишком сложной и попрошу научного руководителя дать другую готовую тему.',
                'Просто впишу в список названия совершенно других книг, близких к теме, подделав их.',
                'Обращусь к международным научным базам (Scopus, Google Scholar, CyberLeninka), переведу и проанализирую работы зарубежных учёных.',
                'Сдам работу некачественной и короткой, оправдываясь отсутствием материала по теме.',
            ],
            'options_uz': [
                "Mavzuni juda qiyin deb hisoblab, ilmiy rahbarimdan boshqa tayyor mavzu berishini so'rayman.",
                "Mavzuga yaqin bo'lgan mutloq boshqa kitoblarni shunchaki nomini ro'yxatga soxtalashtirib yozib qo'yaman.",
                "Xalqaro ilmiy bazalarga (Scopus, Google Scholar, CyberLeninka) murojaat qilib, xorijiy olimlarning ishlarini tarjima qilaman va tahlilga tortaman.",
                "Mavzu bo'yicha material yo'qligini bahona qilib, ishni sifatsiz va qisqa qilib topshiraman.",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-scenario-6', 'difficulty': 0.8,
            'category_ru': 'Оптимизация процесса', 'category_uz': "Jarayonni optimallashtirish",
            'prompt_ru': (
                'Вы проходите практику (стажировку) на предприятии. Руководитель поручил вам однообразную '
                'скучную механическую работу (ручной ввод данных в таблицу), занимающую 3 часа каждый день. '
                'Каким будет ваше эффективное решение в этой ситуации?'
            ),
            'prompt_uz': (
                "Siz korxonada amaliyot (stajirovka) o'tayapsiz. Rahbaringiz sizga har kuni 3 soat vaqt "
                "oladigan bir xil andozadagi zerikarli mexanik ishni (ma'lumotlarni qo'lda jadvalga kiritishni) topshirdi. "
                "Ushbu vaziyatda samarali yechimingiz qanday bo'ladi?"
            ),
            'options_ru': [
                'Из-за скуки перестану ходить на практику или буду просто тратить время впустую.',
                'Изучу способы автоматизации этого механического процесса (с помощью формул Excel, макросов или небольших скриптов) и предложу руководителю проект оптимизации.',
                'Пойду к руководителю и потребую давать мне не такую простую работу, а только крупные проекты.',
                'Заплачу другому студенту-практиканту, чтобы он выполнил работу за меня.',
            ],
            'options_uz': [
                "Ish juda zerikarli bo'lgani uchun amaliyotga bormay qo'yaman yoki vaqtni shunchaki o'tkazaman.",
                "Ushbu mexanik jarayonni avtomatlashtirish yo'llarini (Excel formulalari, makroslar yoki kichik skriptlar yordamida) o'rganib chiqib, rahbarimga optimallashtirish loyihasini taklif qilaman.",
                "Rahbarga borib, menga bunday oddiy ishlar emas, faqat katta loyihalar berishini talab qilaman.",
                "Ishni boshqa bir amaliyotchi talabaga pul berib bajartiraman.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-scenario-7', 'difficulty': 0.88,
            'category_ru': 'Навыки презентации (под давлением)', 'category_uz': "Taqdimot koʻnikmalari (bosim ostida)",
            'prompt_ru': (
                'Вам нужно защитить свой стартап-проект перед инвесторами. Вам было отведено 10 минут, но '
                'когда вы вошли в зал, вам сказали, что время неожиданно сократили до 2 минут. А у вас 20 слайдов. Что вы сделаете?'
            ),
            'prompt_uz': (
                "Startup loyihangizni investorlar oldida himoya qilishingiz kerak. Sizga 10 daqiqa vaqt "
                "berilgan edi, biroq zalga kirganingizda vaqt kutilmaganda 2 daqiqaga qisqartirilganini aytishdi. Slaydlaringiz esa 20 tadan iborat. Nima qilasiz?"
            ),
            'options_ru': [
                'Расстроившись из-за сокращения времени, полностью откажусь от презентации.',
                'Попытаюсь очень быстро проговорить все 20 слайдов, уложившись во время.',
                'Пролистаю слайды и дам чёткий и лаконичный ответ только на 3 главных вопроса: в чём проблема, каково наше решение и какой доход принесёт проект (суть).',
                'Начну спорить с инвесторами, требуя не сокращать время.',
            ],
            'options_uz': [
                "Vaqt qisqarib ketganidan norozi bo'lib, taqdimot qilishdan butunlay voz kechaman.",
                "20 ta slaydning hammasini juda tez gapirib, vaqtga sig'dirishga harakat qilaman.",
                "Slaydlarni varaqlab o'tib, faqat eng asosiy 3 ta narsaga: Muammo nima, Bizning yechim qanday va Loyihaning qancha daromad keltiradi (mag'zi) degan savollarga aniq va lo'nda javob beraman.",
                "Investorlardan vaqtni qisqartirmaslikni talab qilib, ular bilan bahslashaman.",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-scenario-8', 'difficulty': 0.96,
            'category_ru': 'Отладка (диагностика)', 'category_uz': "Xatoliklarni bartaraf etish",
            'prompt_ru': (
                'Вы создали педагогический программный инструмент и провели его alpha-тестирование '
                '(предварительное испытание). В результате в логических алгоритмах программы обнаружена '
                'неожиданная системная ошибка (баг). Каким будет ваш первый шаг в устранении проблемы?'
            ),
            'prompt_uz': (
                "Siz pedagogik dasturiy vosita yaratdingiz va uni alpha-testing (dastlabki sinov) jarayonidan "
                "o'tkazdingiz. Natijada dasturning mantiqiy algoritmlarida kutilmagan tizimli xatolik (bug) aniqlandi. Muammoni bartaraf etishda birinchi qadamingiz?"
            ),
            'options_ru': [
                'Сделаю вид, что не заметил ошибку, и продолжу продавать финальную версию программы.',
                'Полностью удалю программу и начну писать весь код заново.',
                'Применю метод декомпозиции: разделю код на модули для выявления проблемы и по логам диагностирую, какой именно алгоритмический критерий (условие) работает неправильно.',
                'Свалю вину на компьютеры пользователей, тестировавших программу.',
            ],
            'options_uz': [
                "Xatolikni sezmaganga olib, dasturning yakuniy versiyasini sotaveraman.",
                "Dasturni butunlay o'chirib tashlab, hamma kodni boshidan yozishni boshlayman.",
                "Dekompozitsiya metodini qo'llayman: muammoni aniqlash uchun kodni modullarga bo'lib, aynan qaysi algoritmik kriteriy (shart) xato ishlayotganini loglar orqali diagnostika qilaman.",
                "Aybni dasturni sinab ko'rgan foydalanuvchilarning kompyuteriga ag'daraman.",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'ps-scenario-9', 'difficulty': 1.04,
            'category_ru': 'Творческая адаптация', 'category_uz': "Ijodiy moslashuv",
            'prompt_ru': (
                'В рамках недели «Цифрового образования» в университете вам нужно организовать семинар для '
                'студентов, но в университете внезапно полностью отключилось электричество. Не работают ни интернет, ни проектор. '
                'Как вы спасёте семинар?'
            ),
            'prompt_uz': (
                "Universitetda 'Raqamli ta'lim' haftaligi doirasida talabalar o'rtasida seminar tashkil "
                "etishingiz kerak, biroq universitetda to'satdan elektr energiyasi (chiroq) butunlay o'chib qoldi. Internet ham, "
                "proektor ham ishlamayapti. Seminarni qanday saqlab qolasiz?"
            ),
            'options_ru': [
                'Сославшись на отсутствие света, перенесу семинар на другой день и отпущу всех студентов.',
                'Переведу семинар в интерактивный формат: нарисую идеи из презентационных слайдов на доске (или бумаге) и продолжу его в виде живой дискуссии со студентами (вопросы-ответы и мозговой штурм).',
                'Заставлю студентов просто ждать в зале 2 часа, пока не включат свет.',
                'Включу фонарик телефона и буду скучно зачитывать студентам текст из конспекта.',
            ],
            'options_uz': [
                "Chiroq yo'qligini sabab qilib, seminarni boshqa kunga ko'chiraman va hamma talabalarga javob berib yuboraman.",
                "Seminarni interaktiv formatga o'tkazaman: taqdimot slaydlaridagi g'oyalarni doskada (yoki qog'ozda) chizib, talabalar bilan jonli munozara (savol-javob va aqliy hujum) ko'rinishida davom ettiraman.",
                "Chiroq yonguncha talabalarni zalda 2 soat shunchaki kutishga majbur qilaman.",
                "Telefonim chirog'ini yoqib, konspektdagi matnlarni talabalarga zerikarli qilib o'qib beraman.",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'ps-scenario-10', 'difficulty': 1.12,
            'category_ru': 'Наставничество', 'category_uz': "Murabbiylik",
            'prompt_ru': (
                'Вы староста группы. Одногруппник регулярно пропускает занятия и находится на грани '
                'провала итогового экзамена. Что вы сделаете, чтобы системно решить проблему, вместо того чтобы наказывать его или доносить преподавателю?'
            ),
            'prompt_uz': (
                "Siz guruh sardorisiz. Guruhdoshingiz darslarni muntazam qoldirmoqda va yakuniy imtihondan "
                "yiqilish arafasida. Uni jazolash yoki o'qituvchiga sotish o'rniga, muammoni tizimli hal qilish uchun nima qilasiz?"
            ),
            'options_ru': [
                'Исключу его из группового чата и прекращу с ним общение.',
                'Лично поговорю с ним, выясню истинную причину пропусков (возможно, материальные, семейные проблемы или проблемы со здоровьем) и организую от имени группы академическую помощь (консультации) для него.',
                'Буду выполнять за него все занятия и задания, обманывая преподавателей.',
                'Вообще не буду вмешиваться в ситуацию, считая это его личным делом.',
            ],
            'options_uz': [
                "Uni guruh guruhidan chiqarib yuboraman va u bilan aloqani uzaman.",
                "U bilan shaxsan suhbatlashib, dars qoldirishining tub sababini (balki moddiy, oilaviy yoki sog'liq muammosi borligini) aniqlayman va guruh nomidan unga akademik yordam (konsultatsiya) tashkil qilaman.",
                "Uning o'rniga barcha dars va topshiriqlarni o'zim bajarib, o'qituvchilarni aldayman.",
                "Vaziyatga umuman aralashmayman, chunki bu uning shaxsiy ishi deb hisoblayman.",
            ],
            'correct_indices': [1],
        },
    ],
    'attention': [
        {
            'key': 'attn-exact-match-1', 'difficulty': -0.8,
            'category_ru': 'Точность сопоставления', 'category_uz': 'Moslikni aniqlash',
            'prompt_ru': 'Образец: 7392846. Какой из вариантов ТОЧНО совпадает с образцом?',
            'prompt_uz': 'Namuna: 7392846. Qaysi variant namuna bilan ANIQ mos keladi?',
            'options_ru': ['7392846', '7392864', '7398246', '7329846'],
            'options_uz': ['7392846', '7392864', '7398246', '7329846'],
            'correct_indices': [0],
        },
        {
            'key': 'attn-spelling-1', 'difficulty': -0.3,
            'category_ru': 'Вычитка', 'category_uz': "Matnni tekshirish",
            'prompt_ru': 'Какое слово написано с ошибкой?', 'prompt_uz': "Qaysi so'z xato yozilgan?",
            'options_ru': ['Расписание', 'Режисёр', 'Параллельный', 'Симметрия'],
            'options_uz': ['Kutubxona', 'Proffesor', 'Tasviriy', 'Universitet'],
            'correct_indices': [1],
        },
        {
            'key': 'attn-letter-count-1', 'difficulty': 0.1,
            'category_ru': 'Подсчёт деталей', 'category_uz': 'Detallarni sanash',
            'prompt_ru': 'Сколько раз буква «о» встречается в слове «мировоззрение»?',
            'prompt_uz': "«Tabiatshunoslik» so'zida «a» harfi necha marta uchraydi?",
            'options_ru': ['1', '2', '3', '4'], 'options_uz': ['1', '2', '3', '4'],
            'correct_indices': [1],
        },
        {
            'key': 'attn-pattern-break-1', 'difficulty': 0.4,
            'category_ru': 'Обнаружение сбоя в узоре', 'category_uz': 'Naqshdagi uzilishni topish',
            'prompt_ru': 'Узор должен повторяться как "● ● ▲". В последовательности "●●▲●●▲●●●" на какой позиции нарушен порядок?',
            'prompt_uz': 'Naqsh "● ● ▲" tarzida takrorlanishi kerak. "●●▲●●▲●●●" ketma-ketligida qaysi pozitsiyada tartib buzilgan?',
            'options_ru': ['3', '6', '9', 'Нет ошибки'], 'options_uz': ['3', '6', '9', "Xato yo'q"],
            'correct_indices': [2],
        },
        {
            'key': 'attn-row-compare-1', 'difficulty': 0.7,
            'category_ru': 'Сравнение рядов данных', 'category_uz': "Ma'lumotlar qatorini solishtirish",
            'prompt_ru': (
                'Сравните две строки: А: 58273 61094 30852   Б: 58273 61094 30582. '
                'В каком числе есть различие?'
            ),
            'prompt_uz': (
                "Ikki qatorni solishtiring: A: 58273 61094 30852   B: 58273 61094 30582. "
                "Qaysi sonda farq bor?"
            ),
            'options_ru': ['В первом числе (58273)', 'Во втором числе (61094)', 'В третьем числе (30852/30582)', 'Строки идентичны'],
            'options_uz': ['Birinchi sonda (58273)', 'Ikkinchi sonda (61094)', 'Uchinchi sonda (30852/30582)', 'Qatorlar bir xil'],
            'correct_indices': [2],
        },
    ],
    'iq': [
        {
            'key': 'iq-series-1', 'difficulty': -0.7,
            'category_ru': 'Числовые ряды', 'category_uz': 'Sonli qatorlar',
            'prompt_ru': 'Продолжите ряд: 3, 6, 11, 18, 27, ?', 'prompt_uz': 'Qatorni davom ettiring: 3, 6, 11, 18, 27, ?',
            'options_ru': ['36', '38', '40', '42'], 'options_uz': ['36', '38', '40', '42'],
            'correct_indices': [1],
        },
        {
            'key': 'iq-odd-one-out-1', 'difficulty': -0.2,
            'category_ru': 'Классификация', 'category_uz': 'Klassifikatsiya',
            'prompt_ru': 'Какое слово не подходит к остальным: Квадрат, Треугольник, Круг, Тяжёлый?',
            'prompt_uz': "Qaysi so'z boshqalariga mos kelmaydi: Kvadrat, Uchburchak, Doira, Og'ir?",
            'options_ru': ['Квадрат', 'Треугольник', 'Круг', 'Тяжёлый'],
            'options_uz': ['Kvadrat', 'Uchburchak', 'Doira', "Og'ir"],
            'correct_indices': [3],
        },
        {
            'key': 'iq-analogy-1', 'difficulty': 0.1,
            'category_ru': 'Аналогии', 'category_uz': 'Analogiyalar',
            'prompt_ru': 'Рука относится к Перчатке, как Нога относится к ___',
            'prompt_uz': "Qo'l Qo'lqopga qanday munosabatda bo'lsa, Oyoq ___ ga shunday munosabatda bo'ladi",
            'options_ru': ['Обуви', 'Руке', 'Голове', 'Шляпе'],
            'options_uz': ["Poyabzalga", "Qo'lga", "Boshga", "Shlyapaga"],
            'correct_indices': [0],
        },
        {
            'key': 'iq-shape-pattern-1', 'difficulty': 0.4,
            'category_ru': 'Пространственные узоры', 'category_uz': 'Fazoviy naqshlar',
            'prompt_ru': (
                'В ряду фигур каждая следующая имеет на одну сторону больше предыдущей: '
                'треугольник, квадрат, пятиугольник, ?. Какая фигура следующая?'
            ),
            'prompt_uz': (
                "Shakllar qatorida har bir keyingisi oldingisidan bitta ko'proq tomonga ega: "
                "uchburchak, kvadrat, beshburchak, ?. Keyingi shakl qaysi?"
            ),
            'options_ru': ['Шестиугольник', 'Семиугольник', 'Круг', 'Ромб'],
            'options_uz': ["Oltiburchak", "Yettiburchak", "Doira", "Romb"],
            'correct_indices': [0],
        },
        {
            'key': 'iq-combinatorics-1', 'difficulty': 0.9,
            'category_ru': 'Комбинаторика', 'category_uz': 'Kombinatorika',
            'prompt_ru': 'В спортивной секции 5 человек. Каждый пожал руку каждому один раз. Сколько всего было рукопожатий?',
            'prompt_uz': "Sport to'garagida 5 kishi bor. Har biri boshqasi bilan bir marta qo'l siqishdi. Jami nechta qo'l siqish bo'ldi?",
            'options_ru': ['8', '10', '12', '20'], 'options_uz': ['8', '10', '12', '20'],
            'correct_indices': [1],
        },
    ],
    'algorithmic': [
        {
            'key': 'algorithmic-boolean-1', 'difficulty': -1.0,
            'category_ru': 'Логические операции', 'category_uz': 'Mantiqiy amallar',
            'prompt_ru': 'Если A = «Истина», а B = «Ложь», каков результат операции логического умножения (AND / И)?',
            'prompt_uz': "Agar A = \"Rost\" va B = \"Yolg'on\" bo'lsa, mantiqiy ko'paytirish (AND / VA) amali bajarilganda natija nima bo'ladi?",
            'options_ru': ['Истина', 'Ложь', 'Нельзя определить', 'И истина, и ложь одновременно'],
            'options_uz': ['Rost', "Yolg'on", "Aniqlab bo'lmaydi", 'Ham rost, ham yolg\'on'],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-flowchart-1', 'difficulty': -0.9,
            'category_ru': 'Блок-схемы', 'category_uz': 'Blok-sxemalar',
            'prompt_ru': 'В блок-схемах проверка условия (да/нет, истина/ложь) обычно записывается внутри какой геометрической фигуры?',
            'prompt_uz': "Blok-sxemalarda shartni tekshirish (ha/yo'q, rost/yolg'on) odatda qaysi geometrik shakl ichida yoziladi?",
            'options_ru': ['Прямоугольник', 'Ромб', 'Овал', 'Параллелограмм'],
            'options_uz': ["To'g'ri to'rtburchak", 'Romb', 'Oval', 'Parallelogramm'],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-linear-structure-1', 'difficulty': -0.8,
            'category_ru': 'Структуры алгоритма', 'category_uz': 'Algoritm tuzilmalari',
            'prompt_ru': 'Что понимается под линейной структурой в алгоритме?',
            'prompt_uz': 'Algoritmdagi chiziqli tuzilma deganda nima tushuniladi?',
            'options_ru': [
                'Выполнение шагов в разных направлениях в зависимости от условия', 'Бесконечное повторение шагов',
                'Выполнение шагов последовательно, одно за другим, без каких-либо условий', 'Полная неработоспособность алгоритма',
            ],
            'options_uz': [
                "Qadamlarning shartga qarab har xil yo'nalishda bajarilishi", 'Qadamlarning cheksiz takrorlanishi',
                "Qadamlarning hech qanday shartsiz, ketma-ket, birin-ketin bajarilishi", 'Algoritmning umuman ishlamasligi',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'algorithmic-property-finiteness-1', 'difficulty': -0.7,
            'category_ru': 'Свойства алгоритма', 'category_uz': 'Algoritm xossalari',
            'prompt_ru': 'Одно из важнейших свойств, которым должен обладать любой алгоритм, — конечность. Что это означает?',
            'prompt_uz': "Har qanday algoritm ega bo'lishi kerak bo'lgan eng muhim xususiyatlardan biri — cheklanganlikdir. Bu nima degani?",
            'options_ru': [
                'Алгоритм должен работать только на компьютере.', 'Алгоритм должен быть сложным.',
                'Алгоритм обязан прийти к логическому завершению за конечное число шагов.', 'Алгоритм должен понимать только один человек.',
            ],
            'options_uz': [
                'Algoritm faqat kompyuterda ishlashi kerak.', 'Algoritm qiyin bo\'lishi kerak.',
                'Algoritm chekli qadamlardan keyin mantiqiy yakuniga yetishi shart.', 'Algoritmni faqat bir kishi tushunishi kerak.',
            ],
            'correct_indices': [2],
        },
        {
            'key': 'algorithmic-recursion-1', 'difficulty': -0.5,
            'category_ru': 'Рекурсия', 'category_uz': 'Rekursiya',
            'prompt_ru': 'Что такое рекурсия?',
            'prompt_uz': 'Rekursiya nima?',
            'options_ru': [
                'Остановка алгоритма из-за ошибки.', 'Обращение функции или алгоритма к самому себе (самовызов).',
                'Сортировка данных в алфавитном порядке.', 'Удаление программы из памяти.',
            ],
            'options_uz': [
                "Algoritmning xatolikka uchrab to'xtab qolishi.", "Funksiya yoki algoritmning o'z-o'ziga qayta murojaat qilishi (o'zini o'zi chaqirishi).",
                "Ma'lumotlarni alifbo tartibida saralash.", 'Dasturni xotiradan o\'chirib tashlash.',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-trace-1', 'difficulty': -0.4,
            'category_ru': 'Трассировка алгоритма', 'category_uz': 'Algoritmni kuzatish',
            'prompt_ru': 'Проанализируйте данную последовательность: X = 5. На следующем шаге X = X + 3. Затем X = X * 2. Чему будет равен X в конце алгоритма?',
            'prompt_uz': "Berilgan ketma-ketlikni tahlil qiling: X = 5. Keyingi qadamda X = X + 3. Undan keyingi qadamda X = X * 2. Algoritm yakunida X nechaga teng bo'ladi?",
            'options_ru': ['11', '13', '16', '26'], 'options_uz': ['11', '13', '16', '26'],
            'correct_indices': [2],
        },
        {
            'key': 'algorithmic-loop-1', 'difficulty': -0.6,
            'category_ru': 'Циклы', 'category_uz': 'Sikllar',
            'prompt_ru': 'Сколько раз выполнится следующий цикл? Условие цикла: i = 1; Пока i < 5, выполнять: i = i + 1.',
            'prompt_uz': "Quyidagi sikl (takrorlanish) necha marta bajariladi? Sikl sharti: i = 1; Toki i < 5 bo'lguncha bajarilsin: i = i + 1.",
            'options_ru': ['5 раз', '4 раза', '3 раза', 'Бесконечное число раз'],
            'options_uz': ['5 marta', '4 marta', '3 marta', 'Cheksiz marta'],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-infinite-loop-1', 'difficulty': -0.3,
            'category_ru': 'Циклы', 'category_uz': 'Sikllar',
            'prompt_ru': 'Что логически называется «бесконечным циклом» (Infinite loop)?',
            'prompt_uz': '"Cheksiz sikl" (Infinite loop) mantiqan nimaga aytiladi?',
            'options_ru': [
                'Программе, которая работает очень быстро', 'Процессу, условие выхода из которого никогда не выполняется, и он не останавливается',
                'Функции, полностью очищающей память', 'Коду, состоящему только из 0 и 1',
            ],
            'options_uz': [
                'Juda tez ishlaydigan dasturga', "Sikldan chiqish sharti hech qachon bajarilmaydigan va to'xtamaydigan jarayonga",
                'Xotirani butunlay tozalaydigan funksiyaga', 'Faqat 0 va 1 lardan iborat kodga',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-robot-1', 'difficulty': -0.2,
            'category_ru': 'Алгоритмическая симуляция', 'category_uz': 'Algoritmik simulyatsiya',
            'prompt_ru': (
                'Если роботу задан следующий алгоритм, в какую точку он придёт в итоге? '
                'Алгоритм: 3 шага вперёд, 2 шага вправо, 1 шаг назад, 2 шага влево.'
            ),
            'prompt_uz': (
                "Agar robotga quyidagi algoritm berilgan bo'lsa, u oxirida qaysi nuqtaga boradi? "
                "Algoritm: 3 qadam oldinga, 2 qadam o'ngga, 1 qadam orqaga, 2 qadam chapga."
            ),
            'options_ru': [
                'На 3 шага впереди начальной точки', 'На 2 шага правее начальной точки',
                'На 2 шага впереди начальной точки (право-лево компенсируются; 3 шага вперёд минус 1 шаг назад = 2 шага)',
                'Возвращается в начальную точку',
            ],
            'options_uz': [
                "Boshlang'ich nuqtadan 3 qadam oldinda", "Boshlang'ich nuqtadan 2 qadam o'ngda",
                "Boshlang'ich nuqtadan 2 qadam oldinda (o'ng-chap bir-birini yo'qqa chiqaradi; 3 qadam oldinga minus 1 qadam orqaga = 2 qadam)",
                "Boshlang'ich nuqtaga qaytib keladi",
            ],
            'correct_indices': [2],
        },
        {
            'key': 'algorithmic-property-definiteness-1', 'difficulty': 0.2,
            'category_ru': 'Свойства алгоритма', 'category_uz': 'Algoritm xossalari',
            'prompt_ru': 'Что означает свойство результативности алгоритма?',
            'prompt_uz': 'Algoritmning natijaviylik xususiyati nimani anglatadi?',
            'options_ru': [
                'Что алгоритм должен быть очень длинным', 'Что после определённых шагов будет получен ожидаемый точный результат или сообщение об ошибке',
                'Что программа должна иметь только красивый дизайн', 'Что алгоритм решает только математические задачи',
            ],
            'options_uz': [
                'Algoritm juda uzun bo\'lishi kerakligini', "Ma'lum bir qadamlardan keyin kutilgan aniq natija yoki xatolik haqida xabar olinishini",
                'Dasturning faqat chiroyli dizaynga ega bo\'lishini', 'Algoritm faqat matematik masalalarni yechishini',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-stack-1', 'difficulty': 0.1,
            'category_ru': 'Структуры данных', 'category_uz': "Ma'lumotlar tuzilmalari",
            'prompt_ru': 'По какому алгоритмическому правилу обрабатываются элементы в структуре данных Stack (Стек)?',
            'prompt_uz': "Stack (Stek) ma'lumotlar tuzilmasida elementlar qaysi algoritmik qoida asosida qayta ishlanadi?",
            'options_ru': [
                'FIFO (First In, First Out — первый пришёл, первый вышел)', 'LIFO (Last In, First Out — последний пришёл, первый вышел)',
                'В случайном порядке', 'Извлекаются только элементы из середины',
            ],
            'options_uz': [
                'FIFO (First In, First Out - Birinchi kelgan, birinchi ketadi)', 'LIFO (Last In, First Out - Oxirgi kelgan, birinchi ketadi)',
                'Tasodifiy tartibda', "Faqat o'rtadagi elementlar olinadi",
            ],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-sequence-1', 'difficulty': 0.3,
            'category_ru': 'Последовательность действий', 'category_uz': 'Ketma-ketlik',
            'prompt_ru': (
                'Телефон разрядился. Определите правильную последовательность действий алгоритма его включения: '
                '1) Подключить к зарядному устройству. 2) Удерживать кнопку включения. '
                '3) Дождаться, пока загорится экран. 4) Проверить процент заряда (если 0%).'
            ),
            'prompt_uz': (
                "Telefon o'chib qoldi. Uni yoqish algoritmining to'g'ri ketma-ketligini aniqlang: "
                "1) Quvvatlash qurilmasiga ulash. 2) Yoqish tugmasini bosib turish. "
                "3) Ekran yonguncha kutish. 4) Quvvat foizini tekshirish (agar 0% bo'lsa)."
            ),
            'options_ru': ['2, 3, 1, 4', '4, 1, 2, 3', '1, 2, 3, 4', '4, 2, 1, 3'],
            'options_uz': ['2, 3, 1, 4', '4, 1, 2, 3', '1, 2, 3, 4', '4, 2, 1, 3'],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-conditional-1', 'difficulty': 0.4,
            'category_ru': 'Условные операторы', 'category_uz': 'Shartli operatorlar',
            'prompt_ru': (
                '«Если урок начался и студент опоздал, пусть не заходит в аудиторию, иначе пусть садится на своё место.» '
                'Студент не опоздал, но урок ещё не начался. Что он должен сделать согласно алгоритму?'
            ),
            'prompt_uz': (
                '"Agar dars boshlangan bo\'lsa va talaba kechikkan bo\'lsa, u xonaga kirmasin, aks holda joyiga o\'tirsin." '
                "Talaba kechikmadi, lekin dars hali boshlanmagan. Algoritmga ko'ra u nima qilishi kerak?"
            ),
            'options_ru': [
                'Не должен заходить в аудиторию', 'Должен сесть на своё место',
                'Должен подождать в коридоре', 'В алгоритме есть ошибка',
            ],
            'options_uz': [
                'Xonaga kirmasligi kerak', "Joyiga o'tirishi kerak",
                "Yo'lakda kutishi kerak", 'Algoritmda xatolik bor',
            ],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-bubble-sort-1', 'difficulty': 0.5,
            'category_ru': 'Алгоритмы сортировки', 'category_uz': 'Saralash algoritmlari',
            'prompt_ru': (
                'Дан массив (список): [8, 3, 5, 1]. При упорядочивании по возрастанию с помощью пузырьковой '
                'сортировки (Bubble sort), какие два числа поменяются местами на первом шаге?'
            ),
            'prompt_uz': (
                "Massiv (ro'yxat) berilgan: [8, 3, 5, 1]. Uni ko'pikli saralash (Bubble sort) algoritmi yordamida "
                "o'sish tartibida joylashtirishda birinchi qadamda qaysi ikkita son o'rin almashadi?"
            ),
            'options_ru': ['3 и 5', '5 и 1', '8 и 3', 'Ни одно из них не меняется местами'],
            'options_uz': ['3 va 5', '5 va 1', '8 va 3', 'Hech biri almashmaydi'],
            'correct_indices': [2],
        },
        {
            'key': 'algorithmic-traffic-light-1', 'difficulty': 0.6,
            'category_ru': 'Циклические процессы', 'category_uz': 'Davriy jarayonlar',
            'prompt_ru': (
                'Если алгоритм светофора выглядит так: Красный -> Жёлтый -> Зелёный -> Жёлтый -> Красный. '
                'Какой цвет загорится при 11-й смене состояния (начальное состояние — Красный)?'
            ),
            'prompt_uz': (
                "Agar svetofor algoritmi quyidagicha bo'lsa: Qizil -> Sariq -> Yashil -> Sariq -> Qizil. "
                "Tizim 11-marta o'zgarganda qaysi rang yonadi (boshlang'ich holat - Qizil)?"
            ),
            'options_ru': ['Красный', 'Жёлтый', 'Зелёный', 'Светофор выключается'],
            'options_uz': ['Qizil', 'Sariq', 'Yashil', "Svetofor o'chadi"],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-weighing-1', 'difficulty': 0.7,
            'category_ru': 'Оптимизация', 'category_uz': 'Optimallashtirish',
            'prompt_ru': 'У вас есть 3 монеты, одна из них фальшивая (легче остальных). За какое минимальное число взвешиваний на чашечных весах можно точно найти фальшивую монету?',
            'prompt_uz': "Sizda 3 ta tanga bor, ulardan biri soxta (yengilroq). Pallali tarozida minimal necha marta tortish orqali soxta tangani aniq topish mumkin?",
            'options_ru': ['1 раз', '2 раза', '3 раза', 'Найти невозможно'],
            'options_uz': ['1 marta', '2 marta', '3 marta', "Topib bo'lmaydi"],
            'correct_indices': [0],
        },
        {
            'key': 'algorithmic-binary-search-1', 'difficulty': 0.8,
            'category_ru': 'Алгоритмы поиска', 'category_uz': 'Qidiruv algoritmlari',
            'prompt_ru': (
                'Алгоритм поиска: у вас есть отсортированные числа от 1 до 100. Чтобы найти число 75 с помощью '
                'бинарного поиска (деления пополам), какое число проверяется первым?'
            ),
            'prompt_uz': (
                "Qidiruv algoritmi: Sizda 1 dan 100 gacha tartiblangan raqamlar bor. Binoriy qidiruv (o'rtadan bo'lish) "
                "algoritmi orqali 75 sonini topish uchun birinchi bo'lib qaysi son tekshiriladi?"
            ),
            'options_ru': ['25', '50', '75', '1'], 'options_uz': ['25', '50', '75', '1'],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-recursion-2', 'difficulty': 0.9,
            'category_ru': 'Рекурсия', 'category_uz': 'Rekursiya',
            'prompt_ru': (
                'Найдите значение по следующему рекурсивному правилу: F(1) = 1; F(2) = 2; каждое следующее '
                'F(n) = F(n-1) + F(n-2). Чему равно F(4)?'
            ),
            'prompt_uz': (
                "Quyidagi rekursiv qoida bo'yicha uchinchi elementni toping: F(1) = 1; F(2) = 2; Har bir keyingi "
                "F(n) = F(n-1) + F(n-2). F(4) nechaga teng?"
            ),
            'options_ru': ['3', '5', '4', '6'], 'options_uz': ['3', '5', '4', '6'],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-swap-1', 'difficulty': 1.0,
            'category_ru': 'Практические алгоритмы', 'category_uz': 'Amaliy algoritmlar',
            'prompt_ru': 'На каких математических операциях основан алгоритм обмена значений двух переменных без использования третьей вспомогательной переменной?',
            'prompt_uz': "Ikki o'zgaruvchining qiymatini uchinchi qo'shimcha o'zgaruvchisiz almashtirish algoritmi qaysi matematik amallarga asoslanadi?",
            'options_ru': ['Только умножение и деление', 'Сложение и вычитание (или операция XOR)', 'Только возведение в степень', 'Значения нельзя поменять местами'],
            'options_uz': ['Faqat ko\'paytirish va bo\'lish', "Qo'shish va ayirish (yoki XOR amali)", 'Faqat darajaga ko\'tarish', "Qiymatlarni almashtirib bo'lmaydi"],
            'correct_indices': [1],
        },
        {
            'key': 'algorithmic-code-trace-1', 'difficulty': -0.1,
            'category_ru': 'Трассировка кода', 'category_uz': 'Kod trassirovkasi',
            'prompt_ru': (
                'Определите результат следующего фрагмента кода: x = 10; y = 20; if (x > y) { x = x + 5; } '
                'else { y = y + 5; } Каковы итоговые значения x и y?'
            ),
            'prompt_uz': (
                'Quyidagi kod qismining natijasini aniqlang: x = 10; y = 20; if (x > y) { x = x + 5; } '
                "else { y = y + 5; } Yakuniy x va y qiymatlari qancha?"
            ),
            'options_ru': ['x = 15, y = 20', 'x = 10, y = 20', 'x = 10, y = 25', 'x = 15, y = 25'],
            'options_uz': ['x = 15, y = 20', 'x = 10, y = 20', 'x = 10, y = 25', 'x = 15, y = 25'],
            'correct_indices': [2],
        },
    ],
}

CODING_PROBLEM = {
    'slug': 'most-frequent-word',
    'title_ru': 'Самое частое слово',
    'title_uz': "Eng ko'p uchraydigan so'z",
    'statement_ru': (
        'Напишите функцию, которая принимает предложение и возвращает слово, встречающееся чаще '
        'всего. При равенстве частот побеждает слово, встретившееся первым. Игнорируйте пунктуацию '
        'и регистр.'
    ),
    'statement_uz': (
        "Gapni qabul qilib, unda eng ko'p uchraydigan so'zni qaytaruvchi funksiya yozing. Chastotalar "
        "teng bo'lsa, birinchi uchragan so'z g'olib hisoblanadi. Tinish belgilari va katta-kichik "
        "harflarga e'tibor bermang."
    ),
    'example_ru': 'Вход:  "the cat sat on the mat"\nВыход: "the"',
    'example_uz': 'Kirish:  "the cat sat on the mat"\nChiqish: "the"',
    'constraints_ru': [
        '1 ≤ длина предложения ≤ 10 000 символов',
        'Слова разделены одиночными пробелами',
        'Сравнение не чувствительно к регистру',
    ],
    'constraints_uz': [
        '1 ≤ gap uzunligi ≤ 10 000 belgi',
        "So'zlar bitta bo'sh joy bilan ajratilgan",
        "Solishtirish katta-kichik harflarga bog'liq emas",
    ],
    'starter_code_ru': (
        'function mostFrequentWord(sentence) {\n'
        '  const counts = {};\n'
        '  const words = sentence.toLowerCase().split(" ");\n\n'
        '  for (const w of words) {\n'
        '    counts[w] = (counts[w] || 0) + 1;\n'
        '  }\n\n'
        '  // TODO: верните слово с наибольшим количеством повторений\n'
        '}'
    ),
    'starter_code_uz': (
        'function mostFrequentWord(sentence) {\n'
        '  const counts = {};\n'
        '  const words = sentence.toLowerCase().split(" ");\n\n'
        '  for (const w of words) {\n'
        '    counts[w] = (counts[w] || 0) + 1;\n'
        '  }\n\n'
        "  // TODO: eng ko'p takrorlangan so'zni qaytaring\n"
        '}'
    ),
    'test_cases': [
        {'label': "'the cat sat on the mat' → 'the'", 'input': 'the cat sat on the mat', 'expected': 'the', 'hidden': False},
        {'label': "'a b b c c c' → 'c'", 'input': 'a b b c c c', 'expected': 'c', 'hidden': False},
        {'label': "'The Cat sat' → 'the' (case-insensitive)", 'input': 'The Cat sat', 'expected': 'the', 'hidden': True},
    ],
}

LIKERT_CATEGORIES = {
    'teamwork': {
        'label_ru': 'КОМАНДНАЯ РАБОТА', 'label_uz': 'JAMOAVIY ISH',
        'items': [
            {
                'key': 'teamwork_positive_1', 'reverse_scored': False,
                'text_ru': 'Мне нравится объяснять свои рассуждения товарищам по команде при решении задачи.',
                'text_uz': "Masalani yechishda o'z fikrlash yo'limni jamoadoshlarga tushuntirishni yoqtiraman.",
            },
            {
                'key': 'teamwork_negative_1', 'reverse_scored': True,
                'text_ru': 'Я предпочитаю решать задачи полностью самостоятельно.',
                'text_uz': "Masalalarni butunlay yolg'iz hal qilishni afzal ko'raman.",
            },
            {
                'key': 'teamwork_positive_2', 'reverse_scored': False,
                'text_ru': 'Я с готовностью помогаю товарищам по команде, когда они застревают.',
                'text_uz': "Jamoadoshlarim qiynalganda ularga yordam berishga tayyorman.",
            },
            {
                'key': 'teamwork_negative_2', 'reverse_scored': True,
                'text_ru': 'Мне сложно доверить часть задачи другому человеку в команде.',
                'text_uz': "Jamoada vazifaning bir qismini boshqa odamga ishonib topshirish men uchun qiyin.",
            },
        ],
    },
    'patience': {
        'label_ru': "ТЕРПЕНИЕ И НАСТОЙЧИВОСТЬ", 'label_uz': "SABR-TOQAT VA QAT'IYATLILIK",
        'items': [
            {
                'key': 'patience_positive_1', 'reverse_scored': False,
                'text_ru': 'Я продолжаю работать над задачей даже после нескольких неудачных попыток.',
                'text_uz': 'Bir necha muvaffaqiyatsiz urinishdan keyin ham masala ustida ishlashda davom etaman.',
            },
            {
                'key': 'patience_negative_1', 'reverse_scored': True,
                'text_ru': 'Я расстраиваюсь и хочу всё бросить, когда что-то не работает с первого раза.',
                'text_uz': "Biror narsa birinchi urinishda ishlamasa, tushkunlikka tushib, to'xtatib qo'yishni xohlayman.",
            },
            {
                'key': 'patience_positive_2', 'reverse_scored': False,
                'text_ru': 'Я сохраняю спокойствие, когда решение задачи занимает намного больше времени, чем ожидалось.',
                'text_uz': "Masalani yechish kutilganidan ancha ko'p vaqt olganda ham xotirjamligimni saqlayman.",
            },
            {
                'key': 'patience_negative_2', 'reverse_scored': True,
                'text_ru': 'Я склонен переключаться на другую задачу, если эта кажется слишком долгой.',
                'text_uz': "Agar masala juda uzoq davom etayotgandek tuyulsa, boshqa vazifaga o'tishga moyilman.",
            },
        ],
    },
    'learning_speed': {
        'label_ru': 'СКОРОСТЬ ОБУЧЕНИЯ', 'label_uz': "O'RGANISH TEZLIGI",
        'items': [
            {
                'key': 'learning_speed_positive_1', 'reverse_scored': False,
                'text_ru': 'Я быстро схватываю новые понятия после одного объяснения.',
                'text_uz': "Yangi tushunchalarni bir marta tushuntirilgandan keyin tez o'zlashtiraman.",
            },
            {
                'key': 'learning_speed_negative_1', 'reverse_scored': True,
                'text_ru': 'Мне нужно несколько повторений, чтобы разобраться в новой теме.',
                'text_uz': "Yangi mavzuni tushunish uchun menga bir necha marta takrorlash kerak bo'ladi.",
            },
            {
                'key': 'learning_speed_positive_2', 'reverse_scored': False,
                'text_ru': 'Я легко переношу то, что выучил, на новые и незнакомые задачи.',
                'text_uz': "O'rgangan narsalarimni yangi va notanish masalalarga oson qo'llay olaman.",
            },
            {
                'key': 'learning_speed_negative_2', 'reverse_scored': True,
                'text_ru': 'Я часто отстаю от группы, когда мы переходим к новой теме.',
                'text_uz': "Yangi mavzuga o'tganimizda ko'pincha guruhdan orqada qolib ketaman.",
            },
        ],
    },
}
