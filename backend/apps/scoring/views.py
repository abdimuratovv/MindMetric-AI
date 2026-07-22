from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsStudent
from apps.assessments.models import AssessmentAttempt, CognitiveResponse
from apps.i18n import get_language

from .constants import FIELD_CHOICES, FIELD_LABELS, INDICATOR_CHOICES, INDICATOR_LABELS
from .models import Achievement, FieldRecommendation, IndicatorScore, OverallScore
from . import achievements, calculators

# {{ ind.tier }} / {{ ind.color }} for the 10 - len(indicator_scores) indicators a student
# hasn't attempted yet — results/analytics screens show every indicator, not just completed
# ones, so "no score yet" needs its own tier text distinct from a genuine low score.
NOT_COMPLETED_LABEL = {'ru': 'Не пройдено', 'uz': 'Hali topshirilmagan'}
NOT_COMPLETED_COLOR = '#93A39A'
NOT_COMPLETED_BG = '#EDF1EE'

# One sentence per indicator — what it measures / what a high score shows.
INDICATOR_EXPLANATIONS = {
    'ru': {
        'math': 'Проверяет владение базовыми математическими понятиями — арифметикой, процентами и алгебраическими рассуждениями.',
        'logic': 'Следует структурированным, основанным на правилах цепочкам рассуждений и делает верные выводы из посылок.',
        'algorithmic': 'Переводит логику в рабочий, идиоматичный код без лишних итераций.',
        'creative': 'Предлагает нестандартные, оригинальные решения там, где очевидный подход — не единственный.',
        'teamwork': 'Комфортно сотрудничает, делится рассуждениями и учитывает точку зрения товарищей по команде.',
        'patience': 'Продолжает совершенствовать подход после повторных неудачных попыток.',
        'problem_solving': 'Разбивает большую задачу на более мелкие, независимо решаемые шаги и доводит решение до конца.',
        'learning_speed': 'Быстро усваивает новые понятия и переносит их на незнакомые задачи с минимальным числом повторений.',
        'attention': 'Замечает граничные случаи и мелкие ошибки перед отправкой решения.',
        'iq': 'Показывает общий уровень абстрактного мышления на числовых, вербальных и пространственных задачах.',
    },
    'uz': {
        'math': "Arifmetika, foizlar va algebraik mulohaza kabi asosiy matematik tushunchalarni bilish darajasini tekshiradi.",
        'logic': "Tuzilgan, qoidalarga asoslangan mulohaza zanjirlariga amal qiladi va asoslardan to'g'ri xulosalar chiqaradi.",
        'algorithmic': "Mantiqni ortiqcha takrorlarsiz ishlaydigan, idiomatik kodga aylantiradi.",
        'creative': "Aniq yechim yagona yo'l bo'lmagan holatlarda original va nostandart yechimlarni taklif qiladi.",
        'teamwork': "Jamoadoshlar bilan qulay hamkorlik qiladi, fikrlash yo'lini ulashadi va ularning nuqtai nazarini hisobga oladi.",
        'patience': "Bir necha muvaffaqiyatsiz urinishdan so'ng ham yondashuvni takomillashtirishda davom etadi.",
        'problem_solving': "Katta masalani mustaqil yechiladigan kichikroq bosqichlarga ajratadi va yechimni oxirigacha yetkazadi.",
        'learning_speed': "Yangi tushunchalarni tez o'zlashtiradi va ularni kam takrorlash bilan notanish masalalarga qo'llaydi.",
        'attention': "Yechimni yuborishdan oldin chekka holatlar va mayda xatolarni payqaydi.",
        'iq': "Sonli, og'zaki va fazoviy masalalar bo'yicha abstrakt fikrlashning umumiy darajasini ko'rsatadi.",
    },
}

