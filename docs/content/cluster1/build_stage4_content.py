"""Reviewed Uzbek authoring source for the four stage-four manifests.

Run from any directory with Python. Writes reviewed and bundled draft copies.
Mathematical checks live separately in verify_stage4_content.py.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUNDLED = ROOT / 'backend/apps/development/content/cluster1'


class Course:
    def __init__(self, key, order, title, indicators, prefix, source_hash):
        self.prefix = prefix
        self.source = f'source-1-{order}'
        self.data = {
            'schema_version': 1,
            'sources': [{'id': self.source, 'filename': f'1.{order}-mavzu.docx', 'sha256': source_hash}],
            'module': {'key': key, 'version': 1, 'order': order, 'status': 'draft',
                       'review_status': 'internally_checked', 'title_uz': title, 'title_ru': None,
                       'content_language': 'uz', 'indicator_keys': indicators},
            'skills': [], 'lessons': [], 'exercises': [], 'diagnostic_links': [],
        }

    def lesson(self, key, title, parents, theory, prompt, solution, answer, indicators=None):
        self.data['skills'].append({'key': key, 'title_uz': title, 'indicator_keys': indicators or self.data['module']['indicator_keys'], 'prerequisite_keys': parents})
        self.data['lessons'].append({'key': f'{key}-lesson', 'skill_key': key, 'title_uz': title, 'theory_uz': theory,
                                    'worked_example': {'prompt_uz': prompt, 'solution_steps_uz': solution, 'answer_uz': answer}})

    def question(self, purpose, skill, prompt, answer, solution, hint, error, *, difficulty='easy', wrong=None, source=None):
        index = 1 + sum(q['purpose'] == purpose for q in self.data['exercises'])
        options = []
        if wrong is None:
            kind, key = 'numeric', {'value': str(answer)}
        else:
            choices = [(str(answer), 'To‘g‘ri. ' + solution[-1]), *wrong]
            shift = index % len(choices)
            choices = choices[shift:] + choices[:shift]
            for i, (value, feedback) in enumerate(choices):
                options.append({'id': chr(97+i), 'text_uz': value, 'feedback_uz': feedback})
            kind = 'single'
            key = {'option_id': next(o['id'] for o in options if o['text_uz'] == str(answer))}
        self.data['exercises'].append({
            'key': f'{self.prefix}-{purpose}-{index:02d}', 'skill_key': skill, 'purpose': purpose, 'format': kind,
            'difficulty': difficulty, 'prompt_uz': prompt, 'options': options, 'answer_key': key,
            'solution_steps_uz': solution, 'hint_uz': hint if purpose == 'practice' else None,
            'common_error_uz': error,
            'source': {'id': self.source, 'origin': 'adapted' if source else 'authored',
                       'locator': f'Amaliy topshiriqlar, {source}; tahrirlangan' if source else f'Yangi {purpose}: {skill}'},
        })

    def link(self, question, skills, reason):
        self.data['diagnostic_links'].append({'question_key': question, 'skill_keys': skills, 'rationale_uz': reason})

    def finish(self):
        skills = [s['key'] for s in self.data['skills']]
        items = self.data['exercises']
        by_skill = {key: [q['key'] for q in items if q['purpose'] == 'practice' and q['skill_key'] == key] for key in skills}
        self.data['blueprint'] = {
            'precheck_order': [q['key'] for q in items if q['purpose'] == 'precheck'],
            'practice_order': [by_skill[key][round_] for round_ in (0, 1) for key in skills],
            'postcheck_order': [q['key'] for q in items if q['purpose'] == 'postcheck'],
            'matched_pairs': [
                {'skill_key': key, 'difficulty': next(q['difficulty'] for q in items if q['purpose'] == 'precheck' and q['skill_key'] == key),
                 'precheck_key': next(q['key'] for q in items if q['purpose'] == 'precheck' and q['skill_key'] == key),
                 'postcheck_key': next(q['key'] for q in items if q['purpose'] == 'postcheck' and q['skill_key'] == key)} for key in skills],
            'unseen_postcheck_sets': 1,
            'comparison_note_uz': 'Qiyinlik tahririy baholangan; savollar statistik tenglashtirilmagan. Natija faqat ushbu mavzuga tegishli.',
            'exhaustion_note_uz': 'Yangi yakuniy to‘plam tugaganda mashqlar ochiq qoladi, ammo yangi mustaqil tekshiruv uchun bank kengaytirilishi kerak.',
        }
        return self.data


def logic():
    c = Course('mathematical-logic', 2, 'Matematik mantiq va mulohazalar algebrasi', ['logic'], 'logic',
               'A436D2015C4095685CA1AC4D4125DB4EC0DF9BC22D89B78004B3E4E3DE41601C')
    c.lesson('logic-propositions', 'Mulohaza va uning qiymati', [], [
        'Mulohaza — rost yoki yolg‘onligi aniq bo‘lgan darak gap. Rost qiymat 1 (True), yolg‘on qiymat 0 (False) bilan belgilanadi.',
        'Yolg‘on gap ham mulohazadir: “9 juft son” — aniq yolg‘on mulohaza. Gapning yolg‘onligi uni mulohaza bo‘lishdan chiqarmaydi.',
        'Savol va buyruq mulohaza emas. “Eshikni yoping!” buyrug‘iga rost yoki yolg‘on qiymat berilmaydi.',
        '“x > 4” yozuvida x berilmagan bo‘lsa, bu ochiq ifoda. x=6 kabi qiymat yoki aniq shart berilgach uning rostligi tekshiriladi.',
        '“Barcha A lar B” sharti har bir A elementning B ga ham tegishliligini bildiradi; undan barcha B lar A degan teskari xulosa kelib chiqmaydi.',
    ], '“8 soni 2 ga bo‘linadi” va “8 tub son” gaplarini tekshiring.',
       ['Ikkala gap ham aniq darak gap, shuning uchun mulohaza.', '8÷2=4, birinchi mulohaza rost.', '8 ning 1 va 8 dan tashqari 2 bo‘luvchisi bor; ikkinchisi yolg‘on.'], '1 va 0')
    c.lesson('logic-basic-operations', 'Inkor, AND va OR', ['logic-propositions'], [
        '¬A (NOT) A ning qiymatini teskarisiga o‘zgartiradi: ¬0=1, ¬1=0.',
        'A∧B (AND) faqat A va B ikkalasi ham rost bo‘lsa rost. Qolgan uch holatda natija 0.',
        'A∨B (OR) kamida bittasi rost bo‘lsa rost. Bu inklyuziv OR: ikkala mulohaza rost bo‘lganda ham natija 1.',
        'Murakkab ifodalarda qavsni saqlang. Dasturlashdagi and operatori kon’yunksiya, or diz’yunksiya, not inkorga mos.',
    ], 'A=0 va B=1 bo‘lsa, ¬(A∧B) ni toping.', ['A∧B=0∧1=0.', 'Natijani inkor qilamiz: ¬0=1.'], '1')
    c.lesson('logic-implication', 'Implikatsiya va ekvivalentlik', ['logic-propositions'], [
        'A→B — “Agar A, u holda B”. U faqat A=1 va B=0 holatida yolg‘on. A=0 bo‘lsa B ning ikkala qiymatida ham implikatsiya rost.',
        'A↔B ekvivalentlik bo‘lib, A va B bir xil qiymat olgandagina rost: 0↔0=1 va 1↔1=1.',
        'A→B formulasi ¬A∨B bilan teng kuchli. A→B dan B→A degan teskari implikatsiya kelib chiqmaydi.',
        'A→B va ¬B→¬A teng kuchli: bu kontrapozitsiya. Masalan, yomg‘ir bo‘lsa ko‘cha nam deyilsa, ko‘cha nam emasligidan yomg‘ir bo‘lmaganini chiqarish mumkin.',
        'A→B va B→C berilib, A rost bo‘lsa, avval B, keyin C rostligi kelib chiqadi.',
    ], 'A=1 va B=0 bo‘lganda A→B hamda A↔B ni hisoblang.',
       ['Rost shartdan yolg‘on oqibat chiqmoqda: A→B=0.', 'Qiymatlar turli, shuning uchun A↔B=0.'], '0 va 0')
    c.lesson('logic-truth-tables', 'Rostlik jadvali', ['logic-basic-operations', 'logic-implication'], [
        'n ta turli mulohaza o‘zgaruvchisi uchun rostlik jadvalida 2ⁿ ta qator bor. Bir xil o‘zgaruvchini takror yozish qatorlar sonini oshirmaydi.',
        'Ikki o‘zgaruvchi uchun standart tartib: (A,B)=(0,0),(0,1),(1,0),(1,1). Har bir topshiriqda qatorlar tartibi shu tarzda aniq beriladi.',
        'Har bir qator uchun avval qavs ichidagi va yordamchi ifodalar hisoblanadi. Keyin yakuniy ustun to‘ldiriladi.',
        'A∧B ning yakuniy ustuni 0,0,0,1; A∨B niki 0,1,1,1. Ustunda nechta rost qator borligi barcha qatorlarni sanash bilan topiladi.',
    ], '00,01,10,11 tartibida A→B ustunini tuzing.',
       ['00 da implikatsiya 1; 01 da ham 1.', '10 da rost shart yolg‘on oqibatga olib keladi: 0.', '11 da natija 1.'], '1,1,0,1')
    c.lesson('logic-laws', 'Mantiqiy qonunlar va soddalashtirish', ['logic-basic-operations'], [
        'Qo‘sh inkor: ¬¬A=A. Idempotentlik: A∧A=A va A∨A=A. O‘rin almashtirish va guruhlash AND hamda OR uchun ishlaydi.',
        'De Morgan: ¬(A∧B)=¬A∨¬B va ¬(A∨B)=¬A∧¬B. Inkor butun qavsga tegishli; AND va OR o‘rin almashadi.',
        'Yutilish: A∧(A∨B)=A va A∨(A∧B)=A.',
        'Taqsimot: A∧(B∨C)=(A∧B)∨(A∧C). A∨¬A=1, A∧¬A=0; A∧1=A va A∨0=A.',
        'Ikki formula teng kuchli bo‘lsa barcha kirish holatlarida bir xil natija beradi. Bitta misolda mos kelish yetarli emas.',
    ], '¬(¬A∨B) ni soddalashtiring.', ['De Morgan: ¬(¬A∨B)=¬¬A∧¬B.', 'Qo‘sh inkor: ¬¬A=A.'], 'A∧¬B')
    q=c.question
    q('practice','logic-propositions','Qaysi gap rost yoki yolg‘onligi aniq mulohaza?', '7 tub son.',
      ['“7 tub son” darak gap.', '7 faqat 1 va 7 ga bo‘linadi; gap rost mulohaza.'], 'Aniq rostlik qiymatiga ega darak gapni qidiring.',
      'Savol, buyruq va qiymati berilmagan ochiq ifoda mulohaza bilan bir xil emas.', wrong=[('Eshikni yoping!','Bu buyruq.'),('Soat nechchi?','Bu savol.'),('x > 3 (x berilmagan)','x noma’lum, ifoda ochiq.')])
    q('practice','logic-propositions','“9 juft son” gapining qiymatini yozing: rost=1, yolg‘on=0.',0,
      ['9 soni 2 ga qoldiqsiz bo‘linmaydi.', 'Shuning uchun gap yolg‘on: 0.'], '9 ni 2 ga bo‘lganda qoldiq bormi?',
      'Yolg‘on darak gap ham mulohaza bo‘la oladi.')
    q('practice','logic-basic-operations','A=1, B=0, C=1 bo‘lsa, (A∨B)∧¬C ni hisoblang. Rost=1, yolg‘on=0.',0,
      ['A∨B=1∨0=1.', '¬C=¬1=0.', '1∧0=0.'], 'OR va inkorni alohida hisoblang, so‘ng AND ni bajaring.',
      'AND uchun ikkala kirish ham rost bo‘lishi kerak.',source=1)
    q('practice','logic-basic-operations','Dasturlashdagi and operatoriga qaysi matematik mantiq amali mos?', 'Kon’yunksiya (∧)',
      ['and ikkala shartning birgalikda bajarilishini talab qiladi.', 'Bu kon’yunksiya (∧).'], 'Ikkala shart bir vaqtda rost bo‘lishini qaysi amal talab qiladi?',
      'OR kamida bitta rost shartni, NOT esa inkorni bildiradi.',source=8,wrong=[('Diz’yunksiya (∨)','Bu or operatoriga mos.'),('Inkor (¬)','Bu not operatoriga mos.'),('Implikatsiya (→)','Bu “agar…, u holda…” munosabati.')])
    q('practice','logic-implication','A→B qaysi holatda yolg‘on bo‘ladi?', 'A=1, B=0',
      ['Implikatsiya shart bajarilib, oqibat bajarilmaganda buziladi.', 'Yagona yolg‘on holat A=1, B=0.'], 'Rost va’da bajarilmagan holatni qidiring.',
      'A yolg‘on bo‘lsa, implikatsiya B ga qaramay rost.',source=3,wrong=[('A=0, B=0','Yolg‘on asosli implikatsiya rost.'),('A=0, B=1','Bu holatda ham implikatsiya rost.'),('A=1, B=1','Shart va oqibat mos, natija rost.')])
    q('practice','logic-implication','A=0 va B=0 bo‘lsa, A↔B qiymati nechaga teng? Rost=1, yolg‘on=0.',1,
      ['Ekvivalentlik qiymatlar tengligini tekshiradi.', '0 va 0 teng, natija 1.'], 'Ekvivalentlik uchun qiymatlarning tengligi muhim.',
      'Ekvivalentlikni AND bilan aralashtirmang.',source=7)
    q('practice','logic-truth-tables','¬(A∧¬B) uchun rostlik jadvali necha qatordan iborat?',4,
      ['Ifodada ikkita turli o‘zgaruvchi bor: A va B.', 'Qatorlar soni 2²=4.'], 'Inkorlar sonini emas, turli o‘zgaruvchilarni sanang.',
      'A yoki B ning takrorlanishi yangi o‘zgaruvchi yaratmaydi.',source=2,difficulty='medium')
    q('practice','logic-truth-tables','(A,B)=00,01,10,11 tartibida A∨B ustunini tanlang.', '0,1,1,1',
      ['00 da hech biri rost emas: 0.', 'Qolgan uch holatda kamida bittasi rost: 1,1,1.'], 'OR faqat ikkala qiymat 0 bo‘lsa 0 qaytaradi.',
      'Jadval qatorlari tartibini o‘zgartirmang.',difficulty='medium',wrong=[('0,0,0,1','Bu AND ustuni.'),('1,1,1,0','Bu AND ning inkoriga mos.'),('1,0,0,0','Bu OR ning inkoriga mos.')])
    q('practice','logic-laws','De Morgan qonuniga ko‘ra ¬(A∨B) qaysi ifodaga teng?', '¬A∧¬B',
      ['Butun OR ifodasi inkor qilinmoqda.', 'Har bir mulohaza inkor qilinib, OR o‘rniga AND olinadi: ¬A∧¬B.'], 'Qavs ichidagi OR inkor tashqariga chiqqanda AND ga aylanadi.',
      'Faqat harflarni inkor qilish yetmaydi: amal ham o‘zgaradi.',source=5,difficulty='medium',wrong=[('¬A∨¬B','Amal AND ga o‘zgarishi kerak.'),('A∧B','Ikkala mulohazaning inkori yo‘q.'),('A∨¬B','Butun qavsning inkori bitta hadga tegishli emas.')])
    q('practice','logic-laws','A∧(A∨B) ni soddalashtiring.', 'A',
      ['Yutilish qonuni A∧(A∨B)=A.', 'Natija B ga bog‘liq emas: A.'], 'Yutilish qonunini qo‘llang.',
      'Natijani B deb olish A ning majburiy shartligini yo‘qotadi.',source=6,difficulty='medium',wrong=[('B','A=1, B=0 holatida boshlang‘ich ifoda 1, B esa 0.'),('A∨B','A=0, B=1 da qiymatlar farq qiladi.'),('0','A=1 bo‘lsa natija 1 bo‘ladi.')])
    q('precheck','logic-propositions','“12 < 5” mulohazasining rostlik qiymatini yozing: rost=1, yolg‘on=0.',0,
      ['12 soni 5 dan katta.', '12 < 5 yolg‘on, qiymati 0.'],None,'Tengsizlik yo‘nalishini tekshiring.')
    q('precheck','logic-basic-operations','A=0, B=1 bo‘lsa, ¬A∧B qiymati nechaga teng? Rost=1, yolg‘on=0.',1,
      ['¬A=1.', '1∧1=1.'],None,'Avval A inkorini topish kerak.')
    q('precheck','logic-implication','A→B=0 ekani ma’lum. A va B ning qiymatlarini tanlang.', 'A=1, B=0',
      ['Implikatsiyaning yagona yolg‘on holati mavjud.', 'Bu A=1, B=0 holati.'],None,'Asos va oqibatning tartibi muhim.',wrong=[('A=0, B=1','Yolg‘on asosda implikatsiya rost.'),('A=1, B=1','Rost oqibatda implikatsiya rost.'),('A=0, B=0','Yolg‘on asosda implikatsiya rost.')])
    q('precheck','logic-truth-tables','A, B, C uchta turli mulohaza o‘zgaruvchisi uchun to‘liq rostlik jadvali necha qatordan iborat?',8,
      ['Har bir o‘zgaruvchi ikki qiymat oladi.', '2×2×2=8 qator.'],None,'O‘zgaruvchilar sonini 2 ga ko‘paytirish emas, 2 ni shu darajaga ko‘tarish kerak.',difficulty='medium')
    q('precheck','logic-laws','¬¬A ga barcha holatlarda teng bo‘lgan ifodani tanlang.', 'A',
      ['Birinchi inkor A ni teskarilaydi, ikkinchisi qaytaradi.', '¬¬A=A.'],None,'Ikki inkorni bitta inkor sifatida qabul qilmang.',difficulty='medium',wrong=[('¬A','Bu faqat bitta inkor.'),('0','A=1 da qo‘sh inkor 1.'),('1','A=0 da qo‘sh inkor 0.')])
    q('postcheck','logic-propositions','x ning qiymati berilmagan. “x > 4” yozuvi qanday tasniflanadi?', 'Ochiq ifoda; rostligi hali aniqlanmagan',
      ['Qiymat x ga bog‘liq: x=5 da rost, x=2 da yolg‘on.', 'Shartsiz bitta rostlik qiymati yo‘q, bu ochiq ifoda.'],None,'Noma’lum x ga o‘zboshimcha qiymat bermang.',wrong=[('Har doim rost mulohaza','x=2 qarshi misol bo‘ladi.'),('Har doim yolg‘on mulohaza','x=5 da ifoda rost bo‘ladi.'),('Buyruq','Bu harakatni bajarish talabi emas.')])
    q('postcheck','logic-basic-operations','A=1, B=0 bo‘lsa, (A∧B)∨¬A ni hisoblang. Rost=1, yolg‘on=0.',0,
      ['A∧B=0; ¬A=0.', '0∨0=0.'],None,'Yakuniy OR ga kirishdan oldin ikkala qismni hisoblang.')
    q('postcheck','logic-implication','A=0, B=0 bo‘lsa, A→B qiymatini yozing. Rost=1, yolg‘on=0.',1,
      ['A yolg‘on bo‘lsa, implikatsiya buzilmaydi.', 'A→B=1.'],None,'Implikatsiya faqat A=1 va B=0 da yolg‘on.')
    q('postcheck','logic-truth-tables','Ikki o‘zgaruvchining barcha 00,01,10,11 holatlarida A∧B nechta qatorda rost bo‘ladi?',1,
      ['00,01,10 holatlarida kamida bitta kirish 0.', 'Faqat 11 da AND rost: bitta qator.'],None,'Jami qatorlar bilan rost qatorlar sonini aralashtirmang.',difficulty='medium')
    q('postcheck','logic-laws','(A∧B)∨(A∧¬B) ni soddalashtiring.', 'A',
      ['A ni umumiy ko‘paytuvchi sifatida chiqaramiz: A∧(B∨¬B).', 'B∨¬B=1; A∧1=A.'],None,'B va uning inkorining OR qiymati doim 1.',difficulty='medium',wrong=[('B','A=1, B=0 da natija B ga teng emas.'),('¬A','A=1 da boshlang‘ich ifoda 1.'),('0','A=1 bo‘lsa formula rost.')])
    c.link('logic-contrapositive-1',['logic-implication'],'Yomg‘ir/nam ko‘cha shartidan kontrapozitsiya aniqlanadi; darsda bu qoida tushuntirilgan.')
    c.link('logic-extra-conditional-10',['logic-implication'],'A→B→C zanjirida A rostligidan C rostligi chiqariladi.')
    return c.finish()


def sets():
    c = Course('sets-and-relations', 3, 'To‘plamlar nazariyasi va Venn diagrammalari', ['math','logic'], 'sets',
               'CCC9CFB91A7C6A13CBA064F28B1FFF3D4D489E23F9DCD316330F216B85318EA7')
    c.lesson('sets-membership','Element va qism to‘plam',[],[
        'To‘plam elementlardan iborat. a∈A — a A ga tegishli, a∉A — tegishli emas. Elementning takror yozilishi yangi element yaratmaydi: {1,1,2}={1,2}.',
        'A⊆B barcha A elementlari B da ham borligini bildiradi; bunda A=B ham mumkin. Xos qism to‘plam uchun A⊊B yozuvi ishlatiladi.',
        '∅ bo‘sh to‘plam, unda element yo‘q. {∅} esa bitta element — bo‘sh to‘plamning o‘zidan iborat.',
        'n ta turli elementli to‘plamning 2ⁿ ta qism to‘plami bor; bunga ∅ va to‘plamning o‘zi ham kiradi.',
        '“Barcha itlar hayvon” kabi shart itlar to‘plami hayvonlar to‘plamining qism to‘plami ekanini bildiradi. Reks it bo‘lsa, hayvon ham bo‘ladi; teskari xulosa shart emas.',
    ],'A={p,q} ning barcha qism to‘plamlarini sanang.',
       ['Bo‘sh qism to‘plam: ∅.', 'Bitta elementlilar: {p}, {q}; ikkita elementli: {p,q}.', 'Jami 4=2² ta.'],'∅, {p}, {q}, {p,q}')
    c.lesson('sets-operations','Birlashish, kesishish va ayirma',['sets-membership'],[
        'A∪B — A yoki B ga kiruvchi barcha elementlar. Element bir marta yoziladi. A∪A=A.',
        'A∩B — ikkala to‘plamga kiruvchi umumiy elementlar. A∩A=A, A∩∅=∅.',
        'A∖B — A da bor, B da yo‘q elementlar. A∖B va B∖A odatda teng emas; amallar tartibi muhim.',
        'Dasturlashdagi set.intersection umumiy elementlarni, union birlashishni, difference ayirmani beradi. Bu yerda elementlarning tartibi emas, tegishliligi muhim.',
    ],'A={1,2,4}, B={2,3} uchun A∪B, A∩B va A∖B ni toping.',
       ['Barcha turli elementlar: {1,2,3,4}.','Umumiy element: {2}.','A dan B elementlarini olib tashlasak {1,4} qoladi.'],'{1,2,3,4}; {2}; {1,4}')
    c.lesson('sets-complement','Universal va to‘ldiruvchi to‘plam',['sets-membership'],[
        'Universal to‘plam U masalada qaralayotgan barcha elementlarni belgilaydi. A ning to‘ldiruvchisi A′=U∖A; U berilmasdan to‘ldiruvchi aniq emas.',
        'A′ da U ga kirib, A ga kirmaydigan elementlar bo‘ladi. U dan tashqaridagi elementlar olinmaydi.',
        'Bir xil U da (A′)′=A, A∪A′=U va A∩A′=∅.',
        'Masalan, U={a,b,c}, A={b} bo‘lsa A′={a,c}. Qayta to‘ldiruvchi olinsa {b} ga qaytiladi.',
    ],'U={1,2,3,4,5,6}, A={1,3,5} bo‘lsa A′ ni toping.',
       ['U ning har bir elementini tekshiramiz.','A dagi 1,3,5 chiqariladi; 2,4,6 qoladi.'],'{2,4,6}')
    c.lesson('sets-venn','Venn diagrammasidagi hududlar',['sets-operations','sets-complement'],[
        'Ikki doira uchun U to‘rtta ajralgan hududga bo‘linadi: faqat A, A∩B, faqat B va ikkala doiradan tashqari hudud.',
        'A ning elementlari soni faqat A va umumiy hudud sonlari yig‘indisi. B uchun ham xuddi shunday.',
        'A∪B faqat A, kesishma va faqat B hududlarini qamrab oladi. Umumiy hudud bir marta hisoblanadi.',
        'A ning B bilan umumiy bo‘lmagan soyali qismi A∖B dir. Diagrammani matndagi ajralgan hududlar soni bilan ham ifodalash mumkin.',
    ],'Faqat A hududida 4, kesishmada 3, faqat B da 2 element bor. |A| va |A∪B| ni toping.',
       ['A doirasi: 4+3=7.','Birlashish uch ichki hududdan iborat: 4+3+2=9.'],'|A|=7; |A∪B|=9')
    c.lesson('sets-counting','Elementlar soni va qo‘sh hisoblash',['sets-venn','arith-order'],[
        '|A| A dagi turli elementlar sonini bildiradi. Ikki to‘plamda |A∪B|=|A|+|B|−|A∩B|.',
        'Kesishmani ayirish sababi: u |A| va |B| da ikki marta sanalgan. Bir marta qoldirish uchun bir marta ayiriladi.',
        'Birortasiga kirmaydiganlar soni |U|−|A∪B|. Kesishma noma’lum bo‘lsa |A∩B|=|A|+|B|−|A∪B|.',
        'Sonlar shartga mos bo‘lishi kerak: kesishma ikkala to‘plamdan katta bo‘la olmaydi, birlashish esa U dan katta bo‘lmaydi.',
    ],'30 kishidan 18 tasi A, 15 tasi B guruhida; 7 tasi ikkalasida. Hech biriga kirmaydiganlar nechta?',
       ['Birlashish: 18+15−7=26.','Tashqarida: 30−26=4.'],'4')
    q=c.question
    q('practice','sets-membership','A={a,b} to‘plamning jami nechta qism to‘plami bor?',4,
      ['∅, {a}, {b}, {a,b} qism to‘plamlar mavjud.','Jami 2²=4 ta.'],'Bo‘sh to‘plam va A ning o‘zini ham hisobga oling.',
      'Qism to‘plamlar sonini elementlar soniga teng deb olmang.',source=7)
    q('practice','sets-membership','{1,1,2,3} to‘plamda nechta turli element bor?',3,
      ['Takroriy 1 yangi element emas.','Turli elementlar 1,2,3: jami 3 ta.'],'Bir xil elementlarni bir marta sanang.',
      'To‘plam ro‘yxat emas; takrorlar alohida sanalmaydi.')
    q('practice','sets-operations','A={1,2,3,4,5}, B={4,5,6,7} bo‘lsa A∪B ni tanlang.','{1,2,3,4,5,6,7}',
      ['Ikkala to‘plamdagi barcha turli elementlar olinadi.','Birlashish {1,2,3,4,5,6,7}.'],'Umumiy elementlarni takror yozmang.',
      'Birlashish faqat umumiy elementlardan iborat emas.',source=1,wrong=[('{4,5}','Bu kesishma.'),('{1,2,3}','Bu A∖B.'),('{6,7}','Bu B∖A.')])
    q('practice','sets-operations','A={1,2,3,4,5}, B={4,5,6,7} bo‘lsa A∖B ni tanlang.','{1,2,3}',
      ['A dan B da ham bor 4 va 5 ni chiqaramiz.','1,2,3 qoladi.'],'Avval A elementlarini yozing; ulardan B dagilarini o‘chiring.',
      'A∖B ni B∖A bilan almashtirmang.',source=3,wrong=[('{6,7}','Bu teskari ayirma.'),('{4,5}','Bu umumiy qism.'),('{1,2,3,6,7}','Bu ikkala to‘plamning umumiy bo‘lmagan qismlari yig‘indisi.')])
    q('practice','sets-complement','U={1,2,3,4,5,6,7,8,9,10}, A={2,4,6,8,10}. A′ ni tanlang.','{1,3,5,7,9}',
      ['Universal to‘plamdan barcha A elementlarini chiqaramiz.','U dagi toq sonlar qoladi: {1,3,5,7,9}.'],'U da bor, A da yo‘q elementlarni qidiring.',
      'To‘ldiruvchini cheksiz barcha toq sonlar deb olmang.',source=9,wrong=[('{2,4,6,8,10}','Bu A ning o‘zi.'),('∅','U da A dan tashqari elementlar ham bor.'),('{1,3,5,7,9,11}','11 universal to‘plamga kirmaydi.')])
    q('practice','sets-complement','U={a,b,c,d}, A={a,c} bo‘lsa A′ ni toping.','{b,d}',
      ['a va c ni U dan chiqaramiz.','b va d qoladi.'],'Faqat U ichidagi qolgan elementlarni oling.',
      'A ning elementlarini yana to‘ldiruvchiga qo‘shmang.',wrong=[('{a,c}','Bu A.'),('{a,b,c,d}','Bu U, A elementlari chiqarilmagan.'),('∅','b va d A ga kirmaydi.')])
    q('practice','sets-venn','Venn diagrammasida faqat A da 3, kesishmada 2, faqat B da 4 element bor. Birlashishda nechta element bor?',9,
      ['Uch ajralgan hudud qo‘shiladi.','3+2+4=9.'],'Kesishmani aynan bir marta sanang.',
      'A va B sonlarini alohida qo‘shib kesishmani ikki marta sanamang.',difficulty='medium')
    q('practice','sets-venn','A doirasining B bilan umumiy bo‘lmagan qismi bo‘yalgan. Qaysi amal tasvirlangan?','A∖B',
      ['Bo‘yalgan elementlar A ga kiradi, B ga kirmaydi.','Bu A∖B ta’rifi.'],'“A da bor, B da yo‘q” shartini amal bilan bog‘lang.',
      'Doiralar kesishgan qism bu yerda bo‘yalmagan.',difficulty='medium',wrong=[('A∩B','Bu ikkala to‘plamga ham kiradigan hudud.'),('A∪B','Bu ikkala doiraning to‘liq hududi.'),('B∖A','Bu B ning A dan tashqari qismi.')])
    q('practice','sets-counting','|A|=12, |B|=15, |A∩B|=4 bo‘lsa |A∪B| ni toping.',23,
      ['Birlashish uchun kesishma bir marta ayiriladi.','12+15−4=23.'],'|A∪B|=|A|+|B|−|A∩B| formulasini ishlating.',
      '27 deb olish umumiy to‘rt elementni ikki marta sanaydi.',source=5,difficulty='medium')
    q('practice','sets-counting','40 talabadan 25 tasi ingliz, 20 tasi nemis tilini, 8 tasi ikkala tilni biladi. Birorta tilni bilmaydiganlar nechta?',3,
      ['Kamida bitta tilni biladiganlar: 25+20−8=37.','Hech birini bilmaydiganlar: 40−37=3.'],'Avval kamida bitta tilni biladiganlarni toping.',
      'Kesishmani ayirmasdan 25+20 ni olish noto‘g‘ri.',source=10,difficulty='medium')
    q('precheck','sets-membership','A={2,4} bo‘lsa 4∈A mulohazasi qiymatini yozing: rost=1, yolg‘on=0.',1,
      ['4 A ichida sanab o‘tilgan.','Mulohaza rost: 1.'],None,'∈ belgisi elementning to‘plamga tegishliligini bildiradi.')
    q('precheck','sets-operations','A={1,3,5}, B={3,4,5}. A∩B ni toping.','{3,5}',
      ['Ikkala to‘plamga ham kiradigan elementlar 3 va 5.','A∩B={3,5}.'],None,'Umumiy bo‘lmagan elementlar kesishmaga kirmaydi.',wrong=[('{1,3,4,5}','Bu birlashish.'),('{1}','Bu A∖B.'),('{4}','Bu B∖A.')])
    q('precheck','sets-complement','U={1,2,3,4,5}, A={1,5}. A′ ni tanlang.','{2,3,4}',
      ['U dan 1 va 5 chiqariladi.','Qolganlari {2,3,4}.'],None,'A ni U dan ayirish kerak, teskarisi emas.',wrong=[('{1,5}','Bu A.'),('{2,3,4,6}','6 U ga tegishli emas.'),('∅','U bilan A teng emas.')])
    q('precheck','sets-venn','Faqat A hududida 5, kesishmada 2, faqat B da 1 element bor. |A| nechaga teng?',7,
      ['A o‘zining alohida hududi va kesishmani o‘z ichiga oladi.','5+2=7.'],None,'Faqat B hududini A ga qo‘shmang.',difficulty='medium')
    q('precheck','sets-counting','|A|=14, |B|=11 va |A∩B|=5. Birlashishdagi elementlar sonini toping.',20,
      ['Kesishma ikki marta sanalmasligi uchun ayiriladi.','14+11−5=20.'],None,'Birlashish formulasida kesishma qo‘shilmaydi.',difficulty='medium')
    q('postcheck','sets-membership','{∅} to‘plam nechta elementga ega?',1,
      ['Qavs ichida bitta obyekt — bo‘sh to‘plam bor.','Shuning uchun {∅} da bitta element mavjud.'],None,'∅ bilan {∅} bir xil emas.')
    q('postcheck','sets-operations','A={2,4,6}, B={1,2,3} bo‘lsa B∖A ni tanlang.','{1,3}',
      ['B dagi 2 A ga ham kiradi, shuning uchun chiqariladi.','1 va 3 qoladi.'],None,'Ayirma B dan boshlanayotganiga e’tibor bering.',wrong=[('{4,6}','Bu A∖B.'),('{2}','Bu kesishma.'),('{1,2,3,4,6}','Bu birlashish.')])
    q('postcheck','sets-complement','Bir xil U={a,b,c,d,e} da A={b,d,e}. (A′)′ ni toping.','{b,d,e}',
      ['A′={a,c}.','U dan a va c ni chiqarib, A ga qaytamiz: {b,d,e}.'],None,'To‘ldiruvchini ikki marta olish dastlabki to‘plamni qaytaradi.',wrong=[('{a,c}','Bu faqat bir marta olingan to‘ldiruvchi.'),('∅','Ikki to‘ldirish doim bo‘sh to‘plam bermaydi.'),('{a,b,c,d,e}','Bu universal to‘plam.')])
    q('postcheck','sets-venn','A doirasida jami 7 element bor, ulardan 3 tasi B ga ham kiradi. Faqat A hududida nechta element bor?',4,
      ['A ning jami sonidan umumiy hududni ayiramiz.','7−3=4.'],None,'Kesishma jami 7 soni ichida allaqachon hisoblangan.',difficulty='medium')
    q('postcheck','sets-counting','|A|=22, |B|=19, |A∪B|=34 bo‘lsa |A∩B| ni toping.',7,
      ['Formulani kesishma uchun yozamiz: |A∩B|=|A|+|B|−|A∪B|.','22+19−34=7.'],None,'Bu savolda noma’lum birlashish emas, kesishma.',difficulty='medium')
    for key,reason in [
        ('logic-extra-syllogism-1','Itlar hayvonlar qism to‘plami; Reksning tegishliligidan xulosa chiqariladi.'),
        ('logic-extra-syllogism-2','Maktab o‘quvchilari forma kiyuvchilar qism to‘plami sifatida qaraladi.'),
        ('logic-extra-syllogism-3','Atirgul, gul va suvga muhtoj obyektlar orasidagi qism to‘plam zanjiri qo‘llanadi.'),
    ]: c.link(key,['sets-membership'],reason)
    c.data['module']['diagnostic_coverage_note_uz']='Mavjud havolalar faqat qism to‘plam mulohazasiga tegishli. Venn hisoblari va to‘ldiruvchi bo‘yicha alohida diagnostika dalili yo‘q; precheck kerak.'
    return c.finish()


def sequences():
    c=Course('functions-sequences-combinatorics',5,'Funksiyalar, ketma-ketliklar va kombinatorika',['math','iq'],'seq',
             '06BC72C5FC8FD97D6BF2834F03E512D6E6B8052AFEEEFA314C67B11044B6BEED')
    c.lesson('functions-domain','Funksiya va aniqlanish sohasi',['arith-fractions','arith-substitution'],[
        'Funksiya har bir ruxsat etilgan x ga yagona f(x) qiymatni mos qo‘yadi. Aniqlanish sohasi — funksiyada ishlatish mumkin bo‘lgan barcha x lar to‘plami.',
        'Haqiqiy sonli ifodada maxraj nol bo‘la olmaydi. f(x)=1/(x−a) uchun x≠a. Bir nechta nol nuqta bo‘lsa barchasi chiqariladi.',
        'Kvadrat ildiz ostidagi ifoda manfiy bo‘lmasligi kerak: √(x−a) uchun x≥a.',
        'Qiymatlar to‘plami mumkin bo‘lgan natijalar, aniqlanish sohasi esa kirish qiymatlaridir; ular bir xil tushuncha emas.',
    ],'f(x)=1/(x+2) funksiyasining aniqlanish sohasini toping.',
       ['Maxraj x+2 nol bo‘lmasligi kerak.','x+2=0 dan x=−2.','Barcha haqiqiy sonlar olinadi, faqat −2 chiqariladi.'],'x≠−2',indicators=['math'])
    c.lesson('sequences-arithmetic','Arifmetik progressiya',['arith-substitution'],[
        'Arifmetik progressiyada ketma-ket hadlar orasidagi ayirma doimiy: d=a₂−a₁=a₃−a₂. d manfiy yoki nol ham bo‘lishi mumkin.',
        'n-had aₙ=a₁+(n−1)d. Birinchi haddan n-hadgacha n emas, n−1 qadam bor.',
        'Dastlabki n had yig‘indisi Sₙ=n(a₁+aₙ)/2. Barcha sonli topshiriqlarda n musbat butun son.',
        'Oldingi hadni topishda formula teskari ishlatiladi: a₁=aₙ−(n−1)d. Qatorga keyingi had qo‘shishda avval ayirma doimiyligini tekshiring.',
    ],'a₁=5, d=3 bo‘lsa a₄ va S₄ ni toping.',
       ['a₄=5+(4−1)×3=14.','S₄=4(5+14)/2=38.'],'a₄=14; S₄=38')
    c.lesson('sequences-geometric','Geometrik progressiya',['arith-order'],[
        'Geometrik progressiyada keyingi had oldingi hadni doimiy q ga ko‘paytirish orqali olinadi. Bu modulda b₁≠0 va q≠0.',
        'n-had bₙ=b₁qⁿ⁻¹. q kasr yoki manfiy ham bo‘lishi mumkin; masalan q=1/2 bo‘lsa hadlar ikki baravar kamayadi.',
        'Dastlabki n had yig‘indisi q≠1 uchun Sₙ=b₁(qⁿ−1)/(q−1). q=1 bo‘lsa Sₙ=nb₁.',
        'Ayirma doimiy bo‘lsa arifmetik, nisbat doimiy bo‘lsa geometrik progressiya. Faqat boshidagi ikki hadga qarab umumiy qonuniyatni tasdiqlamang.',
    ],'b₁=3, q=2 bo‘lsa b₃ va S₃ ni toping.',
       ['Hadlar 3,6,12; b₃=3×2²=12.','S₃=3+6+12=21.','Formula bilan: 3(2³−1)/(2−1)=21.'],'b₃=12; S₃=21')
    c.lesson('counting-factorial','Faktorial va o‘rin almashtirish',['arith-order'],[
        'Musbat butun n uchun n!=1×2×…×n. 0!=1 deb olinadi. Masalan 4!=24, 5!=120 va 6!=720.',
        'n ta turli elementning barchasini tartiblash soni Pₙ=n!. Birinchi o‘rin uchun n, keyingi uchun n−1 va shu tarzda oxirida bitta tanlov qoladi.',
        'Bu formula barcha elementlar turli bo‘lganda qo‘llanadi. Takrorlanuvchi harflar uchun shu formula to‘g‘ridan-to‘g‘ri qo‘llanmaydi.',
        'Faktoriallar tez o‘sadi; 6!−5! ifodasida ikkala faktorial alohida hisoblanadi yoki 5!(6−1) deb yoziladi.',
    ],'Uchta turli A,B,C harfini nechta tartibda joylashtirish mumkin?',
       ['Birinchi o‘ringa 3, ikkinchisiga 2, uchinchisiga 1 tanlov bor.','3×2×1=3!=6.'],'6',indicators=['math'])
    c.lesson('counting-selection','Joylashtirish va kombinatsiya',['counting-factorial'],[
        'n ta turli elementdan k tasini takrorsiz tanlashda tartib muhim bo‘lsa joylashtirish olinadi: Aₙᵏ=n!/(n−k)!.',
        'Tartib muhim bo‘lmasa kombinatsiya olinadi: Cₙᵏ=n!/[k!(n−k)!]. Bu modulda 0≤k≤n butun sonlar va takrorsiz tanlov qaraladi.',
        'Guruhga ikki delegat tanlashda Ali–Vali va Vali–Ali bir xil guruh. Rahbar va yordamchi tanlashda rollar turli, shuning uchun bu ikki tanlov boshqacha.',
        'Aₙᵏ=Cₙᵏ×k!: har bir tanlangan guruhni k! xil tartiblash mumkin. Avval topshiriqdagi tartib va takrorlanish shartini aniqlang.',
    ],'4 kishidan 2 delegat yoki rahbar va yordamchi tanlash sonlarini taqqoslang.',
       ['Delegatlar guruhi: C₄²=4×3/(2×1)=6.','Rollar turli bo‘lsa: A₄²=4×3=12.'],'6 va 12',indicators=['math'])
    q=c.question
    q('practice','functions-domain','Funksiyaning aniqlanish sohasi nimani bildiradi?','Ruxsat etilgan barcha x qiymatlari to‘plami',
      ['Aniqlanish sohasi kirish qiymatlariga tegishli.','Bu ruxsat etilgan barcha x qiymatlari to‘plami.'],'Kirish bilan natija qiymatlarini farqlang.',
      'Aniqlanish sohasini faqat natijalar to‘plami deb olmang.',source=8,difficulty='medium',wrong=[('Faqat f(x) natijalari to‘plami','Bu qiymatlar to‘plami.'),('Faqat x=0 nuqtasi','Ruxsat etilgan x lar odatda bir nuqta bilan cheklanmaydi.'),('Funksiya nomi','Nom x ga qo‘yilgan cheklovlarni bildirmaydi.')])
    q('practice','functions-domain','f(x)=1/(x−2) uchun qaysi cheklov to‘g‘ri?','x≠2',
      ['Maxraj x−2 nol bo‘lmasligi kerak.','x=2 chiqariladi, ya’ni x≠2.'],'Qaysi x da maxraj nol bo‘ladi?',
      'Maxraj nol bo‘ladigan qiymatni ruxsat etilgan yagona qiymat sifatida tanlamang.',difficulty='medium',wrong=[('x=2','Bu aynan taqiqlangan nuqta.'),('x≠−2','−2 da maxraj −4, nol emas.'),('Barcha haqiqiy x','x=2 da bo‘lish aniqlanmagan.')])
    q('practice','sequences-arithmetic','a₁=3, d=4 bo‘lsa arifmetik progressiyaning 10-hadini toping.',39,
      ['a₁₀=a₁+9d.','3+9×4=39.'],'Birinchi haddan o‘ninchi hadgacha to‘qqiz qadam bor.',
      '10d qo‘shish bir qadam ortiqcha hisoblaydi.',source=1)
    q('practice','sequences-arithmetic','Arifmetik progressiyada a₁=2, a₅=14. Dastlabki 5 had yig‘indisini toping.',40,
      ['S₅=5(a₁+a₅)/2.','5(2+14)/2=40.'],'Birinchi va oxirgi hadlarning o‘rtachasini hadlar soniga ko‘paytiring.',
      'Faqat a₅ ni topish emas, barcha besh hadni yig‘ish so‘ralgan.',source=3)
    q('practice','sequences-geometric','b₁=2, q=3 bo‘lsa geometrik progressiyaning 4-hadini toping.',54,
      ['b₄=b₁q³.','2×3³=2×27=54.'],'Daraja 4−1 ga teng.',
      'Nisbatni qo‘shish emas, ko‘paytirish kerak.',source=2)
    q('practice','sequences-geometric','b₁=5, q=2 bo‘lsa geometrik progressiyaning dastlabki 4 hadi yig‘indisini toping.',75,
      ['Hadlar 5,10,20,40.','5+10+20+40=75.'],'To‘rt hadni alohida yozib tekshiring.',
      '40 faqat to‘rtinchi had, yig‘indi emas.',source=9)
    q('practice','counting-factorial','5! qiymatini hisoblang.',120,
      ['5!=5×4×3×2×1.','Ko‘paytma 120.'],'5 dan 1 gacha butun sonlarni ko‘paytiring.',
      'Faktorial 5×5 yoki 1+2+3+4+5 emas.',source=4)
    q('practice','counting-factorial','To‘rtta turli elementning o‘rin almashtirishlari soni P₄ nechaga teng?',24,
      ['P₄=4!.','4×3×2×1=24.'],'Barcha to‘rtta element tartiblanmoqda.',
      '4² barcha elementlarning takrorsiz tartiblarini bermaydi.',source=5)
    q('practice','counting-selection','7 ta turli elementdan tartibi muhim bo‘lmagan 3 talik guruhlar sonini toping.',35,
      ['C₇³=7!/(3!4!)=7×6×5/(3×2×1).','210/6=35.'],'Bir xil uchlikning 3! ta tartibini bitta guruh deb oling.',
      '210 joylashtirishlarni sanaydi; guruhlarni emas.',source=6,difficulty='medium')
    q('practice','counting-selection','5 ta turli harfdan takrorsiz 3 harfli tartibli yozuvlar nechta tuziladi?',60,
      ['Birinchi o‘ringa 5, keyingisiga 4, uchinchisiga 3 tanlov.','A₅³=5×4×3=60.'],'Yozuvda harflar tartibi muhim.',
      '3! ga bo‘lish tartibni yo‘qotadi.',source=10,difficulty='medium')
    q('precheck','functions-domain','f(x)=√(x−1) haqiqiy qiymat olishi uchun qaysi shart kerak?','x≥1',
      ['Ildiz ostida x−1≥0 bo‘lishi kerak.','Shuning uchun x≥1.'],None,'Ildiz osti nol bo‘lishi mumkin; manfiy bo‘lishi mumkin emas.',difficulty='medium',wrong=[('x>1','x=1 ham ruxsat etilgan.'),('x≠1','Bu ildiz ostining manfiyligini to‘smaydi.'),('x≤1','x<1 da ildiz osti manfiy.')])
    q('precheck','sequences-arithmetic','4,7,10,… arifmetik progressiyaning navbatdagi hadini toping.',13,
      ['Ayirma 7−4=3 va 10−7=3.','Keyingi had 10+3=13.'],None,'Doimiy ayirmani qo‘llang.')
    q('precheck','sequences-geometric','3,6,12,… geometrik progressiyaning navbatdagi hadini toping.',24,
      ['Nisbat 6/3=2 va 12/6=2.','Keyingi had 12×2=24.'],None,'Oxirgi ayirmani davom ettirish o‘rniga doimiy nisbatni oling.')
    q('precheck','counting-factorial','3!+2! ifodaning qiymatini toping.',8,
      ['3!=6 va 2!=2.','6+2=8.'],None,'Faktoriallarni qo‘shishdan oldin ularning har birini hisoblang.')
    q('precheck','counting-selection','6 kishidan teng huquqli 2 delegatni nechta usulda tanlash mumkin?',15,
      ['Rollar teng, shuning uchun tartib muhim emas.','C₆²=6×5/2=15.'],None,'Bir juftlikni ikki tartibda sanamang.',difficulty='medium')
    q('postcheck','functions-domain','f(x)=1/(x²−9) uchun aniqlanish sohasidagi cheklovni tanlang.','x≠−3 va x≠3',
      ['x²−9=(x−3)(x+3).','Maxraj x=3 hamda x=−3 da nol; ikkala qiymat ham chiqariladi.'],None,'Kvadrat tenglamada manfiy ildizni unutmang.',difficulty='medium',wrong=[('Faqat x≠3','x=−3 da ham maxraj nol.'),('Faqat x≠−3','x=3 da ham maxraj nol.'),('Barcha haqiqiy x','Maxrajni nol qiladigan ikki nuqta mavjud.')])
    q('postcheck','sequences-arithmetic','Arifmetik progressiyada a₄=11 va d=3. a₁ ni toping.',2,
      ['a₄=a₁+3d.','a₁=11−3×3=2.'],None,'Oldingi hadni topish uchun ayirma teskari yo‘nalishda ayiriladi.')
    q('postcheck','sequences-geometric','Geometrik progressiyada b₁=4, q=1/2. b₃ ni toping.',1,
      ['Hadlar 4,2,1.','Formula bilan 4×(1/2)²=1.'],None,'q kasr bo‘lsa har qadamda qiymat kamayishi mumkin.')
    q('postcheck','counting-factorial','n musbat butun son va n!=720 bo‘lsa n ni toping.',6,
      ['5!=120.','6!=6×120=720; demak n=6.'],None,'720 ni javob qilib takrorlash emas, faktoriali 720 bo‘lgan n so‘ralgan.')
    q('postcheck','counting-selection','5 kishidan rahbar va undan boshqa yordamchini nechta usulda tanlash mumkin?',20,
      ['Rahbar uchun 5, qolgan yordamchi uchun 4 tanlov bor.','Rollar turli: 5×4=20.'],None,'Rahbar va yordamchi o‘rin almashtirsa boshqa natija hosil bo‘ladi.',difficulty='medium')
    for key in ('math-medium-1','math-medium-8','math-easy-12'):
        c.link(key,['counting-factorial'],'Faktorial yoki barcha turli elementlarning o‘rin almashtirishlari hisoblanadi.')
    c.link('math-medium-3',['counting-selection'],'Tartibsiz uchlik tanlash kombinatsiya formulasiga mos.')
    for key in ('iq-extra-series-1','iq-extra-series-2','iq-extra-series-3'):
        c.link(key,['sequences-arithmetic'],'Qatorda o‘zgarmas ayirma bor; faqat arifmetik ketma-ketlik ko‘nikmasiga dalil.')
    for key in ('iq-extra-series-11','iq-extra-series-12','iq-extra-series-13'):
        c.link(key,['sequences-geometric'],'Qatorda o‘zgarmas nisbat bor; umumiy IQga emas, geometrik ketma-ketlik ko‘nikmasiga tegishli.')
    c.data['module']['diagnostic_coverage_note_uz']='Funksiyaning aniqlanish sohasi bo‘yicha mos mavjud diagnostika savoli topilmadi; bu ko‘nikma precheck bilan tekshiriladi.'
    return c.finish()


def matrices():
    c=Course('matrices-linear-algebra',6,'Matritsalar va chiziqli algebra elementlari',['math'],'matrix',
             'EA2A27F86AC3F05C3D5FC350013A5513F3768A72ED421F41B74CB13C5D245269')
    c.lesson('matrices-shape','Qator, ustun va o‘lcham',['arith-order'],[
        'Matritsa sonlarning to‘g‘ri to‘rtburchak jadvali. m ta qator va n ta ustunli matritsaning o‘lchami m×n; jami mn ta element bor.',
        'Ushbu materialda [[a,b],[c,d]] yozuvida ichki qavslar qatorni bildiradi: birinchi qator a,b; ikkinchisi c,d.',
        'Element Aᵢⱼ da birinchi indeks qator, ikkinchisi ustun. Indekslar bu modulda 1 dan boshlanadi.',
        'Qator va ustun tartibini almashtirmang: 2×3 ikki qator, uch ustun; 3×2 esa uch qator, ikki ustun.',
    ],'A=[[1,4,7],[2,5,8]] matritsaning o‘lchami va A₂₃ ni toping.',
       ['Ikki ichki qator, har birida uch element bor: 2×3.','Ikkinchi qatorning uchinchi elementi 8.'],'2×3; A₂₃=8')
    c.lesson('matrices-types','Kvadrat, diagonal va birlik matritsa',['matrices-shape'],[
        'Qatorlar soni ustunlar soniga teng matritsa kvadrat deyiladi: m=n.',
        'Bosh diagonalda A₁₁,A₂₂,… elementlar turadi. Diagonal matritsada bosh diagonaldan tashqaridagi barcha elementlar 0.',
        'Birlik matritsada bosh diagonaldagi barcha elementlar 1, qolganlari 0. I yoki E bilan belgilanadi.',
        'Har bir birlik matritsa diagonal va kvadrat. Lekin har bir kvadrat yoki diagonal matritsa birlik emas. n×n birlik matritsada n ta 1 bor.',
    ],'[[2,0],[0,3]] matritsa birlikmi?',
       ['Matritsa kvadrat va diagonaldan tashqarida 0 lar bor.','Diagonal 2 va 3 dan iborat; birlik uchun ikkalasi ham 1 bo‘lishi kerak.'],'Diagonal, ammo birlik emas')
    c.lesson('matrices-addition','Qo‘shish, ayirish va songa ko‘paytirish',['matrices-shape'],[
        'Faqat bir xil o‘lchamli matritsalarni qo‘shish yoki ayirish mumkin. Mos qator va ustundagi elementlar ustida amal bajariladi.',
        'Qo‘shishda Cᵢⱼ=Aᵢⱼ+Bᵢⱼ; ayirishda Cᵢⱼ=Aᵢⱼ−Bᵢⱼ. Ayirish ishorasi B ning barcha elementlariga taalluqli.',
        'Matritsani k songa ko‘paytirishda har bir element k ga ko‘paytiriladi. Nol element 0 bo‘lib qoladi.',
        'Manfiy songa ko‘paytirganda ishoralar almashadi. Matritsaning o‘lchami bu amallarda saqlanadi.',
    ],'A=[[1,2],[3,0]], B=[[2,−1],[0,4]] uchun A+B ni toping.',
       ['Birinchi qator: 1+2=3 va 2+(−1)=1.','Ikkinchi qator: 3+0=3 va 0+4=4.'],'[[3,1],[3,4]]')
    c.lesson('matrices-product','Matritsalarni ko‘paytirish',['matrices-shape','arith-order'],[
        'A ning ustunlar soni B ning qatorlar soniga teng bo‘lsa AB aniqlangan. (m×n)(n×p) natija m×p o‘lchamli.',
        'Natijadagi Cᵢⱼ uchun A ning i-qatori bilan B ning j-ustunidagi mos elementlar ko‘paytiriladi va yig‘iladi.',
        '2×2 holatda C₁₁=A₁₁B₁₁+A₁₂B₂₁. Bu mos elementlarni shunchaki ko‘paytirish emas.',
        'AB va BA odatda teng emas; hatto ulardan biri aniqlanib, ikkinchisi aniqlanmasligi ham mumkin.',
    ],'[[1,3]] qator matritsani [[2],[4]] ustun matritsaga ko‘paytiring.',
       ['O‘lchamlar (1×2)(2×1) mos; natija 1×1.','Bitta element 1×2+3×4=14.'],'[[14]]')
    c.lesson('matrices-determinant','2×2 determinant',['matrices-shape','arith-order'],[
        'Determinant kvadrat matritsaga tegishli son. Bu modulda faqat 2×2 holat hisoblanadi.',
        'A=[[a,b],[c,d]] uchun det(A)=ad−bc: bosh diagonal ko‘paytmasidan ikkinchi diagonal ko‘paytmasi ayiriladi.',
        'Diagonal 2×2 matritsada b=c=0, shuning uchun determinant diagonal elementlar ko‘paytmasi ad ga teng.',
        'Determinant manfiy, nol yoki musbat bo‘lishi mumkin. Manfiy ishorani o‘zboshimcha olib tashlamang; ad+bc formulasi noto‘g‘ri.',
    ],'A=[[2,3],[1,4]] determinantini toping.',
       ['Bosh diagonal ko‘paytmasi 2×4=8.','Ikkinchi diagonal ko‘paytmasi 3×1=3.','det(A)=8−3=5.'],'5')
    q=c.question
    q('practice','matrices-shape','A=[[2,1],[4,3]] matritsaning o‘lchamini tanlang.','2×2',
      ['Ikki qator va har qatorda ikki ustun bor.','O‘lcham 2×2.'],'Avval ichki qatorlar, keyin har qatordagi elementlarni sanang.',
      'To‘rtta element borligi o‘lcham 4×1 degani emas.',source=1,wrong=[('1×4','Bu matritsa bitta qatordan iborat emas.'),('4×1','Bu matritsa to‘rtta qatordan iborat emas.'),('2×4','Har bir qatorda to‘rtta emas, ikkita element bor.')])
    q('practice','matrices-shape','3×2 o‘lchamli matritsada jami nechta element bor?',6,
      ['Har bir uch qatorda ikkitadan element bor.','3×2=6.'],'Qatorlar sonini ustunlar soniga ko‘paytiring.',
      'O‘lchamlar yig‘indisi jami elementlar sonini bermaydi.')
    q('practice','matrices-types','2×2 birlik matritsani tanlang.','[[1,0],[0,1]]',
      ['Birlik matritsaning bosh diagonalida 1 lar, boshqa joylarida 0 lar bo‘ladi.','Bu [[1,0],[0,1]] matritsa.'],'Ikkala diagonal element ham 1 bo‘lishi kerak.',
      'Barcha elementlari 1 bo‘lgan matritsa birlik emas.',source=6,wrong=[('[[1,1],[1,1]]','Diagonaldan tashqaridagi elementlar 0 bo‘lishi kerak.'),('[[0,1],[1,0]]','Bu yerda 1 lar ikkinchi diagonalda.'),('[[2,0],[0,2]]','Diagonalda 2 emas, 1 bo‘lishi kerak.')])
    q('practice','matrices-types','[[2,0],[0,5]] matritsa haqida qaysi xulosa to‘g‘ri?','Diagonal, ammo birlik emas',
      ['Diagonaldan tashqarida 0 lar bor.','Diagonal 2 va 5 dan iborat, shu sabab birlik emas.'],'Birlik uchun diagonal qiymatlarining o‘zini tekshiring.',
      'Diagonal bo‘lish birlik bo‘lish uchun yetarli emas.',wrong=[('Birlik matritsa','Diagonal elementlar 1 emas.'),('Kvadrat emas','O‘lchami 2×2, ya’ni kvadrat.'),('Nol matritsa','2 va 5 nol emas.')])
    q('practice','matrices-addition','[[1,−2],[3,4]] + [[2,5],[−1,0]] ni hisoblang.','[[3,3],[2,4]]',
      ['Birinchi qator: 1+2=3; −2+5=3.','Ikkinchi qator: 3+(−1)=2; 4+0=4.'],'Bir xil o‘rindagi elementlarni qo‘shing.',
      'Turli qator yoki ustunlarni almashtirmang.',source=3,wrong=[('[[3,7],[4,4]]','Manfiy elementlar ishorasi yo‘qolgan.'),('[[2,−10],[−3,0]]','Bu mos elementlarni ko‘paytirish natijasi, qo‘shish emas.'),('[[-1,−7],[4,4]]','Bu ayirish natijasi.')])
    q('practice','matrices-addition','−2 × [[3,0],[−1,4]] ni toping.','[[-6,0],[2,−8]]',
      ['−2×3=−6; −2×0=0.','−2×(−1)=2; −2×4=−8.'],'−2 ni har bir elementga ko‘paytiring.',
      'Ikki manfiy son ko‘paytmasi musbat bo‘ladi.',source=4,wrong=[('[[-6,0],[−2,−8]]','−2×(−1)=+2 bo‘lishi kerak.'),('[[−6,0],[−1,4]]','Ikkinchi qator ham ko‘paytirilishi kerak.'),('[[6,0],[−2,8]]','−2 ning manfiy ishorasi hisobga olinmagan.')])
    q('practice','matrices-product','AB aniqlanishi uchun qaysi shart kerak?','A ustunlari soni B qatorlari soniga teng',
      ['Har bir qator–ustun ko‘paytmasida hadlar soni teng bo‘lishi kerak.','Shuning uchun A ustunlari soni B qatorlari soniga teng.'],'(m×n)(n×p) yozuvidagi ichki sonlarga qarang.',
      'Ko‘paytirish shartini qo‘shishdagi bir xil o‘lcham sharti bilan aralashtirmang.',source=7,difficulty='medium',wrong=[('A qatorlari soni B ustunlari soniga teng','Bu AB uchun kerakli ichki o‘lcham sharti emas.'),('Ikkalasi albatta kvadrat','To‘g‘ri to‘rtburchak matritsalar ham ko‘paytiriladi.'),('Ikkalasi albatta bir xil o‘lchamli','2×3 va 3×4 turli o‘lchamda, lekin ko‘paytma aniqlangan.')])
    q('practice','matrices-product','A=[[1,2],[0,1]], B=[[2,0],[3,1]]. AB ni toping.','[[8,2],[3,1]]',
      ['C₁₁=1×2+2×3=8; C₁₂=1×0+2×1=2.','C₂₁=0×2+1×3=3; C₂₂=0×0+1×1=1.'],'Har bir element uchun A qatori va B ustunining ko‘paytmalari yig‘iladi.',
      'Mos elementlarni alohida ko‘paytirish matritsa ko‘paytmasi emas.',difficulty='medium',wrong=[('[[2,0],[0,1]]','Bu mos elementlarni ko‘paytirish.'),('[[2,4],[3,7]]','Bu BA ko‘paytmasi, AB emas.'),('[[3,2],[3,2]]','Bu A+B natijasi.')])
    q('practice','matrices-determinant','[[5,2],[3,1]] determinantini toping.',-1,
      ['ad=5×1=5; bc=2×3=6.','5−6=−1.'],'Bosh diagonal ko‘paytmasidan ikkinchisini ayiring.',
      '5+6 emas, 5−6 hisoblanadi.',source=2,difficulty='medium')
    q('practice','matrices-determinant','[[7,4],[2,1]] determinantini hisoblang.',-1,
      ['ad=7×1=7; bc=4×2=8.','7−8=−1.'],'Manfiy natija ham mumkin.',
      'Determinantning modulini olish talab qilinmagan.',source=5,difficulty='medium')
    q('precheck','matrices-shape','[[1,2,3],[4,5,6]] matritsaning o‘lchamini tanlang.','2×3',
      ['Ikki qator bor, har biri uch elementli.','O‘lcham 2×3.'],None,'Qatorlar soni birinchi yoziladi.',wrong=[('3×2','Qator va ustunlar almashgan.'),('1×6','Bu bitta qatorli matritsa emas.'),('6×1','Bu oltita qatorli matritsa emas.')])
    q('precheck','matrices-types','3×3 birlik matritsada nechta 1 elementi bor?',3,
      ['Faqat bosh diagonaldagi uchta element 1.','Qolgan oltita element 0.'],None,'Barcha 9 element 1 emas.')
    q('precheck','matrices-addition','A o‘lchami 2×2, B o‘lchami 2×3. A+B haqida to‘g‘ri xulosani tanlang.','Qo‘shish aniqlanmagan',
      ['Qo‘shish uchun qatorlar ham, ustunlar ham mos bo‘lishi kerak.','Ustunlar soni turli, qo‘shish aniqlanmagan.'],None,'Faqat qatorlarning tengligi yetarli emas.',wrong=[('Natija 2×3','Mos elementlar yetishmaydi.'),('Natija 2×2','B ning uchinchi ustunini tashlab yuborish mumkin emas.'),('Natija 4×5','O‘lchamlar bir-biriga qo‘shilmaydi.')])
    q('precheck','matrices-product','A o‘lchami 2×3, B o‘lchami 3×4. AB ning o‘lchami qanday?','2×4',
      ['Ichki o‘lchamlar 3 va 3 teng.','Natija tashqi o‘lchamlar bo‘yicha 2×4.'],None,'Natijada ichki 3 emas, tashqi o‘lchamlar qoladi.',difficulty='medium',wrong=[('3×3','Bu ichki o‘lchamlarni natija deb olish.'),('4×2','Tashqi o‘lchamlar tartibi almashgan.'),('2×3','Natija A ning o‘lchami bilan bir xil bo‘lishi shart emas.')])
    q('precheck','matrices-determinant','[[6,0],[0,2]] diagonal matritsaning determinantini toping.',12,
      ['ad=6×2=12; bc=0×0=0.','12−0=12.'],None,'Diagonal elementlar yig‘indisi emas, ko‘paytmasi olinadi.',difficulty='medium')
    q('postcheck','matrices-shape','[[1],[2],[3],[4]] yozuvida har bir ichki qavs bitta qator. Matritsaning o‘lchamini tanlang.','4×1',
      ['To‘rtta qator bor, har birida bitta element.','O‘lcham 4×1.'],None,'Bitta ustun bo‘lish bitta qator bo‘lish degani emas.',wrong=[('1×4','Bu qator matritsaning o‘lchami bo‘lardi.'),('2×2','Berilgan qatorlar qayta joylashtirilmaydi.'),('4×4','Har bir qatorda to‘rtta emas, bitta element bor.')])
    q('postcheck','matrices-types','[[1,0,0],[0,2,0],[0,0,1]] birlik matritsami? Ha=1, yo‘q=0 deb yozing.',0,
      ['O‘rtadagi diagonal element 2.', 'Birlik matritsaning barcha diagonal elementlari 1 bo‘lishi kerak; javob 0.'],None,'Diagonal bo‘lishning o‘zi birlik bo‘lishni bildirmaydi.')
    q('postcheck','matrices-addition','[[4,−1],[2,3]] − [[1,2],[0,−2]] ni hisoblang.','[[3,−3],[2,5]]',
      ['Birinchi qator: 4−1=3, −1−2=−3.','Ikkinchi qator: 2−0=2, 3−(−2)=5.'],None,'Manfiy sonni ayirish qo‘shishga aylanadi.',wrong=[('[[3,1],[2,1]]','Manfiy elementlar bilan ayirish ishoralari noto‘g‘ri qo‘llangan.'),('[[5,1],[2,1]]','Bu qo‘shish natijasi.'),('[[3,−3],[2,1]]','Oxirgi element 3−(−2)=5 bo‘lishi kerak.')])
    q('postcheck','matrices-product','[[2,−1]] × [[3],[4]] ko‘paytmadagi yagona elementni toping.',2,
      ['Qator–ustun qoidasiga ko‘ra 2×3+(−1)×4.','6−4=2.'],None,'Mos ko‘paytmalar qo‘shiladi; ularning o‘zini ko‘paytirmang.',difficulty='medium')
    q('postcheck','matrices-determinant','[[3,2],[1,4]] determinantini toping.',10,
      ['ad=3×4=12; bc=2×1=2.','12−2=10.'],None,'Ikkinchi diagonal ko‘paytmasini ayirishni unutmang.',difficulty='medium')
    c.data['module']['diagnostic_coverage_note_uz']='Mavjud diagnostika bankida matritsa o‘lchami, amallari yoki determinantga bevosita mos savol yo‘q. Sun’iy havola yaratilmagan; modul precheck orqali baholanadi.'
    return c.finish()


def build():
    for data in (logic(), sets(), sequences(), matrices()):
        filename=f'{data["module"]["key"]}.v1.json'
        content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
        for directory in (HERE,BUNDLED):
            directory.mkdir(parents=True,exist_ok=True)
            (directory/filename).write_text(content,encoding='utf-8')
        print(f'{filename}: {len(data["lessons"])} lessons, {len(data["exercises"])} exercises (draft)')


if __name__=='__main__':
    build()
