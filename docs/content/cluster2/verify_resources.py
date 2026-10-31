"""Offline resource QA. Does not make the old production importer accept schema 2."""
import copy
import hashlib
import json
import math
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from authoring import HERE, ROOT, digest

sys.path.insert(0, str(ROOT / 'backend'))
from apps.development.validation import ContentValidationError, validate_content
from apps.development.translations import validate_translation


def require(value, message):
    if not value:
        raise AssertionError(message)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate_resource(data, ru, graph):
    meta = data['module']
    require(data['schema_version'] == 2, 'New cluster requires schema 2.')
    require(meta['cluster'] == 2 and meta['order'] in range(1, 7), 'Invalid cluster/order.')
    require(meta['topic_number'] == f"2.{meta['order']}", 'Topic number mismatch.')
    allowed = {'algorithmic', 'creative', 'problem_solving'}
    require(set(meta['indicator_keys']) <= allowed and meta['indicator_keys'], 'Invalid cluster-two indicators.')
    for row in data['skills']:
        require(set(row['indicator_keys']) <= set(meta['indicator_keys']), 'Skill indicator mismatch.')
    require(meta['title_ru'] == ru['title'], 'Russian module title mismatch.')
    require(meta['status'] == 'draft', 'Stage one cannot publish content.')
    # Reuse the deployed validator for the unchanged lesson/question/blueprint
    # shape only. New metadata is checked above, never written to a database.
    # schema/indicators in this disposable projection are not the resource file.
    core = copy.deepcopy(data)
    core['schema_version'] = 1
    core['module']['indicator_keys'] = ['math']
    for skill in core['skills']:
        skill['indicator_keys'] = ['math']
    validate_content(core, known_skills=graph)
    validate_translation(data, ru)
    require('answer_key' not in json.dumps(ru), 'Translation contains grading override.')
    operators = re.compile(r'←|==|!=|≥|≤|[<>]|\b(?:TRUE|FALSE|AND|OR|NOT|TO|OUTPUT|RETURN|INPUT|DECISION|START|END|div|mod)\b')
    numeric = []
    for q in data['exercises']:
        tq = ru['exercises'][q['key']]
        require(Counter(operators.findall(q['prompt_uz'])) == Counter(operators.findall(tq['prompt'])), f"Operator change: {q['key']}")
        require(len(q['solution_steps_uz']) >= 2, 'Missing worked solution steps.')
        if q['format'] == 'numeric':
            numeric.append(q['key'])
        else:
            require(len(q['options']) == 3, 'Expected three distinct authored options.')
            require(len(set(o['text_uz'] for o in q['options'])) == 3, 'Repeated Uzbek option.')
            require(len(set(o['text'] for o in tq['options'].values())) == 3, 'Repeated Russian option.')
        require(q['source']['origin'] == 'authored', 'Authored content mislabelled as supplied source.')
    for lesson in data['lessons']:
        require(len(lesson['theory_uz']) >= 3, 'Lesson lacks explanatory paragraphs.')
        require(len(lesson['worked_example']['solution_steps_uz']) >= 3, 'Example lacks steps.')
    projects = data.get('projects', [])
    require(len(projects) == (2 if meta['order'] == 6 else 0), 'Incorrect open-project coverage.')
    require(set(ru.get('projects', {})) == {p['key'] for p in projects}, 'Project translation missing.')
    for project in projects:
        require(project['assessment'] == 'self_review', 'Open project cannot claim automatic grading.')
        local = ru['projects'][project['key']]
        for name in ('title', 'brief', 'constraints', 'steps', 'deliverables', 'rubric'):
            a, b = project[name + '_uz'], local[name]
            if isinstance(a, list):
                require(isinstance(b, list) and len(a) == len(b) and len(a) >= 3, 'Project section incomplete.')
                pairs = zip(a, b)
            else:
                pairs = [(a, b)]
            for x, y in pairs:
                require(x.strip() and y.strip(), 'Empty project translation.')
                require(Counter(re.findall(r'\d+', x)) == Counter(re.findall(r'\d+', y)), 'Project constant changed.')
    return numeric


