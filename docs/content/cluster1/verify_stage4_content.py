"""Offline structure/provenance checks and separately calculated stage-four answers.

The oracles below encode question inputs independently of the authoring script.
They do not infer psychometric equivalence or replace an external content review.
"""

import argparse
import hashlib
import itertools
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'backend'))

from apps.assessments.content import MCQ_QUESTIONS
from apps.development.numeric import parse_numeric
from apps.development.validation import validate_content


def normalized(value):
    return ' '.join(str(value).replace('−', '-').split())


def set_text(values):
    return '{' + ','.join(str(value) for value in sorted(values)) + '}' if values else '∅'


def matrix_text(values):
    return json.dumps(values, separators=(',', ':'))


def product(a, b):
    assert len(a[0]) == len(b)
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def determinant(a):
    return a[0][0]*a[1][1] - a[0][1]*a[1][0]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def shape(a):
    return f'{len(a)}×{len(a[0])}'


def implies(a, b):
    return not a or b


ROWS = list(itertools.product((False, True), repeat=2))
EXPRESSIONS = {
    'A': lambda a,b:a, 'B': lambda a,b:b, '¬A': lambda a,b:not a,
    '0': lambda a,b:False, '1': lambda a,b:True,
    '¬A∧¬B': lambda a,b:not a and not b, '¬A∨¬B': lambda a,b:not a or not b,
    'A∧B': lambda a,b:a and b, 'A∨¬B': lambda a,b:a or not b,
    'A∨B': lambda a,b:a or b,
}


