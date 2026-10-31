"""Bilingual authoring helpers. Outputs are draft resources, never a DB import."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def b(value):
    if isinstance(value, dict):
        return value
    parts = value.split(' || ')
    if len(parts) != 2 or not all(p.strip() for p in parts):
        raise ValueError(f'Bilingual pair required: {value!r}')
    return dict(zip(('uz', 'ru'), parts))


def n(prompt, answer, steps, error, hint=None):
    return {'prompt': b(prompt), 'answer': str(answer), 'steps': b(steps),
            'error': b(error), 'hint': b(hint) if hint else None, 'options': []}


def s(prompt, options, steps, error, hint=None):
    """First authored option is correct; output rotates its position by question index."""
    return {'prompt': b(prompt), 'options': [(b(t), b(f)) for t, f in options],
            'steps': b(steps), 'error': b(error), 'hint': b(hint) if hint else None}


def lesson(key, title, theory, example, steps, answer, questions, prerequisites=()):
    assert len(questions) == 4
    assert all(q['hint'] for q in questions[:2]), key
    return {'key': key, 'title': b(title), 'theory': [b(p) for p in theory],
            'example': b(example), 'steps': b(steps), 'answer': b(answer),
            'questions': questions, 'prerequisites': list(prerequisites)}


def module(key, number, title, indicators, lessons):
    assert len(lessons) == 5
    return {'key': key, 'number': number, 'title': b(title),
            'indicators': indicators, 'lessons': lessons}


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def compile_module(authored, sources):
    m = authored
    data = {'schema_version': 2, 'sources': sources,
            'module': {'key': m['key'], 'version': 1, 'order': m['number'],
                       'cluster': 2, 'topic_number': f"2.{m['number']}",
                       'title_uz': m['title']['uz'], 'title_ru': m['title']['ru'],
                       'content_language': 'uz', 'indicator_keys': m['indicators'],
                       'status': 'draft', 'review_status': 'internally_checked',
                       'diagnostic_coverage_note_uz': 'Aniq diagnostika savollari bilan xarita hali tasdiqlanmagan. Boshlang‘ich tekshiruv mavzu bo‘yicha dastlabki dalil beradi.'},
            'skills': [], 'lessons': [], 'exercises': [], 'diagnostic_links': [],
            'blueprint': {'precheck_order': [], 'practice_order': [], 'postcheck_order': [],
                          'matched_pairs': [], 'unseen_postcheck_sets': 1,
                          'comparison_note_uz': 'Ko‘nikma va tahririy qiyinlik bo‘yicha juftlangan; statistik tenglashtirish va umumiy qobiliyat o‘sishi da’vosi yo‘q.',
                          'exhaustion_note_uz': 'Bitta mustaqil yakuniy tekshiruv to‘plami bor. Yangi bank bo‘lmasa qayta o‘sish o‘lchovi olinmaydi.'}}
    ru = {'module_key': m['key'], 'version': 1, 'language': 'ru',
          'title': m['title']['ru'], 'skills': {}, 'lessons': {}, 'exercises': {}}
    for index, l in enumerate(m['lessons']):
        key = l['key']
        data['skills'].append({'key': key, 'title_uz': l['title']['uz'],
                               'indicator_keys': m['indicators'], 'prerequisite_keys': l['prerequisites']})
        ru['skills'][key] = l['title']['ru']
        lk = f'{key}-lesson'
        data['lessons'].append({'key': lk, 'skill_key': key, 'title_uz': l['title']['uz'],
                                'theory_uz': [t['uz'] for t in l['theory']],
                                'worked_example': {'prompt_uz': l['example']['uz'],
                                                   'solution_steps_uz': l['steps']['uz'].split('|'),
                                                   'answer_uz': l['answer']['uz']}})
        ru['lessons'][lk] = {'title': l['title']['ru'], 'theory': [t['ru'] for t in l['theory']],
                             'worked_example': {'prompt': l['example']['ru'],
                                                'solution_steps': l['steps']['ru'].split('|'),
                                                'answer': l['answer']['ru']}}
        qkeys = {}
        for j, q in enumerate(l['questions']):
            purpose = ['practice', 'practice', 'precheck', 'postcheck'][j]
            qk = f'{key}-{purpose}' + (f'-{j + 1}' if j < 2 else '')
            qkeys[purpose] = qk
            options, roptions = [], {}
            if q['options']:
                choices = list(enumerate(q['options']))
                offset = (index + j) % len(choices)
                choices = choices[offset:] + choices[:offset]
                for k, (original, (label, feedback)) in enumerate(choices):
                    oid = chr(97 + k)
                    options.append({'id': oid, 'text_uz': label['uz'], 'feedback_uz': feedback['uz']})
                    roptions[oid] = {'text': label['ru'], 'feedback': feedback['ru']}
                    if original == 0:
                        answer = {'option_id': oid}
            else:
                answer = {'value': q['answer']}
            data['exercises'].append({'key': qk, 'skill_key': key, 'purpose': purpose,
                                      'format': 'single' if options else 'numeric', 'difficulty': 'medium',
                                      'prompt_uz': q['prompt']['uz'], 'options': options, 'answer_key': answer,
                                      'solution_steps_uz': q['steps']['uz'].split('|'),
                                      'common_error_uz': q['error']['uz'],
                                      'hint_uz': q['hint']['uz'] if purpose == 'practice' else None,
                                      'source': {'id': 'authored-cluster2', 'origin': 'authored',
                                                 'locator': f"{m['number']}/{key}/{purpose}/{j + 1}"}})
            ru['exercises'][qk] = {'prompt': q['prompt']['ru'], 'options': roptions,
                                   'solution_steps': q['steps']['ru'].split('|'),
                                   'common_error': q['error']['ru'],
                                   'hint': q['hint']['ru'] if purpose == 'practice' else None}
            data['blueprint'][purpose + '_order'].append(qk)
        data['blueprint']['matched_pairs'].append({'skill_key': key, 'difficulty': 'medium',
                                                  'precheck_key': qkeys['precheck'], 'postcheck_key': qkeys['postcheck']})
    # Practice has two passes so that the readiness window covers every skill.
    data['blueprint']['practice_order'] = [f"{l['key']}-practice-{j}" for j in (1, 2) for l in m['lessons']]
    ru['source_hash'] = digest(data)
    return data, ru


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def markdown(data, ru, language):
    is_ru = language == 'ru'
    title = ru['title'] if is_ru else data['module']['title_uz']
    lines = [f"# {data['module']['topic_number']} — {title}", '',
             'Учебный материал · черновик · версия 1' if is_ru else 'O‘quv resursi · draft · versiya 1', '',
             '[Правила псевдокода](pseudocode.ru.md) · [Все темы](README.md)' if is_ru else
             '[Psevdokod qoidalari](pseudocode.uz.md) · [Barcha mavzular](README.md)', '',
             'Авторские задания. Ключи и разборы включены в эту преподавательскую копию; файл не публикуется целиком студенту во время проверок.' if is_ru else
             'Mualliflik topshiriqlari. Ushbu o‘qituvchi nusxasida javoblar va yechimlar bor; tekshiruv paytida fayl talabaga to‘liq berilmaydi.', '']
    for lesson_row in data['lessons']:
        local = ru['lessons'][lesson_row['key']]
        example = local['worked_example'] if is_ru else {
            'prompt': lesson_row['worked_example']['prompt_uz'],
            'solution_steps': lesson_row['worked_example']['solution_steps_uz'],
            'answer': lesson_row['worked_example']['answer_uz']}
        lines += ['## ' + (local['title'] if is_ru else lesson_row['title_uz']), '']
        for paragraph in local['theory'] if is_ru else lesson_row['theory_uz']:
            lines += [paragraph, '']
        lines += ['### ' + ('Разобранный пример' if is_ru else 'Ishlangan misol'), '', example['prompt'], '']
        lines += [f'{i + 1}. {step}' for i, step in enumerate(example['solution_steps'])]
        lines += ['', ('Ответ: ' if is_ru else 'Javob: ') + example['answer'], '']
        for q in (q for q in data['exercises'] if q['skill_key'] == lesson_row['skill_key']):
            t = ru['exercises'][q['key']]
            names = {'practice': ('Mashq', 'Практика'), 'precheck': ('Boshlang‘ich tekshiruv', 'Входная проверка'),
                     'postcheck': ('Yakuniy tekshiruv', 'Итоговая проверка')}
            lines += [f"### {names[q['purpose']][int(is_ru)]} — `{q['key']}`", '', t['prompt'] if is_ru else q['prompt_uz'], '']
            for o in q['options']:
                lines += [f"- {o['id']}) " + (t['options'][o['id']]['text'] if is_ru else o['text_uz'])]
            lines += ['', ('Ключ: ' if is_ru else 'Kalit: ') + next(iter(q['answer_key'].values())), '']
            lines += [f'{i + 1}. {step}' for i, step in enumerate(t['solution_steps'] if is_ru else q['solution_steps_uz'])]
            lines += ['', ('Типичная ошибка: ' if is_ru else 'Keng tarqalgan xato: ') + (t['common_error'] if is_ru else q['common_error_uz']), '']
            if q['purpose'] == 'practice':
                lines += [('Подсказка: ' if is_ru else 'Ishora: ') + (t['hint'] if is_ru else q['hint_uz']), '']
            for o in q['options']:
                lines += [f"- {o['id']}: " + (t['options'][o['id']]['feedback'] if is_ru else o['feedback_uz'])]
            lines += ['']
    return '\n'.join(lines) + '\n'