# {{ bandExplanation }} — one sentence per band key (see calculators._BANDS), not a
# template substituted with the band headline: Russian/Uzbek grammar doesn't inflect
# cleanly by word-splicing a translated noun phrase into a fixed sentence frame.
BAND_EXPLANATIONS = {
    'ru': {
        'exceptional': 'Входит в топ трети этого курса по всем десяти показателям способностей.',
        'high': 'Стабильно входит в верхнюю половину курса по большинству из десяти показателей способностей.',
        'developing': 'Показывает результаты около среднего уровня курса, с явными точками роста по отдельным показателям.',
        'foundational': 'Находится на начальном уровне по большинству из десяти показателей — есть значительный потенциал для роста при целевой практике.',
    },
    'uz': {
        'exceptional': "O'nta qobiliyat ko'rsatkichi bo'yicha ushbu oqimning eng yuqori uchdan bir qismiga kiradi.",
        'high': "O'nta ko'rsatkichning aksariyati bo'yicha barqaror tarzda oqimning yuqori yarmida turadi.",
        'developing': "Oqimning o'rtacha darajasiga yaqin natija ko'rsatmoqda, alohida ko'rsatkichlarda aniq o'sish nuqtalari bor.",
        'foundational': "O'nta ko'rsatkichning aksariyati bo'yicha boshlang'ich darajada — maqsadli mashq bilan sezilarli o'sish salohiyati mavjud.",
    },
}

OVERALL_EXPLANATIONS = {
    'ru': {
        'exceptional': (
            'Исключительный результат по всем десяти показателям способностей. Наиболее сильные стороны видны у '
            'показателей с самым высоким баллом на диаграмме ниже — им стоит уделить внимание в первую очередь '
            'при планировании развития. Эта оценка отражает только автоматизированное тестирование — '
            'педагогический контекст см. в отзыве преподавателя.'
        ),
        'high': (
            'Высокий результат по большинству из десяти показателей способностей. Показатели с наименьшим '
            'баллом на диаграмме ниже — область, которая больше всего выиграет от целевой практики. Эта оценка '
            'отражает только автоматизированное тестирование — педагогический контекст см. в отзыве преподавателя.'
        ),
        'developing': (
            'Развивающийся результат: некоторые показатели уже являются сильными сторонами, другие только '
            'формируются. Показатели с наименьшим баллом на диаграмме ниже — область, которая больше всего '
            'выиграет от целевой практики. Эта оценка отражает только автоматизированное тестирование — '
            'педагогический контекст см. в отзыве преподавателя.'
        ),
        'foundational': (
            'Начальный результат с пространством для роста по большинству из десяти показателей. Показатели с '
            'наименьшим баллом на диаграмме ниже — хорошая отправная точка для целевой практики. Эта оценка '
            'отражает только автоматизированное тестирование — педагогический контекст см. в отзыве преподавателя.'
        ),
    },
    'uz': {
        'exceptional': (
            "O'nta qobiliyat ko'rsatkichi bo'yicha ajoyib natija. Eng kuchli tomonlar quyidagi diagrammada eng "
            "yuqori ballga ega ko'rsatkichlarda ko'rinadi — rivojlanishni rejalashtirishda ularga birinchi "
            "navbatda e'tibor bering. Ushbu ball faqat avtomatlashtirilgan testlashni aks ettiradi — pedagogik "
            "kontekst uchun o'qituvchi tavsiyanomasiga qarang."
        ),
        'high': (
            "O'nta ko'rsatkichning aksariyati bo'yicha yuqori natija. Quyidagi diagrammada eng past ballga ega "
            "ko'rsatkichlar — maqsadli mashqdan eng ko'p foyda ko'radigan soha. Ushbu ball faqat "
            "avtomatlashtirilgan testlashni aks ettiradi — pedagogik kontekst uchun o'qituvchi tavsiyanomasiga "
            "qarang."
        ),
        'developing': (
            "Rivojlanayotgan natija: ba'zi ko'rsatkichlar allaqachon kuchli tomon, boshqalari hali "
            "shakllanmoqda. Quyidagi diagrammada eng past ballga ega ko'rsatkichlar — maqsadli mashqdan eng ko'p "
            "foyda ko'radigan soha. Ushbu ball faqat avtomatlashtirilgan testlashni aks ettiradi — pedagogik "
            "kontekst uchun o'qituvchi tavsiyanomasiga qarang."
        ),
        'foundational': (
            "O'nta ko'rsatkichning aksariyati bo'yicha o'sish salohiyati katta bo'lgan boshlang'ich natija. "
            "Quyidagi diagrammada eng past ballga ega ko'rsatkichlar — maqsadli mashq uchun yaxshi boshlang'ich "
            "nuqta. Ushbu ball faqat avtomatlashtirilgan testlashni aks ettiradi — pedagogik kontekst uchun "
            "o'qituvchi tavsiyanomasiga qarang."
        ),
    },
}