def expected_answers():
    values = {}

    def assign(prefix, purpose, answers):
        for i, answer in enumerate(answers, 1):
            values[f'{prefix}-{purpose}-{i:02d}'] = answer

    false_pair = next((a,b) for a,b in ROWS if not implies(a,b))
    implication_failure = f'A={int(false_pair[0])}, B={int(false_pair[1])}'
    assign('logic','practice',[
        '7 tub son.', int(9 % 2 == 0), int((True or False) and not True), 'Kon’yunksiya (∧)',
        implication_failure, int(False == False), 2**len({'A','B'}),
        ','.join(str(int(a or b)) for a,b in ROWS), '¬A∧¬B', 'A',
    ])
    assign('logic','precheck',[
        int(12 < 5), int(not False and True), implication_failure, 2**3, 'A',
    ])
    assign('logic','postcheck',[
        'Ochiq ifoda; rostligi hali aniqlanmagan', int((True and False) or not True),
        int(implies(False,False)), sum(a and b for a,b in ROWS), 'A',
    ])
    assign('sets','practice',[
        2**len({'a','b'}), len({1,1,2,3}), set_text({1,2,3,4,5}|{4,5,6,7}),
        set_text({1,2,3,4,5}-{4,5,6,7}), set_text(set(range(1,11))-{2,4,6,8,10}),
        set_text(set('abcd')-set('ac')), sum([3,2,4]), 'A∖B', 12+15-4, 40-(25+20-8),
    ])
    assign('sets','precheck',[
        int(4 in {2,4}), set_text({1,3,5}&{3,4,5}), set_text({1,2,3,4,5}-{1,5}), 5+2, 14+11-5,
    ])
    universe, a = set('abcde'), set('bde')
    assign('sets','postcheck',[
        len({frozenset()}), set_text({1,2,3}-{2,4,6}), set_text(universe-(universe-a)), 7-3, 22+19-34,
    ])
    assign('seq','practice',[
        'Ruxsat etilgan barcha x qiymatlari to‘plami', 'x≠2', 3+(10-1)*4,
        sum(2+i*3 for i in range(5)), 2*3**(4-1), sum(5*2**i for i in range(4)),
        math.factorial(5), math.factorial(4), math.comb(7,3), math.perm(5,3),
    ])
    assign('seq','precheck',[
        'x≥1', 10+(7-4), 12*Fraction(6,3), math.factorial(3)+math.factorial(2), math.comb(6,2),
    ])
    assign('seq','postcheck',[
        f'x≠−{math.isqrt(9)} va x≠{math.isqrt(9)}', 11-3*3, 4*Fraction(1,2)**2,
        next(n for n in range(1,10) if math.factorial(n)==720), math.perm(5,2),
    ])
    a,b = [[1,-2],[3,4]],[[2,5],[-1,0]]
    assign('matrix','practice',[
        shape([[2,1],[4,3]]), len([[0,0] for _ in range(3)])*2,
        matrix_text(identity(2)), 'Diagonal, ammo birlik emas',
        matrix_text([[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]),
        matrix_text([[-2*x for x in row] for row in [[3,0],[-1,4]]]),
        'A ustunlari soni B qatorlari soniga teng',
        matrix_text(product([[1,2],[0,1]],[[2,0],[3,1]])),
        determinant([[5,2],[3,1]]),determinant([[7,4],[2,1]]),
    ])
    assign('matrix','precheck',[
        shape([[1,2,3],[4,5,6]]), sum(sum(row) for row in identity(3)),
        'Qo‘shish aniqlanmagan', '2×4', determinant([[6,0],[0,2]]),
    ])
    a,b = [[4,-1],[2,3]],[[1,2],[0,-2]]
    assign('matrix','postcheck',[
        shape([[1],[2],[3],[4]]),int([[1,0,0],[0,2,0],[0,0,1]]==identity(3)),
        matrix_text([[a[i][j]-b[i][j] for j in range(2)] for i in range(2)]),
        product([[2,-1]],[[3],[4]])[0][0],determinant([[3,2],[1,4]]),
    ])
    return values


def expected_examples():
    return {
        'logic-propositions': f'{int(8%2==0)} va {int(all(8%d for d in range(2,8)))}',
        'logic-basic-operations': str(int(not (False and True))),
        'logic-implication': f'{int(implies(True,False))} va {int(True==False)}',
        'logic-truth-tables': ','.join(str(int(implies(a,b))) for a,b in ROWS),
        'logic-laws': 'A∧¬B',
        'sets-membership': '∅, {p}, {q}, {p,q}',
        'sets-operations': f'{set_text({1,2,4}|{2,3})}; {set_text({1,2,4}&{2,3})}; {set_text({1,2,4}-{2,3})}',
        'sets-complement': set_text(set(range(1,7))-{1,3,5}),
        'sets-venn': f'|A|={4+3}; |A∪B|={4+3+2}',
        'sets-counting': str(30-(18+15-7)),
        'functions-domain': 'x≠−2',
        'sequences-arithmetic': f'a₄={5+3*3}; S₄={sum(5+3*i for i in range(4))}',
        'sequences-geometric': f'b₃={3*2**2}; S₃={sum(3*2**i for i in range(3))}',
        'counting-factorial': str(math.factorial(3)),
        'counting-selection': f'{math.comb(4,2)} va {math.perm(4,2)}',
        'matrices-shape': '2×3; A₂₃=8',
        'matrices-types': 'Diagonal, ammo birlik emas',
        'matrices-addition': matrix_text([[3,1],[3,4]]),
        'matrices-product': matrix_text(product([[1,3]],[[2],[4]])),
        'matrices-determinant': str(determinant([[2,3],[1,4]])),
    }


def verify(source_dir=None):
    # Historical stage-four oracle covers its original five modules only.
    # The later 1.4 bank has independent checks in test_number_theory.py.
    contents = [json.loads(path.read_text(encoding='utf-8')) for path in HERE.glob('*.v1.json')
                if path.name != 'number-theory-discrete-mathematics.v1.json']
    assert len(contents) == 5, 'Expected five course manifests'
    graph = {skill['key']: skill['prerequisite_keys'] for data in contents for skill in data['skills']}
    assert len(graph) == 25, 'Expected 25 unique skill keys'
    bank = {q['key']: (indicator,q) for indicator, rows in MCQ_QUESTIONS.items() for q in rows}
    new = [data for data in contents if data['module']['key'] != 'arithmetic-algebra']
    expected, examples = expected_answers(), expected_examples()
    checked, checked_examples = set(), set()
    for data in contents:
        validate_content(data, known_skills=graph, diagnostic_keys=bank.keys())
        filename = f'{data["module"]["key"]}.v1.json'
        assert data == json.loads((ROOT/'backend/apps/development/content/cluster1'/filename).read_text(encoding='utf-8')), filename
        for link in data['diagnostic_links']:
            assert bank[link['question_key']][0] in data['module']['indicator_keys'], link
            if bank[link['question_key']][0]=='iq':
                assert set(link['skill_keys']) <= {'sequences-arithmetic','sequences-geometric'}, link
        if source_dir:
            for source in data['sources']:
                digest=hashlib.sha256((Path(source_dir)/source['filename']).read_bytes()).hexdigest()
                assert digest.upper()==source['sha256'].upper(), source['filename']
        if data not in new:
            continue
        for q in data['exercises']:
            answer=expected[q['key']]
            if q['format']=='numeric':
                assert parse_numeric(q['answer_key']['value'])==answer, (q['key'],answer)
            else:
                choices=q['options']
                matching=[o for o in choices if normalized(o['text_uz'])==normalized(answer)]
                assert len(matching)==1 and matching[0]['id']==q['answer_key']['option_id'], (q['key'],answer)
                assert len({normalized(o['text_uz']) for o in choices})==len(choices), q['key']
            checked.add(q['key'])
        for lesson in data['lessons']:
            assert normalized(lesson['worked_example']['answer_uz'])==normalized(examples[lesson['skill_key']]), lesson['key']
            checked_examples.add(lesson['skill_key'])
    assert checked==expected.keys() and len(checked)==80
    assert checked_examples==examples.keys() and len(checked_examples)==20

    # Independently check every assignment and every distractor for Boolean laws.
    law_targets={
        'logic-practice-09':lambda a,b:not(a or b),
        'logic-practice-10':lambda a,b:a and(a or b),
        'logic-precheck-05':lambda a,b:not(not a),
        'logic-postcheck-05':lambda a,b:(a and b)or(a and not b),
    }
    logical={q['key']:q for d in new for q in d['exercises'] if d['module']['key']=='mathematical-logic'}
    for key,target in law_targets.items():
        q=logical[key]
        equivalent=[o for o in q['options'] if all(EXPRESSIONS[o['text_uz']](a,b)==target(a,b) for a,b in ROWS)]
        assert len(equivalent)==1 and equivalent[0]['id']==q['answer_key']['option_id'],key
    assert all((not(not a or b))==(a and not b) for a,b in ROWS), 'Worked De Morgan example'
    # The source powerset example and diagonal classification are also checked.
    assert len([combo for k in range(3) for combo in itertools.combinations('pq',k)])==4
    assert [[2,0],[0,5]]!=identity(2) and [[2,0],[0,3]]!=identity(2)
    old=subprocess.run([sys.executable,str(HERE/'validate_content.py')],capture_output=True,text=True,check=True)
    old_report=json.loads(old.stdout)
    assert not old_report['errors'] and old_report['independent_answer_checks']==20
    report={'modules':5,'skills':25,'lessons':25,'exercises':100,'new_answer_checks':len(checked),
            'existing_answer_checks':20,'new_worked_examples_checked':len(checked_examples),
            'boolean_laws_all_assignments':True,'prerequisite_graph_valid':True,
            'source_hashes_checked':bool(source_dir),
            'new_origin_counts':{kind:sum(q['source']['origin']==kind for d in new for q in d['exercises']) for kind in ('adapted','authored')},
            'diagnostic_question_references':sum(len(d['diagnostic_links']) for d in contents)}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir')
    verify(parser.parse_args().source_dir)
