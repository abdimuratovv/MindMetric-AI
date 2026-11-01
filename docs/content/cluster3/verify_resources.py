"""Offline QA of draft resources; no Django imports and no production access."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from authoring import FORMAT, HERE, digest, markdown, write_json
from activities import build as build_activities, render
from build_resources import CURRICULUM_SHA
from module31 import build as module31
from module32 import build as module32
from module33 import build as module33
from module34 import build as module34
from lab_studytools import take, find, clip
from debugging_reference import add, discount, can_borrow
from library_reference import find_book, borrow, return_book


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def nonempty(text):
    return isinstance(text, str) and bool(text.strip())


def pair(uz, ru, label):
    require(nonempty(uz) and nonempty(ru), f'{label}: empty translation')
    require(not re.search('[А-Яа-яЁё]', uz), f'{label}: Cyrillic in Uzbek')
    if re.search('[А-Яа-яЁё]', ru) is None:
        # Pure code, identifiers and numeric answers legitimately need no Cyrillic.
        require(uz == ru, f'{label}: Russian prose missing')
    require(re.findall(r'-?\d+(?:\.\d+)?', uz) == re.findall(r'-?\d+(?:\.\d+)?', ru),
            f'{label}: numeric constants differ')
    require(re.findall(r'```[^\n]*\n(.*?)```', uz, re.S) ==
            re.findall(r'```[^\n]*\n(.*?)```', ru, re.S), f'{label}: code differs')


def validate(data, ru):
    meta = data['module']
    require(data['resource_format'] == FORMAT and data['integration_status'] == 'not_importable', 'Draft contract')
    require(meta['cluster'] == 3 and meta['status'] == 'draft', 'Cluster/status')
    require(meta['order'] in range(1, 5) and meta['topic_number'] == f"3.{meta['order']}", 'Topic metadata')
    require(ru['module_key'] == meta['key'] and ru['version'] == meta['version'] and ru['language'] == 'ru', 'Locale metadata')
    require(ru['source_hash'] == digest(data), 'Locale hash')
    require(data['diagnostic_links'] == [], 'Unverified diagnostic links')
    pair(meta['title_uz'], ru['title'], 'title')
    require(meta['title_ru'] == ru['title'], 'Title copies')
    skills = {s['key']: s for s in data['skills']}
    require(len(data['skills']) == len(skills) == 5, 'Five unique skills')
    require(set(ru['skills']) == set(skills), 'Skill locale coverage')
    for key, skill in skills.items():
        pair(skill['title_uz'], ru['skills'][key], key)
        require(set(skill['prerequisite_keys']) <= set(skills), 'Unknown prerequisite')
        def visit(current, path):
            require(current not in path, 'Prerequisite cycle')
            for parent in skills[current]['prerequisite_keys']:
                visit(parent, path | {current})
        visit(key, set())
    lessons = {l['key']: l for l in data['lessons']}
    require(len(data['lessons']) == len(lessons) == 5 and set(ru['lessons']) == set(lessons), 'Five bilingual lessons')
    require(Counter(l['skill_key'] for l in lessons.values()) == Counter(skills.keys()), 'Lesson skill coverage')
    for key, lesson in lessons.items():
        t = ru['lessons'][key]
        pair(lesson['title_uz'], t['title'], key)
        pair(lesson['outcome_uz'], t['outcome'], key)
        require(len(lesson['theory_uz']) == len(t['theory']) >= 3, 'Theory paragraphs')
        for a, b in zip(lesson['theory_uz'], t['theory']):
            pair(a, b, key)
        ex, rex = lesson['worked_example'], t['worked_example']
        pair(ex['prompt_uz'], rex['prompt'], key)
        pair(ex['answer_uz'], rex['answer'], key)
        require(len(ex['solution_steps_uz']) == len(rex['solution_steps']) >= 2, 'Example steps')
        for a, b in zip(ex['solution_steps_uz'], rex['solution_steps']):
            pair(a, b, key)
    exercises = {q['key']: q for q in data['exercises']}
    require(len(data['exercises']) == len(exercises) == 20 and set(ru['exercises']) == set(exercises), 'Twenty bilingual questions')
    prompts = set()
    for key, item in exercises.items():
        t = ru['exercises'][key]
        require(item['skill_key'] in skills, 'Question skill')
        require(item['purpose'] in ('practice', 'precheck', 'postcheck'), 'Purpose')
        require(item['prompt_uz'] not in prompts, 'Repeated prompt')
        prompts.add(item['prompt_uz'])
        pair(item['prompt_uz'], t['prompt'], key)
        pair(item['common_error_uz'], t['common_error'], key)
        require(len(item['solution_steps_uz']) == len(t['solution_steps']) >= 2, 'Solution steps')
        for a, b in zip(item['solution_steps_uz'], t['solution_steps']):
            pair(a, b, key)
        if item['purpose'] == 'practice':
            pair(item['hint_uz'], t['hint'], key)
        else:
            require(item['hint_uz'] is None and t['hint'] is None, 'Check hint leak')
        if item['format'] == 'single':
            options = {o['id']: o for o in item['options']}
            require(len(options) == len(item['options']) == 3, 'Three unique options')
            require(set(t['options']) == set(options), 'Option locale coverage')
            require(len({o['text_uz'] for o in options.values()}) == 3, 'Duplicate option')
            require(set(item['answer_key']) == {'option_id'} and item['answer_key']['option_id'] in options, 'Answer ID')
            for oid, option in options.items():
                pair(option['text_uz'], t['options'][oid]['text'], key)
                pair(option['feedback_uz'], t['options'][oid]['feedback'], key)
        else:
            require(item['format'] == 'numeric' and not item['options'] and not t['options'], 'Numeric format')
            require(set(item['answer_key']) == {'value'} and re.fullmatch(r'-?\d+', item['answer_key']['value']), 'Numeric answer')
        require(item['source']['origin'] == 'authored' and item['source']['id'] == 'authored-cluster3', 'Question source')
    for skill in skills:
        require(Counter(q['purpose'] for q in exercises.values() if q['skill_key'] == skill) ==
                {'practice': 2, 'precheck': 1, 'postcheck': 1}, '2/1/1 coverage')
    for purpose in ('practice', 'precheck', 'postcheck'):
        order = data['blueprint'][purpose + '_order']
        require(len(order) == len(set(order)) and set(order) ==
                {k for k, q in exercises.items() if q['purpose'] == purpose}, 'Blueprint order')
    matched = data['blueprint']['matched_pairs']
    require(len(matched) == 5 and {m['skill_key'] for m in matched} == set(skills), 'Matched coverage')
    for m in matched:
        for purpose in ('precheck', 'postcheck'):
            item = exercises[m[purpose + '_key']]
            require(item['skill_key'] == m['skill_key'] and item['purpose'] == purpose, 'Matched purpose')


def reference_numeric():
    # These calculations are independent of the authored answer keys and API implementation.
    trace = 4
    trace += 2
    trace *= 3
    a = 3
    b = a
    a = 8
    return {
        'debug-trace-practice-1': trace,
        'debug-trace-precheck': b,
        'debug-trace-postcheck': sum([2, 5, 1]),
        'debug-breakpoint-practice-1': 7,  # paused BEFORE multiplication
        'review-tokens-postcheck': len([1, 2, 3]),
        'learn-signature-practice-1': min(4, 2),
        'learn-signature-precheck': min(1, 4),
        'learn-minimal-practice-1': [2, 5, 8].index(8),
        'learn-minimal-postcheck': -1 if 9 not in [1, 3] else [1, 3].index(9),
        'learn-limits-practice-1': 9 if 14 > 9 else 14,
        'learn-transfer-practice-2': min(5, 3),
        'learn-transfer-postcheck': 6 if 2 <= 6 <= 8 else None,
    }


def code_references():
    count = 0
    def check(condition):
        nonlocal count
        require(condition, f'Code reference #{count + 1}')
        count += 1
    for args, expected in [((2, 5), 7), ((-3, 3), 0), ((0, 0), 0)]:
        check(add(*args) == expected)
    for args, expected in [((200, 15), 170), ((200, 0), 200), ((200, 100), 0), ((0, 25), 0)]:
        check(discount(*args) == expected)
    for value, expected in [(0, False), (1, True), (2, True)]:
        check(can_borrow(value) is expected)
    for length in range(6):
        items = list(range(length))
        for limit in range(7):
            result = take(items, limit)
            check(result == [i for i in range(length) if i < limit])
            check(result is not items and items == list(range(length)))
    check(take([7, 8, 9]) == [7, 8])
    for bad, exception in [(-1, ValueError), (True, TypeError), (2.5, TypeError), ('2', TypeError)]:
        try:
            take([1], bad)
        except exception:
            count += 1
        else:
            raise ValueError('Expected take exception')
    check(find([4, 4, 9], 4) == 0)
    check(find([], 2, -1) == -1)
    check(find([1], 2) is None)
    for x, expected in [(-3, 0), (0, 0), (4, 4), (10, 10), (15, 10)]:
        check(clip(x) == expected)
    check(clip(15, 3, 12) == 12)
    try:
        clip(5, 8, 2)
    except ValueError:
        count += 1
    else:
        raise ValueError('Expected clip exception')
    check('a,b,c'.split(',', maxsplit=1) == ['a', 'b,c'])
    catalog = {'b1': {'title': 'Algorithms', 'total': 1, 'available': 1}}
    loans = {}
    copy = find_book(catalog, 'b1')
    copy['available'] = 999
    check(catalog['b1']['available'] == 1)
    check(find_book(catalog, 'absent') is None)
    def invariant():
        check(catalog['b1']['available'] >= 0)
        check(catalog['b1']['available'] + sum(v for (_, book), v in loans.items() if book == 'b1') == 1)
    check(borrow(catalog, loans, 'r1', 'b1') == 'ok')
    invariant()
    before = deepcopy((catalog, loans))
    check(borrow(catalog, loans, 'r2', 'b1') == 'unavailable')
    check((catalog, loans) == before)
    check(return_book(catalog, loans, 'r2', 'b1') == 'no_loan')
    check((catalog, loans) == before)
    check(return_book(catalog, loans, 'r1', 'absent') == 'not_found')
    check(borrow(catalog, loans, 'r1', 'absent') == 'not_found')
    check((catalog, loans) == before)
    check(return_book(catalog, loans, 'r1', 'b1') == 'ok')
    invariant()
    check(not loans)
    check(borrow(catalog, loans, 'r2', 'b1') == 'ok')
    invariant()
    # Multiple copies and multiple readers test conservation beyond the single-copy demo.
    catalog = {'b1': {'title': 'Algorithms', 'total': 3, 'available': 3}}
    loans = {}
    for reader in ['r1', 'r1', 'r2']:
        check(borrow(catalog, loans, reader, 'b1') == 'ok')
        check(catalog['b1']['available'] + sum(loans.values()) == 3)
    for reader in ['r1', 'r2', 'r1']:
        check(return_book(catalog, loans, reader, 'b1') == 'ok')
        check(catalog['b1']['available'] + sum(loans.values()) == 3)
    check(catalog['b1']['available'] == 3 and not loans)
    # Intentional syntax fault remains visible in the student starter.
    try:
        compile((HERE / 'debugging-starter.py.txt').read_text(), 'starter', 'exec')
    except SyntaxError:
        count += 1
    else:
        raise ValueError('Starter must preserve intended syntax error')
    return count


def git_references():
    count = 0
    with tempfile.TemporaryDirectory(prefix='mindmetric-cluster3-') as name:
        root = Path(name).resolve()
        require(root.parent == Path(tempfile.gettempdir()).resolve(), 'Temporary Git workspace boundary')
        def git(*args, ok=True):
            result = subprocess.run(['git', '-c', 'core.autocrlf=false', *args], cwd=root,
                                    capture_output=True, text=True, encoding='utf-8', timeout=20)
            if ok:
                require(result.returncode == 0, f'Git {args}: {result.stderr}')
            return result
        def check(condition):
            nonlocal count
            require(condition, f'Git reference #{count + 1}')
            count += 1
        git('init', '-b', 'main')
        git('config', 'user.name', 'MindMetric local QA')
        git('config', 'user.email', 'qa@example.invalid')
        (root / 'a.txt').write_text('v1\n')
        (root / 'POLICY.md').write_text('display_limit=2\n')
        git('add', '.')
        git('commit', '-m', 'baseline')
        (root / 'a.txt').write_text('v2\n')
        git('add', 'a.txt')
        (root / 'a.txt').write_text('v3\n')
        check(git('show', ':a.txt').stdout.strip() == 'v2')
        check('v2' in git('diff', '--staged').stdout)
        check('v3' in git('diff').stdout)
        git('commit', '-m', 'staged v2')
        check(git('show', 'HEAD:a.txt').stdout.strip() == 'v2')
        check((root / 'a.txt').read_text().strip() == 'v3')
        git('add', 'a.txt')
        git('commit', '-m', 'restaged v3')
        check(git('show', 'HEAD:a.txt').stdout.strip() == 'v3')
        check(not git('remote').stdout.strip())
        baseline = git('rev-parse', 'HEAD').stdout.strip()
        git('switch', '-c', 'review-a')
        (root / 'POLICY.md').write_text('display_limit=3\n')
        git('add', 'POLICY.md')
        git('commit', '-m', 'limit 3')
        a_head = git('rev-parse', 'HEAD').stdout.strip()
        git('switch', '-c', 'review-b', baseline)
        (root / 'POLICY.md').write_text('display_limit=5\n')
        git('add', 'POLICY.md')
        git('commit', '-m', 'limit 5')
        git('switch', 'main')
        git('merge', 'review-a')
        check(git('rev-parse', 'HEAD').stdout.strip() == a_head)
        check(git('branch', '--show-current').stdout.strip() == 'main')
        conflict = git('merge', 'review-b', ok=False)
        check(conflict.returncode == 1 and '<<<<<<<' in (root / 'POLICY.md').read_text())
        (root / 'POLICY.md').write_text('display_limit=4\n')
        git('add', 'POLICY.md')
        git('commit', '-m', 'resolve according to contract')
        check(not git('status', '--porcelain').stdout.strip())
        check((root / 'POLICY.md').read_text().strip() == 'display_limit=4')
        check(git('rev-parse', 'review-a').stdout.strip() == a_head)
    return count


def negative_cases(data, ru):
    mutations = [
        ('missing translation', lambda d, r: r['lessons'].pop(next(iter(r['lessons'])))),
        ('empty Russian title', lambda d, r: r.update(title='')),
        ('wrong answer ID', lambda d, r: d['exercises'][0].update(answer_key={'option_id': 'z'})),
        ('duplicate question', lambda d, r: d['exercises'].append(deepcopy(d['exercises'][0]))),
        ('invalid locale option', lambda d, r: r['exercises'][d['exercises'][0]['key']]['options'].pop('a')),
        ('check hint', lambda d, r: d['exercises'][2].update(hint_uz='yordam')),
        ('unknown skill', lambda d, r: d['exercises'][0].update(skill_key='absent')),
        ('prerequisite cycle', lambda d, r: d['skills'][0].update(prerequisite_keys=[d['skills'][-1]['key']])),
        ('blueprint overlap', lambda d, r: d['blueprint']['postcheck_order'].append(d['blueprint']['precheck_order'][0])),
        ('matched pair purpose', lambda d, r: d['blueprint']['matched_pairs'][0].update(postcheck_key=d['blueprint']['precheck_order'][0])),
        ('changed constant', lambda d, r: r['exercises'][d['exercises'][0]['key']].update(prompt='Python 3: print(8 / 0). Какая ошибка?')),
        ('changed code', lambda d, r: r['lessons'][d['lessons'][0]['key']]['worked_example'].update(
            prompt=r['lessons'][d['lessons'][0]['key']]['worked_example']['prompt'].replace('4 > 2', '4 < 2'))),
        ('claim importability', lambda d, r: d.update(integration_status='ready')),
    ]
    rejected = []
    for label, mutate in mutations:
        d, r = deepcopy(data), deepcopy(ru)
        mutate(d, r)
        r['source_hash'] = digest(d)  # test validation beyond a stale hash
        try:
            validate(d, r)
        except (ValueError, KeyError, TypeError):
            rejected.append(label)
        else:
            raise ValueError(f'Negative case escaped: {label}')
    bad = deepcopy(ru)
    bad['source_hash'] = '0' * 64
    try:
        validate(data, bad)
    except ValueError:
        rejected.append('stale locale hash')
    else:
        raise ValueError('Hash negative case escaped')
    return rejected


def main():
    manifest = read(HERE / 'authoring-manifest.json')
    for name, expected in manifest.items():
        require(hashlib.sha256((HERE / name).read_text(encoding='utf-8').encode()).hexdigest() == expected,
                f'Authoring hash: {name}; rebuild resources')
    curriculum = Path('D:/Downloads/Telegram Desktop/Oqitish moduli.docx')
    if curriculum.exists():
        require(hashlib.sha256(curriculum.read_bytes()).hexdigest() == CURRICULUM_SHA, 'Curriculum hash')
    refs = reference_numeric()
    found_numeric, all_keys, counts = {}, set(), Counter()
    first = None
    for builder in (module31, module32, module33, module34):
        authored = builder()
        key = authored['key']
        data = read(HERE / f'{key}.v1.json')
        ru = read(HERE / 'translations' / f'{key}.v1.ru.json')
        validate(data, ru)
        require(data['sources'][1]['sha256'] == digest(manifest), 'Source manifest reference')
        require(data['sources'][0]['sha256'] == CURRICULUM_SHA, 'Curriculum source reference')
        if first is None:
            first = (data, ru)
        require(not all_keys.intersection(q['key'] for q in data['exercises']), 'Cross-module duplicate')
        all_keys.update(q['key'] for q in data['exercises'])
        for row in data['exercises']:
            counts[row['format']] += 1
            if row['format'] == 'numeric':
                found_numeric[row['key']] = int(row['answer_key']['value'])
        # Check rotated answer mapping against the manually authored semantic choice.
        for lesson, source in zip(data['lessons'], authored['lessons']):
            for item, original in zip([q for q in data['exercises'] if q['skill_key'] == lesson['skill_key']], source['questions']):
                if original['options']:
                    selected = next(o for o in item['options'] if o['id'] == item['answer_key']['option_id'])
                    require(selected['text_uz'] == original['options'][0]['text']['uz'], 'Choice rotation/key mismatch')
        for language in ('uz', 'ru'):
            for audience in ('teacher', 'student', 'checks'):
                suffix = '' if audience == 'teacher' else f'.{audience}'
                path = HERE / f"{data['module']['topic_number']}-mavzu.{language}{suffix}.md"
                output = path.read_text(encoding='utf-8')
                require(output == markdown(data, ru, language, audience), f'Rendered resource drift: {path.name}')
                if audience != 'teacher':
                    for segment in output.split('### ')[1:]:
                        if '-practice-' in segment or '-precheck' in segment or '-postcheck' in segment:
                            require(not any(token in segment for token in ('Kalit:', 'Ключ:', 'Keng tarqalgan xato:', 'Типичная ошибка:')), 'Student feedback leak')
                if audience == 'checks':
                    require(not any(token in output for token in ('Ishora:', 'Подсказка:', 'Javob:', 'Ответ:', '-practice-')), 'Check answer/hint leak')
    require(found_numeric == refs, 'Independent numeric answer mismatch')
    require(len(all_keys) == 80, 'Total questions')
    tasks = build_activities()
    require(read(HERE / 'activities.v1.json')['activities'] == tasks and len(tasks) == 3, 'Activities source copy')
    for item in tasks:
        for field in ('title', 'goal'):
            pair(item[field]['uz'], item[field]['ru'], item['key'])
        for field in ('materials', 'contract', 'steps', 'deliverables', 'rubric', 'solution'):
            require(bool(item[field]), 'Empty activity field')
            for row in item[field]:
                pair(row['uz'], row['ru'], item['key'])
        for language in ('uz', 'ru'):
            for teacher in (False, True):
                suffix = '.teacher' if teacher else '.student'
                output = (HERE / f"{item['key']}.{language}{suffix}.md").read_text(encoding='utf-8')
                require(output == render(item, language, teacher), 'Activity render drift')
                if not teacher:
                    require('O‘qituvchi yechimi' not in output and 'Решение преподавателя' not in output, 'Activity solution leak')
    for language in ('uz', 'ru'):
        source = (HERE / f'bridge.{language}.md').read_text(encoding='utf-8')
        for code in re.findall(r'```python\n(.*?)```', source, re.S):
            compile(code, 'bridge', 'exec')
    for path in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if not target.startswith(('http:', 'https:', '#')):
                resolved = path.parent / target.split('#')[0]
                require(resolved.exists() or resolved == HERE / 'verification-result.json',
                        f'Broken local link: {path.name} -> {target}')
    rejected = negative_cases(*first)
    result = {'status': 'passed', 'scope': 'offline standalone resources only',
        'modules': 4, 'skills': 20, 'lessons': 20, 'worked_examples': 20, 'questions': 80,
        'question_formats': dict(counts), 'numeric_reference_answers': len(refs),
        'choice_key_rotation_checks': counts['single'], 'open_activities': 3,
        'python_reference_checks': code_references(), 'git_reference_checks': git_references(),
        'negative_cases_rejected': rejected, 'languages': ['uz', 'ru'],
        'curriculum_verified_on_this_host': curriculum.exists(),
        'integration_status': 'not_importable', 'external_pedagogical_review': False,
        'psychometric_calibration': False}
    write_json(HERE / 'verification-result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