# One sentence per field — why a student who scores well on its weighted indicators
# (see constants.FIELD_WEIGHTS) fits that specialization. Shown next to each ranked
# entry in {{ fieldRecommendations }}.
FIELD_EXPLANATIONS = {
    'ru': {
        'backend': 'Сильное сочетание алгоритмического и логического мышления — хорошая основа для серверной разработки и сложных программных систем.',
        'frontend': 'Высокая креативность и внимательность к деталям — хорошая основа для разработки пользовательских интерфейсов.',
        'data_ai': 'Сильные математические и аналитические способности — потенциал в data science и машинном обучении.',
        'qa': 'Высокая внимательность и терпение — качества, необходимые для тестирования и контроля качества ПО.',
        'team_lead': 'Развитые навыки командной работы и решения проблем — предпосылки для роли тимлида или руководителя проекта.',
        'devops': 'Терпение и внимательность в сочетании с решением проблем — хорошая основа для DevOps и системного администрирования.',
    },
    'uz': {
        'backend': "Algoritmik va mantiqiy fikrlashning kuchli uyg'unligi — server tomoni dasturlash va murakkab dasturiy tizimlar uchun yaxshi asos.",
        'frontend': "Yuqori kreativlik va detallarga e'tibor — foydalanuvchi interfeyslarini ishlab chiqish uchun yaxshi asos.",
        'data_ai': "Kuchli matematik va tahliliy qobiliyatlar — data science va mashinaviy o'rganish sohasidagi salohiyat.",
        'qa': "Yuqori diqqat va sabr-toqat — dasturiy ta'minot sifatini nazorat qilish va testlashda zarur fazilatlar.",
        'team_lead': "Rivojlangan jamoaviy ish va muammo yechish ko'nikmalari — jamoa boshqaruvchisi yoki loyiha menejeri roli uchun zamin.",
        'devops': "Sabr-toqat va diqqatning muammo yechish bilan uyg'unligi — DevOps va tizim ma'muriyati uchun yaxshi asos.",
    },
}


def serialize_field_recommendation(recommendation: FieldRecommendation | None, lang: str) -> dict:
    """Shared shape for ResultsSummaryView and reviews.TeacherStudentDetailView —
    both show the same ranked-fields block, just to different audiences."""
    if recommendation is None or not recommendation.is_confident:
        return {'available': False, 'fields': []}
    # fit_scores was written by calculators.compute_field_fit already sorted best-first
    # (state_tracker.py); iterate it directly rather than FIELD_CHOICES order so that
    # ordering survives the JSONField round-trip instead of reverting to declaration order.
    return {
        'available': True,
        'fields': [
            {
                'key': key,
                'label': FIELD_LABELS[lang][key],
                'score': score,
                'explanation': FIELD_EXPLANATIONS[lang][key],
            }
            for key, score in recommendation.fit_scores.items()
        ],
    }


