"""Standalone bilingual curriculum authoring. Does not import application code."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMAT = 'mindmetric-cluster3-draft-v1'


def b(value):
    parts = value.split(' || ')
    if len(parts) != 2 or not all(part.strip() for part in parts):
        raise ValueError(f'Expected UZ/RU text: {value!r}')
    return dict(zip(('uz', 'ru'), parts))


def choice(text, feedback):
    return {'text': b(text), 'feedback': b(feedback)}


def q(prompt, options, steps, error, hint=None):
    """First authored option is correct; compiler rotates it in published copies."""
    return {'prompt': b(prompt), 'options': options, 'steps': b(steps),
            'error': b(error), 'hint': b(hint) if hint else None}


def numeric(prompt, answer, steps, error, hint=None):
    return dict(q(prompt, [], steps, error, hint), answer=str(answer))


def lesson(key, title, outcome, theory, example, steps, answer, questions):
    assert len(questions) == 4
    assert all(row['hint'] is not None for row in questions[:2])
    assert all(row['hint'] is None for row in questions[2:])
    return {'key': key, 'title': b(title), 'outcome': b(outcome),
            'theory': [b(p) for p in theory], 'example': b(example),
            'steps': b(steps), 'answer': b(answer), 'questions': questions}


def module(key, number, title, lessons):
    assert len(lessons) == 5
    return {'key': key, 'number': number, 'title': b(title), 'lessons': lessons}


def digest(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def compile_module(authored, sources):
    m = authored
    data = {'resource_format': FORMAT, 'integration_status': 'not_importable',
            'sources': sources, 'module': {'key': m['key'], 'version': 1, 'cluster': 3,
            'order': m['number'], 'topic_number': f"3.{m['number']}",
            'title_uz': m['title']['uz'], 'title_ru': m['title']['ru'], 'status': 'draft',
            'content_language': 'uz', 'review_status': 'internally_checked'},
            'skills': [], 'lessons': [], 'exercises': [], 'diagnostic_links': [],
            'blueprint': {'practice_order': [], 'precheck_order': [], 'postcheck_order': [],
                          'matched_pairs': [], 'unseen_postcheck_sets': 1}}
    ru = {'module_key': m['key'], 'version': 1, 'language': 'ru', 'title': m['title']['ru'],
          'skills': {}, 'lessons': {}, 'exercises': {}}
    previous = []
    for index, row in enumerate(m['lessons']):
        key = row['key']
        data['skills'].append({'key': key, 'title_uz': row['title']['uz'], 'prerequisite_keys': previous[-1:]})
        ru['skills'][key] = row['title']['ru']
        previous.append(key)
        lk = key + '-lesson'
        data['lessons'].append({'key': lk, 'skill_key': key, 'title_uz': row['title']['uz'],
            'outcome_uz': row['outcome']['uz'], 'theory_uz': [p['uz'] for p in row['theory']],
            'worked_example': {'prompt_uz': row['example']['uz'],
                              'solution_steps_uz': row['steps']['uz'].split('|'), 'answer_uz': row['answer']['uz']}})
        ru['lessons'][lk] = {'title': row['title']['ru'], 'outcome': row['outcome']['ru'],
            'theory': [p['ru'] for p in row['theory']], 'worked_example': {'prompt': row['example']['ru'],
            'solution_steps': row['steps']['ru'].split('|'), 'answer': row['answer']['ru']}}
        pairs = {}
        for j, item in enumerate(row['questions']):
            purpose = ('practice', 'practice', 'precheck', 'postcheck')[j]
            qk = f'{key}-{purpose}' + (f'-{j + 1}' if j < 2 else '')
            pairs[purpose] = qk
            options, roptions = [], {}
            if item['options']:
                choices = list(enumerate(item['options']))
                offset = (index + j + m['number']) % len(choices)
                choices = choices[offset:] + choices[:offset]
                for k, (original, option) in enumerate(choices):
                    oid = chr(97 + k)
                    options.append({'id': oid, 'text_uz': option['text']['uz'], 'feedback_uz': option['feedback']['uz']})
                    roptions[oid] = {'text': option['text']['ru'], 'feedback': option['feedback']['ru']}
                    if original == 0:
                        answer = {'option_id': oid}
            else:
                answer = {'value': item['answer']}
            data['exercises'].append({'key': qk, 'skill_key': key, 'purpose': purpose,
                'format': 'single' if options else 'numeric', 'prompt_uz': item['prompt']['uz'],
                'options': options, 'answer_key': answer, 'solution_steps_uz': item['steps']['uz'].split('|'),
                'common_error_uz': item['error']['uz'], 'hint_uz': item['hint']['uz'] if item['hint'] else None,
                'source': {'id': 'authored-cluster3', 'origin': 'authored', 'locator': f"3.{m['number']}/{qk}"}})
            ru['exercises'][qk] = {'prompt': item['prompt']['ru'], 'options': roptions,
                'solution_steps': item['steps']['ru'].split('|'), 'common_error': item['error']['ru'],
                'hint': item['hint']['ru'] if item['hint'] else None}
            data['blueprint'][purpose + '_order'].append(qk)
        data['blueprint']['matched_pairs'].append({'skill_key': key, 'precheck_key': pairs['precheck'], 'postcheck_key': pairs['postcheck']})
    data['blueprint']['practice_order'] = [f"{row['key']}-practice-{j}" for j in (1, 2) for row in m['lessons']]
    ru['source_hash'] = digest(data)
    return data, ru


def markdown(data, ru, language, audience):
    """Teacher includes all keys; student study and checks are separate files."""
    is_ru = language == 'ru'
    title = ru['title'] if is_ru else data['module']['title_uz']
    names = {'teacher': ('O‘qituvchi nusxasi — javoblar mavjud', 'Копия преподавателя — с ответами'),
             'student': ('O‘quvchi nusxasi — o‘qish va mashq', 'Копия учащегося — изучение и практика'),
             'checks': ('Tekshiruv varag‘i — javobsiz', 'Проверочный лист — без ответов')}
    lines = [f"# {data['module']['topic_number']} — {title}", '', names[audience][int(is_ru)], '',
             f'[README](README.md) · [Python / Git](bridge.{language}.md)', '']
    for row in data['lessons']:
        local = ru['lessons'][row['key']]
        lines += ['## ' + (local['title'] if is_ru else row['title_uz']), '']
        if audience != 'checks':
            lines += [('Результат: ' if is_ru else 'Natija: ') + (local['outcome'] if is_ru else row['outcome_uz']), '']
            for paragraph in local['theory'] if is_ru else row['theory_uz']:
                lines += [paragraph, '']
            example = local['worked_example'] if is_ru else {
                'prompt': row['worked_example']['prompt_uz'], 'solution_steps': row['worked_example']['solution_steps_uz'],
                'answer': row['worked_example']['answer_uz']}
            lines += ['### ' + ('Разобранный пример' if is_ru else 'Ishlangan misol'), '', example['prompt'], '']
            lines += [f'{i + 1}. {step}' for i, step in enumerate(example['solution_steps'])]
            lines += ['', ('Ответ: ' if is_ru else 'Javob: ') + example['answer'], '']
        for item in [q for q in data['exercises'] if q['skill_key'] == row['skill_key']]:
            if audience == 'student' and item['purpose'] != 'practice':
                continue
            if audience == 'checks' and item['purpose'] == 'practice':
                continue
            t = ru['exercises'][item['key']]
            name = {'practice': ('Mashq', 'Практика'), 'precheck': ('Boshlang‘ich', 'Входная'),
                    'postcheck': ('Yakuniy', 'Итоговая')}[item['purpose']][int(is_ru)]
            lines += [f"### {name} — `{item['key']}`", '', t['prompt'] if is_ru else item['prompt_uz'], '']
            for o in item['options']:
                lines += [f"- {o['id']}) " + (t['options'][o['id']]['text'] if is_ru else o['text_uz'])]
            lines += ['']
            hint = t['hint'] if is_ru else item['hint_uz']
            if hint and audience != 'checks':
                lines += [('Подсказка: ' if is_ru else 'Ishora: ') + hint, '']
            if audience == 'teacher':
                lines += [('Ключ: ' if is_ru else 'Kalit: ') + next(iter(item['answer_key'].values())), '']
                lines += [f'{i + 1}. {s}' for i, s in enumerate(t['solution_steps'] if is_ru else item['solution_steps_uz'])]
                lines += ['', ('Типичная ошибка: ' if is_ru else 'Keng tarqalgan xato: ') + (t['common_error'] if is_ru else item['common_error_uz']), '']
                for o in item['options']:
                    lines += [f"- {o['id']}: " + (t['options'][o['id']]['feedback'] if is_ru else o['feedback_uz'])]
                lines += ['']
            else:
                lines += [('Ваш ответ и обоснование: __________' if is_ru else 'Javobingiz va asosingiz: __________'), '']
    return '\n'.join(lines).rstrip() + '\n'
