"""Offline stage-one content checks; no Django setup or database writes.

Run from the repository root:
    python docs/content/cluster1/validate_content.py
"""

import ast
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


def validate():
    folder = Path(__file__).resolve().parent
    root = folder.parents[2]
    data = json.loads((folder / 'arithmetic-algebra.v1.json').read_text(encoding='utf-8'))
    exercises = data['exercises']
    items = {q['key']: q for q in exercises}
    skills = {s['key']: s for s in data['skills']}
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    check(data['schema_version'] == 1, 'Unsupported schema version')
    check(data['module']['status'] == 'draft', 'Pilot content must remain draft')
    check(len(items) == len(exercises) == 20, 'Expected 20 unique exercises')
    check(len(skills) == len(data['skills']) == len(data['lessons']) == 5,
          'Expected five unique skills and five lessons')
    check(Counter(q['purpose'] for q in exercises) == {'practice': 10, 'precheck': 5, 'postcheck': 5},
          'Invalid purpose distribution')

    def visit(key, stack):
        check(key not in stack, f'Prerequisite cycle: {key}')
        if key in stack:
            return
        for parent in skills[key]['prerequisite_keys']:
            check(parent in skills, f'Unknown prerequisite: {parent}')
            if parent in skills:
                visit(parent, stack | {key})

    for key in skills:
        visit(key, set())
        check(Counter(q['purpose'] for q in exercises if q['skill_key'] == key)
              == {'practice': 2, 'precheck': 1, 'postcheck': 1}, f'Coverage: {key}')
        check(sum(lesson['skill_key'] == key for lesson in data['lessons']) == 1,
              f'Lesson coverage: {key}')
    for lesson in data['lessons']:
        check(lesson['theory_uz'] and lesson['worked_example']['solution_steps_uz']
              and lesson['worked_example']['answer_uz'], f'Incomplete lesson: {lesson["key"]}')

    sources = {source['id']: source for source in data['sources']}
    for q in exercises:
        key = q['key']
        check(q['skill_key'] in skills, f'Unknown skill: {key}')
        check(q['source']['id'] in sources and q['source']['locator'], f'Source: {key}')
        check(q['prompt_uz'] and q['solution_steps_uz'] and q['common_error_uz'], f'Empty content: {key}')
        check(q['difficulty'] in {'easy', 'medium', 'hard'}, f'Difficulty: {key}')
        check(bool(q['hint_uz']) if q['purpose'] == 'practice' else q['hint_uz'] is None,
              f'Hint policy: {key}')
        if q['format'] == 'numeric':
            F(q['answer_key']['value'])
            check(not q['options'], f'Numeric question has options: {key}')
        elif q['format'] == 'single':
            ids = [option['id'] for option in q['options']]
            check(len(ids) == len(set(ids)) and len(ids) >= 2, f'Invalid options: {key}')
            check(q['answer_key']['option_id'] in ids, f'Invalid answer option: {key}')
            check(all(option['feedback_uz'] and option['text_uz'] for option in q['options']),
                  f'Missing option text or feedback: {key}')
        else:
            check(False, f'Unsupported format: {key}')

    for purpose in ('precheck', 'practice', 'postcheck'):
        keys = data['blueprint'][purpose + '_order']
        check(len(keys) == len(set(keys)) and set(keys)
              == {q['key'] for q in exercises if q['purpose'] == purpose}, f'Blueprint: {purpose}')
    for pair in data['blueprint']['matched_pairs']:
        for field in ('precheck_key', 'postcheck_key'):
            q = items[pair[field]]
            check(q['skill_key'] == pair['skill_key'] and q['difficulty'] == pair['difficulty'],
                  f'Mismatched pair: {pair["skill_key"]}')
    practice = data['blueprint']['practice_order']
    for offset in (0, 5):
        check({items[key]['skill_key'] for key in practice[offset:offset + 5]} == skills.keys(),
              f'Practice round must cover five skills: {offset}')
    check(len({q['prompt_uz'] for q in exercises}) == 20, 'Duplicate prompts')

    # Independent exact calculations written from the mathematical questions.
    # This catches incorrect keys; it does not prove psychometric equivalence.
    expected_numbers = {
        'arith-practice-01': 24 - F(3 * (2 + 4), 2) + 5,
        'arith-practice-02': (3 + 5)**2 - (3 - 5)**2,
        'arith-practice-03': 2 * (-3)**3 - 4 * (-3) + 7,
        'arith-practice-04': F(4**2 - 9, 4**2 - 3 * 4),
        'arith-practice-05': 12 + 5 - 2**3,
        'arith-practice-08': F('3.5') * 4 - F(5, 6) * 12,
        'arith-practice-09': (2 * 2 - 3) * (2 * 2 + 3) + 3**2,
        'arith-precheck-02': F(3, 4) - F(1, 6),
        'arith-precheck-03': 2 * (-2)**2 - (-2),
        'arith-postcheck-01': F(18, (2 + 1)**2) + 7,
        'arith-postcheck-02': F(3, 5) * (1 - F(1, 4)),
        'arith-postcheck-03': (-3) * 2 - 2**2,
    }
    for key, value in expected_numbers.items():
        check(F(items[key]['answer_key']['value']) == value, f'Mathematics: {key}; expected {value}')

    # Option id and mathematical property are both checked. Symbolic identities
    # below use coefficient equality, not just a substitution at one point.
    expected_options = {
        'arith-practice-06': ('b', 2 == 2 and -3 != 2),
        'arith-practice-07': ('b', (1, 0, 0, -8) == (1, 2-2, 4-4, -8)
                             and (3-2)*(3**2+2*3+4) == 19),
        'arith-practice-10': ('c', F(6 * 15, 9) == 10),
        'arith-precheck-01': ('a', ((-3)**2, -3**2) == (9, -9)),
        'arith-precheck-04': ('c', (3-2, 3*4) == (1, 12)),
        'arith-precheck-05': ('c', F(3*5-1, 2) == 7),
        'arith-postcheck-04': ('b', (1, -2*3, 3**2) == (1, -6, 9)),
        'arith-postcheck-05': ('d', 2*(5+3) == 5+11),
    }
    for key, (option, valid) in expected_options.items():
        check(valid and items[key]['answer_key']['option_id'] == option, f'Mathematics: {key}')
    check(set(expected_numbers) | set(expected_options) == set(items), 'Missing independent answer check')

    tree = ast.parse((root / 'backend/apps/assessments/content.py').read_text(encoding='utf-8'))
    assignment = next(node for node in tree.body if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == 'MCQ_QUESTIONS'
                              for target in node.targets))
    bank = ast.literal_eval(assignment.value)
    existing = {q['key'] for group in bank.values() for q in group}
    for link in data['diagnostic_links']:
        check(link['question_key'] in existing, f'Unknown diagnostic: {link["question_key"]}')
        check(set(link['skill_keys']) <= skills.keys(), f'Unknown diagnostic skill: {link}')

    # Optional provenance check. Content checks do not depend on the Downloads path.
    if len(sys.argv) == 2:
        for source in sources.values():
            file = Path(sys.argv[1]) / source['filename']
            check(file.exists(), f'Missing source: {file.name}')
            if file.exists():
                digest = hashlib.sha256(file.read_bytes()).hexdigest().upper()
                check(digest == source['sha256'], f'Source changed: {file.name}')

    print(json.dumps({'exercises': len(items), 'lessons': len(data['lessons']), 'skills': len(skills),
                      'diagnostic_links': len(data['diagnostic_links']),
                      'independent_answer_checks': len(expected_numbers) + len(expected_options),
                      'errors': errors}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(validate())