class ResultsSummaryView(APIView):
    """
    GET /api/results/summary/

    Feeds the results screen: {{ overallScore }}, {{ band }}, {{ bandExplanation }},
    {{ indicators }}. The radar chart's points/axes/rings/dots stay a pure
    frontend computation (same `polar()` helper, ported unchanged) over
    `indicators`, so they aren't computed here.

    Always returns all 10 indicators (not just the ones the student has scored so far) —
    "View results" unlocks after completing just one assessment (see
    apps.scoring.state_tracker.StudentStateTracker.get_resume_state's `any_completed`), so
    most students will have several indicators still unattempted. Each entry carries
    `completed` so the frontend can render those distinctly instead of silently omitting
    them, which previously made a 4-of-10 radar look like the product only measures 4 things.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        lang = get_language(request)
        overall = OverallScore.objects.filter(student=request.user).first()
        scores_by_key = {
            row.indicator_key: row.score
            for row in IndicatorScore.objects.filter(student=request.user)
        }

        indicators = []
        for key, _ in INDICATOR_CHOICES:
            score = scores_by_key.get(key)
            if score is None:
                indicators.append({
                    'key': key,
                    'label': INDICATOR_LABELS[lang][key],
                    'score': None,
                    'tier': NOT_COMPLETED_LABEL[lang],
                    'color': NOT_COMPLETED_COLOR,
                    'pct': '0%',
                    'completed': False,
                })
                continue
            tier = calculators.tier_for(score, lang)
            indicators.append({
                'key': key,
                'label': INDICATOR_LABELS[lang][key],
                'score': score,
                'tier': tier['tier'],
                'color': tier['color'],
                'pct': f'{score}%',
                'completed': True,
            })

        overall_score = overall.score if overall else 0
        band_info = calculators.band_for(overall_score, lang)
        field_recommendation = FieldRecommendation.objects.filter(student=request.user).first()

        return Response({
            'overallScore': overall_score,
            'band': band_info['band'],
            'bandBg': band_info['bg'],
            'bandColor': band_info['color'],
            'bandExplanation': BAND_EXPLANATIONS[lang][band_info['key']],
            'indicators': indicators,
            'overallExplanation': OVERALL_EXPLANATIONS[lang][band_info['key']],
            'programmingAptitudeScore': overall.programming_aptitude_score if overall else None,
            'fieldRecommendations': serialize_field_recommendation(field_recommendation, lang),
        })


class AnalyticsDetailView(APIView):
    """
    GET /api/results/analytics/

    Feeds {{ indicatorsDetail }} — same rows as the summary, plus cohort
    average/percentile (computed here, was a fabricated offset in the mockup:
    `Math.max(40, i.score - 8 - (idx % 3) * 3)`).

    Like ResultsSummaryView, always returns all 10 indicators — see that view's
    docstring. cohortAvg/percentile are meaningless for a test the student hasn't
    taken, so unattempted rows carry `cohortAvg`/`percentile: None` instead of a
    fabricated comparison; the explanation still shows so the student knows what
    the test measures.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        lang = get_language(request)
        scores_by_key = {
            row.indicator_key: row.score
            for row in IndicatorScore.objects.filter(student=request.user)
        }

        detail = []
        for key, _ in INDICATOR_CHOICES:
            score = scores_by_key.get(key)
            if score is None:
                detail.append({
                    'key': key,
                    'label': INDICATOR_LABELS[lang][key],
                    'score': None,
                    'tier': NOT_COMPLETED_LABEL[lang],
                    'tierColor': NOT_COMPLETED_COLOR,
                    'tierBg': NOT_COMPLETED_BG,
                    'color': NOT_COMPLETED_COLOR,
                    'pct': '0%',
                    'cohortAvg': None,
                    'percentile': None,
                    'explanation': INDICATOR_EXPLANATIONS[lang][key],
                    'completed': False,
                })
                continue

            tier = calculators.tier_for(score, lang)
            cohort_avg = IndicatorScore.objects.filter(
                indicator_key=key,
            ).exclude(student=request.user).aggregate(avg=Avg('score'))['avg'] or score
            cohort_avg = round(cohort_avg)
            percentile = min(99, 50 + round((score - cohort_avg) * 1.4))

            detail.append({
                'key': key,
                'label': INDICATOR_LABELS[lang][key],
                'score': score,
                'tier': tier['tier'],
                'tierColor': tier['color'],
                'tierBg': tier['bg'],
                'color': tier['color'],
                'pct': f'{score}%',
                'cohortAvg': cohort_avg,
                'percentile': percentile,
                'explanation': INDICATOR_EXPLANATIONS[lang][key],
                'completed': True,
            })

        return Response(detail)


