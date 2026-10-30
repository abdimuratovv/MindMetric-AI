import hashlib
import json
import math
from pathlib import Path

from django.test import SimpleTestCase
from apps.development.content_loader import BUNDLED_CONTENT, bundled_contents
from apps.development.validation import validate_content


class NumberTheoryContentTests(SimpleTestCase):
    def setUp(self):
        self.data=next(d for d in bundled_contents() if d['module']['key']=='number-theory-discrete-mathematics')

    def test_contract_parity_and_real_authored_source(self):
        contents=bundled_contents()
        graph={s['key']:s['prerequisite_keys'] for d in contents for s in d['skills']}
        validate_content(self.data,known_skills=graph)
        self.assertEqual(self.data['module']['order'],4)
        self.assertEqual(self.data['diagnostic_links'],[])
        directory=Path(__file__).resolve().parents[4]/'docs/content/cluster1'
        self.assertEqual(self.data,json.loads((directory/'number-theory-discrete-mathematics.v1.json').read_text(encoding='utf-8')))
        source=self.data['sources'][0]
        self.assertEqual(hashlib.sha256((directory/source['filename']).read_bytes()).hexdigest().upper(),source['sha256'])

    def test_twenty_answers_against_independent_integer_oracles(self):
        def prime(n):return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
        expected={
            'practice':[73//9,104%9,next(n for n in (25,27,29,33) if prime(n)),
                        '2² × 3 × 7',math.gcd(48,18),math.gcd(45,60),math.lcm(8,12),
                        math.lcm(9,15),int('110101',2),format(58,'o')+'₈'],
            'precheck':[85//7,next(n for n in (1,39,43,49) if prime(n)),math.gcd(84,126),math.lcm(12,18),int('101101',2)],
            'postcheck':[7*9+4,sum(prime(n) for n in range(21,30)),math.gcd(48,180),math.lcm(8,14),format(202,'X')+'₁₆'],
        }
        self.assertEqual(2**2*3*7,84)
        for purpose,answers in expected.items():
            rows=[q for q in self.data['exercises'] if q['purpose']==purpose]
            self.assertEqual(len(rows),len(answers))
            for row,answer in zip(rows,answers):
                with self.subTest(key=row['key']):
                    actual=row['answer_key'].get('value')
                    if row['format']=='single':
                        actual=next(o['text_uz'] for o in row['options'] if o['id']==row['answer_key']['option_id'])
                    self.assertEqual(actual,str(answer))

    def test_worked_examples_and_conversion_boundaries(self):
        answers=[row['worked_example']['answer_uz'] for row in self.data['lessons']]
        self.assertEqual(divmod(59,8),(7,3))
        self.assertEqual(answers[0],'59 div 8 = 7; 59 mod 8 = 3')
        self.assertTrue(all(97%d for d in range(2,math.isqrt(97)+1)))
        self.assertEqual(answers[1],'97 tub son')
        self.assertEqual(answers[2],str(math.gcd(252,105)))
        self.assertEqual(answers[3],f'{math.lcm(6,15)} daqiqadan keyin')
        self.assertEqual(int('2A',16),int('101010',2))
        self.assertEqual(int('52',8),42)
        self.assertEqual(answers[4],'2A₁₆ = 42₁₀ = 101010₂ = 52₈')
        with self.assertRaises(ValueError):int('58',8)
