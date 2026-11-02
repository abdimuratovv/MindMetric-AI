"""Read-only curricular priorities, separate from skill-level evidence and IRT."""
import math

from apps.assessments.models import AssessmentAttempt
from apps.scoring.constants import INDICATOR_LABELS
from apps.scoring.models import IndicatorScore
from .curriculum import CLUSTERS

# Oqitish moduli.docx: each of the ten indicators belongs to one cluster.
CLUSTER_INDICATORS = {
    1: ('math', 'logic', 'iq'),
    2: ('algorithmic', 'creative', 'problem_solving'),
    3: ('teamwork', 'patience', 'learning_speed', 'attention'),
}


def cluster_guidance(scores, completed, language='uz'):
    language = language if language in ('uz', 'ru') else 'uz'
    keys = {key for group in CLUSTER_INDICATORS.values() for key in group}
    valid = {key for key in keys if key in completed and isinstance(scores.get(key), (int, float))
             and not isinstance(scores[key], bool) and math.isfinite(scores[key]) and 0 <= scores[key] <= 100}
    result = {'available': valid == keys, 'completed_count': len(valid), 'required_count': len(keys),
              'policy_version': 1, 'clusters': []}
    if valid != keys:
        return result
    rows = []
    for number, group in CLUSTER_INDICATORS.items():
        indicators = [{'key': key, 'label': INDICATOR_LABELS[language][key], 'score': scores[key]} for key in group]
        rows.append({'id': number, 'title': CLUSTERS[number][language][0],
                     'score': round(sum(scores[key] for key in group) / len(group), 2),
                     'indicators': indicators})
    minimum = min(row['score'] for row in rows)
    maintenance = min(scores[key] for key in keys) >= 80
    for row in rows:
        row['recommended'] = row['score'] == minimum
        roman = {1: 'I', 2: 'II', 3: 'III'}[row['id']]
        if language == 'uz':
            row['headline'] = f"Sizga {roman} klasterni rivojlantirish tavsiya etiladi"
            row['reason'] = (f"Chunki ushbu klasterga tegishli indikatorlarning o‘rtacha bali {row['score']:g}/100 "
                             "bo‘lib, uch klaster orasida eng past natijadir. Teng balli klasterlar birgalikda tavsiya qilinadi.")
        else:
            row['headline'] = f'Вам рекомендуется развивать кластер {roman}'
            row['reason'] = (f"Средний балл связанных показателей — {row['score']:g}/100: это наименьший результат "
                             'среди трёх кластеров. Кластеры с равным баллом рекомендуются вместе.')
    result.update(clusters=rows, mode='maintenance' if maintenance else 'development',
                  note=(('Barcha indikatorlaringiz yuqori darajada. Bu tavsiya ko‘nikmalarni mustahkamlash uchun. '
                         if maintenance else '') +
                        'Bu o‘quv ustuvorligi; aniq mavzuni boshlang‘ich tekshiruv belgilaydi. Modul tavsiyalari alohida ko‘nikma dalillariga asoslanadi.')
                  if language == 'uz' else
                  (('Все показатели на высоком уровне. Рекомендация поможет закрепить навыки. ' if maintenance else '') +
                   'Это учебный приоритет; конкретную тему уточняет входная проверка. Рекомендации модулей основаны на данных по отдельным навыкам.'))
    return result


def student_cluster_guidance(student, language='uz'):
    scores = dict(IndicatorScore.objects.filter(student=student).values_list('indicator_key', 'score'))
    completed = set(AssessmentAttempt.objects.filter(student=student, status='completed').values_list('assessment_type', flat=True))
    return cluster_guidance(scores, completed, language)