def serialize_achievement(achievement: Achievement, lang: str) -> dict:
    """Shared shape for both AchievementListView's rows and the {achievement} field
    Submit{Mcq,Coding,Likert}View echo back right after a badge is earned/upgraded."""
    return {
        'key': achievement.indicator_key,
        'label': INDICATOR_LABELS[lang][achievement.indicator_key],
        'name': achievements.badge_name(achievement.indicator_key, lang),
        'tier': achievement.tier,
        'tierLabel': achievements.tier_label(achievement.tier, lang),
        'score': achievement.score,
        'earnedAt': achievement.tier_earned_at,
        'locked': False,
    }


class ResultsMistakesView(APIView):
    """
    GET /api/results/mistakes/

    Feeds the results screen's "typical mistakes" section: one entry per
    completed-attempt question the student didn't answer fully correctly
    (correctness < 1.0), grouped by indicator, with the pedagogical advice
    authored on that question (CognitiveQuestion.feedback_ru/uz — see
    apps.assessments.feedback_content). Shown only here, never during the
    live test — surfacing it mid-attempt would leak which answer was wrong
    while the adaptive engine (apps.scoring.engine) is still picking
    difficulty-matched follow-up questions, undermining the test itself.

    Only questions with authored feedback are included — coverage is content,
    not code, so a not-yet-authored question is silently skipped rather than
    showing a blank tip.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        lang = get_language(request)
        responses = (
            CognitiveResponse.objects
            .filter(
                attempt__student=request.user,
                attempt__status=AssessmentAttempt.Status.COMPLETED,
                correctness__lt=1.0,
            )
            .exclude(**{f'question__feedback_{lang}': ''})
            .select_related('question')
            .order_by('question__indicator_key', '-responded_at')
        )

        grouped = {}
        for response in responses:
            question = response.question
            key = question.indicator_key
            entry = grouped.setdefault(key, {
                'indicatorKey': key,
                'indicatorLabel': INDICATOR_LABELS[lang][key],
                'items': [],
            })
            entry['items'].append({
                'prompt': getattr(question, f'prompt_{lang}'),
                'feedback': getattr(question, f'feedback_{lang}'),
            })

        mistakes = list(grouped.values())
        for entry in mistakes:
            entry['count'] = len(entry['items'])

        return Response({'mistakes': mistakes})


class AchievementListView(APIView):
    """
    GET /api/achievements/

    Feeds the student's achievement collection (the "Yutuqlarim"/"Достижения"
    profile screen) — always returns all 10 indicator slots, locked ones
    included with their badge name still shown (just dimmed client-side), so
    the collection reads as "10 to collect" rather than silently hiding
    unearned badges. Mirrors ResultsSummaryView's same choice for indicators.
    """

    permission_classes = [IsStudent]

    def get(self, request):
        lang = get_language(request)
        earned = {a.indicator_key: a for a in Achievement.objects.filter(student=request.user)}

        badges = []
        for key, _ in INDICATOR_CHOICES:
            achievement = earned.get(key)
            if achievement:
                badges.append(serialize_achievement(achievement, lang))
            else:
                badges.append({
                    'key': key,
                    'label': INDICATOR_LABELS[lang][key],
                    'name': achievements.badge_name(key, lang),
                    'tier': None,
                    'tierLabel': None,
                    'score': None,
                    'earnedAt': None,
                    'locked': True,
                })

        return Response({
            'badges': badges,
            'earnedCount': sum(1 for b in badges if not b['locked']),
            'totalCount': len(badges),
        })