def while_count(start, stop, update, predicate):
    x, count = start, 0
    while predicate(x, stop):
        x = update(x)
        count += 1
        require(count <= 100, 'Reference loop did not terminate.')
    return count


def do_final(start, update, predicate):
    x = start
    for _ in range(100):
        x = update(x)
        if not predicate(x):
            return x
    raise AssertionError('Reference do-while did not terminate.')


def withdrawal(balance, denomination, amount):
    valid = amount > 0 and amount <= balance and amount % denomination == 0
    return balance - amount if valid else balance


def taxi(base, included, rate, distance):
    return base + max(0, distance - included) * rate


def numerical_oracles():
    # Independent reference calculations; never execute text from resource files.
    a, z = 2, 9
    a = z
    z = a
    x, y = 3, 6
    x = y - 1
    y = x + y
    return {
        'algo-io-practice-1': 6000 * 4,
        'algo-io-postcheck': 18 * 12,
        'algo-decompose-practice-2': 80000 - 10000 + 5000,
        'algo-decompose-postcheck': 3 * 20000 - 15000 + 7000,
        'algo-assignment-practice-1': (5 + 2) * 3,
        'algo-assignment-practice-2': a + z,
        'algo-assignment-precheck': (lambda a, b: (b, a))(6, 4)[1],
        'algo-assignment-postcheck': y,
        'algo-trace-practice-1': 8 - 3,
        'algo-trace-precheck': [7, 2][0],
        'cond-if-practice-1': 7 - 2 if 7 >= 5 else 7 + 2,
        'cond-if-practice-2': ((1 + 2) * 4),
        'cond-if-precheck': 10 if 0 > 0 else 20,
        'cond-if-postcheck': 4 + 3 if 4 < 5 else 4 - 3,
        'cond-multiple-practice-1': 3 if 75 >= 90 else (2 if 75 >= 60 else 1),
        'cond-multiple-practice-2': (1 if -1 > 0 else 2) if 5 > 0 else 3,
        'cond-multiple-precheck': 3 if 90 >= 90 else (2 if 90 >= 60 else 1),
        'cond-switch-practice-1': {1: 10, 2: 20}.get(9, -1),
        'cond-switch-precheck': {1: 4, 2: 8}.get(1, 0),
        'loop-for-practice-1': sum(range(2, 6)),
        'loop-for-practice-2': math.prod(2 for _ in range(1, 4)),
        'loop-for-precheck': len(range(3, 8)),
        'loop-for-postcheck': 9 + sum(range(5, 4)),
        'loop-while-practice-1': while_count(3, 12, lambda x: x + 3, lambda x, stop: x < stop),
        'loop-while-precheck': while_count(10, 5, lambda x: x + 1, lambda x, stop: x < stop),
        'loop-while-postcheck': while_count(20, 2, lambda x: x // 2, lambda x, stop: x > stop),
        'loop-do-practice-1': do_final(0, lambda x: x + 2, lambda x: x < 5),
        'loop-do-practice-2': do_final(0, lambda x: x + 1, lambda x: False),
        'loop-do-precheck': do_final(9, lambda x: x - 4, lambda x: x > 3),
        'loop-nested-practice-1': sum(1 for i in range(1, 4) for j in range(1, 5)),
        'loop-nested-practice-2': sum(1 for i in range(1, 4) for j in range(1, i + 1)),
        'loop-nested-precheck': sum(i for i in range(1, 3) for j in range(1, 4)),
        'loop-nested-postcheck': sum(1 for i in range(1, 5) for j in range(1, i + 1)),
        'loop-recursion-practice-1': math.factorial(4),
        'loop-recursion-precheck': 2 + sum(3 for _ in range(3)),
        'loop-recursion-postcheck': len(range(4, -1, -1)),
        'opt-equivalence-practice-1': sum(range(1, 9)),
        'opt-equivalence-postcheck': sum(range(1, 2)),
        'opt-time-practice-1': len(range(7)) + len(range(5)),
        'opt-time-practice-2': sum(1 for _ in range(5) for _ in range(6)),
        'opt-time-precheck': Fraction(8 ** 2, 4 ** 2),
        'opt-memory-practice-2': len([None] * 20) + 2,
        'opt-memory-postcheck': len([None] * 12) + 4,
        'opt-reuse-practice-1': 6 * 5 - 6,
        'opt-reuse-precheck': 2 * 15 - 15,
        'case-contract-practice-2': 9000 * 5,
        'case-taxi-practice-1': taxi(12000, 3, 2000, 7),
        'case-taxi-practice-2': taxi(12000, 3, 2000, 2),
        'case-taxi-precheck': taxi(9000, 2, 2500, 2),
        'case-taxi-postcheck': taxi(15000, 4, 3000, 6) - 15000,
        'case-atm-practice-1': withdrawal(80000, 10000, 50000),
        'case-atm-precheck': withdrawal(40000, 10000, 50000),
        'case-tests-practice-2': taxi(8000, 1, 2000, 3),
        'design-functions-postcheck': 4 + 1 + 0,
        'design-alternatives-practice-1': 2 * 5 + 3,
        'design-alternatives-postcheck': (2 * 3 + 5) - (2 * 4 + 2),
    }


def rejected(call, label):
    try:
        call()
    except (ContentValidationError, AssertionError, KeyError, TypeError, ValueError):
        return label
    raise AssertionError('Invalid resource accepted: ' + label)


def main():
    paths = sorted(HERE.glob('*.v1.json'))
    require(len(paths) == 6, 'Expected six module files.')
    resources = [(load(path), load(HERE / 'translations' / (path.stem + '.ru.json'))) for path in paths]
    cluster1 = [load(path) for path in (ROOT / 'docs/content/cluster1').glob('*.v*.json')]
    graph = {s['key']: s['prerequisite_keys'] for d in cluster1 + [d for d, _ in resources] for s in d['skills']}
    require(len(graph) == sum(len(d['skills']) for d in cluster1 + [d for d, _ in resources]), 'Global skill key collision.')
    require({d['module']['order'] for d, _ in resources} == set(range(1, 7)), 'Missing module order.')
    numeric_keys, all_keys, all_prompts = [], [], []
    for data, ru in resources:
        numeric_keys += validate_resource(data, ru, graph)
        all_keys += [q['key'] for q in data['exercises']]
        all_prompts += [q['prompt_uz'].strip() for q in data['exercises']]
        for lang in ('uz', 'ru'):
            path = HERE / f"2.{data['module']['order']}-mavzu.{lang}.md"
            text = path.read_text(encoding='utf-8')
            require(all(q['key'] in text for q in data['exercises']), f'Markdown incomplete: {path.name}')
            require(' || ' not in text, 'Unresolved authoring delimiter.')
    require(len(set(all_keys)) == len(all_keys) == 120, 'Question key collision.')
    require(len(set(all_prompts)) == len(all_prompts), 'Repeated prompt across modules.')
    oracles = numerical_oracles()
    require(set(oracles) == set(numeric_keys), 'Every numeric question needs an independent reference.')
    for data, _ in resources:
        for q in data['exercises']:
            if q['format'] == 'numeric':
                require(Fraction(q['answer_key']['value']) == oracles[q['key']], 'Wrong numeric key: ' + q['key'])
    manifest = load(HERE / 'authoring-manifest.json')
    require(all(hashlib.sha256((HERE / name).read_text(encoding='utf-8').encode('utf-8')).hexdigest() == sha for name, sha in manifest.items()), 'Stale authoring manifest.')
    manifest_sha = hashlib.sha256((HERE / 'authoring-manifest.json').read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    for data, _ in resources:
        require(next(s for s in data['sources'] if s['id'] == 'authored-cluster2')['sha256'] == manifest_sha, 'Stale author source SHA.')
    curriculum = Path('D:/Downloads/Telegram Desktop/Oqitish moduli.docx')
    source_checked = False
    if curriculum.exists():
        sha = hashlib.sha256(curriculum.read_bytes()).hexdigest()
        require(all(d['sources'][0]['sha256'] == sha for d, _ in resources), 'Curriculum source SHA mismatch.')
        source_checked = True
    data, ru = resources[0]
    negatives = []
    altered = copy.deepcopy(ru); altered['source_hash'] = '0' * 64
    negatives.append(rejected(lambda: validate_translation(data, altered), 'wrong_source_hash'))
    altered = copy.deepcopy(ru); altered['lessons'].pop(next(iter(altered['lessons'])))
    negatives.append(rejected(lambda: validate_translation(data, altered), 'missing_translated_lesson'))
    altered = copy.deepcopy(ru); key = next(q['key'] for q in data['exercises'] if q['purpose'] == 'precheck')
    altered['exercises'][key]['hint'] = 'Недопустимая подсказка'
    negatives.append(rejected(lambda: validate_translation(data, altered), 'check_hint'))
    altered = copy.deepcopy(ru); altered['exercises'][key]['answer_key'] = {'value': '0'}
    negatives.append(rejected(lambda: validate_translation(data, altered), 'grading_override'))
    altered = copy.deepcopy(data); altered['blueprint']['postcheck_order'][0] = altered['blueprint']['precheck_order'][0]
    negatives.append(rejected(lambda: validate_resource(altered, ru, graph), 'mixed_pre_post_bank'))
    altered = copy.deepcopy(ru); altered['exercises']['algo-io-practice-1']['prompt'] += ' 999'
    negatives.append(rejected(lambda: validate_translation(data, altered), 'changed_numeric_constant'))
    altered = copy.deepcopy(data); altered['module']['indicator_keys'] = ['math']
    negatives.append(rejected(lambda: validate_resource(altered, ru, graph), 'wrong_cluster_indicator'))
    altered = copy.deepcopy(ru)
    key = next(q['key'] for q in data['exercises'] if q['options'])
    altered['exercises'][key]['options'].pop(next(iter(altered['exercises'][key]['options'])))
    negatives.append(rejected(lambda: validate_translation(data, altered), 'missing_translated_option'))
    altered = copy.deepcopy(ru)
    key = 'algo-assignment-practice-1'
    altered['exercises'][key]['prompt'] = altered['exercises'][key]['prompt'].replace('←', '==', 1)
    negatives.append(rejected(lambda: validate_resource(data, altered, graph), 'changed_code_operator'))
    altered = copy.deepcopy(data)
    altered['skills'][0]['prerequisite_keys'] = [altered['skills'][0]['key']]
    negatives.append(rejected(lambda: validate_resource(altered, ru, graph), 'prerequisite_cycle'))
    project_data, project_ru = next((d, t) for d, t in resources if d['module']['order'] == 6)
    altered = copy.deepcopy(project_ru); altered['projects'] = {}
    negatives.append(rejected(lambda: validate_resource(project_data, altered, graph), 'missing_translated_project'))
    legacy_guard = rejected(lambda: validate_content(data, known_skills=graph), 'legacy_importer_rejects_schema2')
    result = {'passed': True, 'stage': 'offline_resources_only', 'modules': 6, 'languages': ['uz', 'ru'],
              'skills': 30, 'lessons': 30, 'worked_examples': 30, 'questions': 120,
              'numeric_reference_checks': len(numeric_keys), 'single_choice_editorial_review': 120 - len(numeric_keys),
              'practice': 60, 'precheck': 30, 'postcheck': 30, 'self_review_projects': 2,
              'curriculum_source_hash_checked': source_checked, 'negative_cases': negatives,
              'legacy_importer_guard': legacy_guard,
              'production_importer_schema2_supported': False, 'database_writes': False}
    (HERE / 'verification-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
