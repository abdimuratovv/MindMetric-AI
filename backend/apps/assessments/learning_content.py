"""
Seed content for the learning_speed indicator (LearningModule/LearningItem).

Each module teaches an invented mini-system the student cannot know in advance,
then tests it in three blocks of three items, each block harder than the last.
Two modules per family, so a retake gets the other variant of each family.

`options` is used when the answer choices are language-neutral (numbers, invented
words); otherwise `options_ru`/`options_uz` carry the translated choices in the
same order. Item keys are derived as <module key>-b<block>-<n> by the seed command.
"""

_SYM_PROMPT = {'ru': 'Чему равен результат?', 'uz': 'Natija nechaga teng?'}
_X_PROMPT = {'ru': 'Чему равен x после выполнения программы?', 'uz': 'Dastur bajarilgandan keyin x nechaga teng?'}
_A_PROMPT = {'ru': 'Чему равно a после выполнения программы?', 'uz': 'Dastur bajarilgandan keyin a nechaga teng?'}


def _item(block, prompt, correct_index, explanation, *, code='', options=None, options_ru=None, options_uz=None):
    return {
        'block': block,
        'prompt_ru': prompt['ru'], 'prompt_uz': prompt['uz'],
        'code': code,
        'options_ru': options_ru if options_ru is not None else options,
        'options_uz': options_uz if options_uz is not None else options,
        'correct_index': correct_index,
        'explanation_ru': explanation['ru'], 'explanation_uz': explanation['uz'],
    }


def _same(text):
    return {'ru': text, 'uz': text}


LEARNING_MODULES = [
    # -- Symbols ----------------------------------------------------------------------
    {
        'key': 'symbols-a', 'family': 'symbols',
        'title_ru': 'Язык символов: ▲ ● ■', 'title_uz': 'Belgilar tili: ▲ ● ■',
        'rules_ru': [
            '▲ — умножает число на 2',
            '● — прибавляет к числу 3',
            '■ — вычитает из числа 1',
            'Символы пишутся после числа и выполняются по очереди слева направо: 2 ● ▲ → (2 + 3) × 2 = 10',
        ],
        'rules_uz': [
            "▲ — sonni 2 ga ko'paytiradi",
            "● — songa 3 qo'shadi",
            '■ — sondan 1 ayiradi',
            "Belgilar sondan keyin yoziladi va chapdan o'ngga navbat bilan bajariladi: 2 ● ▲ → (2 + 3) × 2 = 10",
        ],
        'items': [
            _item(1, _SYM_PROMPT, 2, _same('4 × 2 = 8'), code='4 ▲', options=['6', '16', '8', '2']),
            _item(1, _SYM_PROMPT, 0, _same('5 + 3 = 8'), code='5 ●', options=['8', '15', '2', '53']),
            _item(1, _SYM_PROMPT, 1, _same('6 − 1 = 5'), code='6 ■', options=['7', '5', '4', '6']),

            _item(2, _SYM_PROMPT, 2, _same('5 + 3 = 8, 8 × 2 = 16'), code='5 ● ▲', options=['13', '11', '16', '26']),
            _item(2, _SYM_PROMPT, 1, _same('3 × 2 = 6, 6 − 1 = 5'), code='3 ▲ ■', options=['4', '5', '6', '7']),
            _item(2, _SYM_PROMPT, 0, _same('7 − 1 = 6, 6 + 3 = 9'), code='7 ■ ●', options=['9', '10', '8', '11']),

            _item(3, _SYM_PROMPT, 2, _same('2 × 2 = 4, 4 + 3 = 7, 7 − 1 = 6, 6 × 2 = 12'),
                  code='2 ▲ ● ■ ▲', options=['10', '14', '12', '13']),
            _item(3, {'ru': 'Какое число нужно поставить вместо ?, чтобы получить 13?',
                      'uz': "? o'rniga qaysi son qo'yilsa, natija 13 bo'ladi?"},
                  1, _same('5 × 2 = 10, 10 + 3 = 13'), code='? ▲ ● = 13', options=['4', '5', '6', '8']),
            _item(3, _SYM_PROMPT, 0, _same('4 + 3 = 7, 7 − 1 = 6, 6 × 2 = 12, 12 × 2 = 24'),
                  code='4 ● ■ ▲ ▲', options=['24', '20', '26', '28']),
        ],
    },
    {
        'key': 'symbols-b', 'family': 'symbols',
        'title_ru': 'Язык символов: ◆ ★ ▼', 'title_uz': 'Belgilar tili: ◆ ★ ▼',
        'rules_ru': [
            '◆ — прибавляет к числу 2',
            '★ — умножает число на 3',
            '▼ — делит число на 2',
            'Символы пишутся перед числом. Первым выполняется символ, ближайший к числу, то есть справа налево: '
            '◆ ★ 1 → ★ 1 = 3, затем ◆ 3 = 5',
        ],
        'rules_uz': [
            "◆ — songa 2 qo'shadi",
            "★ — sonni 3 ga ko'paytiradi",
            "▼ — sonni 2 ga bo'ladi",
            "Belgilar sondan oldin yoziladi. Songa eng yaqin belgi birinchi bajariladi, ya'ni o'ngdan chapga: "
            '◆ ★ 1 → ★ 1 = 3, keyin ◆ 3 = 5',
        ],
        'items': [
            _item(1, _SYM_PROMPT, 0, _same('5 + 2 = 7'), code='◆ 5', options=['7', '10', '3', '25']),
            _item(1, _SYM_PROMPT, 1, _same('4 × 3 = 12'), code='★ 4', options=['7', '12', '43', '16']),
            _item(1, _SYM_PROMPT, 2, _same('10 : 2 = 5'), code='▼ 10', options=['20', '8', '5', '12']),

            _item(2, _SYM_PROMPT, 3, _same('★ 4 = 12, ◆ 12 = 14'), code='◆ ★ 4', options=['18', '12', '10', '14']),
            _item(2, _SYM_PROMPT, 0, _same('◆ 4 = 6, ★ 6 = 18'), code='★ ◆ 4', options=['18', '14', '12', '20']),
            _item(2, _SYM_PROMPT, 1, _same('◆ 6 = 8, ▼ 8 = 4'), code='▼ ◆ 6', options=['5', '4', '3', '8']),

            _item(3, _SYM_PROMPT, 2, _same('★ 6 = 18, ▼ 18 = 9, ◆ 9 = 11'), code='◆ ▼ ★ 6', options=['12', '9', '11', '10']),
            _item(3, _SYM_PROMPT, 1, _same('◆ 2 = 4, ★ 4 = 12, ▼ 12 = 6'), code='▼ ★ ◆ 2', options=['7', '6', '5', '12']),
            _item(3, {'ru': 'Какое число нужно поставить вместо ?, чтобы получить 21?',
                      'uz': "? o'rniga qaysi son qo'yilsa, natija 21 bo'ladi?"},
                  2, _same('◆ 5 = 7, ★ 7 = 21'), code='★ ◆ ? = 21', options=['7', '19', '5', '6']),
        ],
    },

    # -- Pseudocode -------------------------------------------------------------------
    {
        'key': 'pseudocode-a', 'family': 'pseudocode',
        'title_ru': 'Язык MINI: NUR, KAS, ZUR, TAK', 'title_uz': 'MINI tili: NUR, KAS, ZUR, TAK',
        'rules_ru': [
            'NUR x 5 — записывает в x значение 5',
            'KAS x 3 — прибавляет к x число 3',
            'ZUR x 2 — умножает x на 2',
            'TAK 3 { … } — повторяет команды в скобках 3 раза',
            'Команды выполняются сверху вниз',
        ],
        'rules_uz': [
            'NUR x 5 — x ga 5 qiymatini yozadi',
            "KAS x 3 — x ga 3 qo'shadi",
            "ZUR x 2 — x ni 2 ga ko'paytiradi",
            'TAK 3 { … } — qavs ichidagi buyruqlarni 3 marta takrorlaydi',
            'Buyruqlar yuqoridan pastga bajariladi',
        ],
        'items': [
            _item(1, _X_PROMPT, 1, {'ru': 'x = 2, затем 2 + 4 = 6', 'uz': 'x = 2, keyin 2 + 4 = 6'},
                  code='NUR x 2\nKAS x 4', options=['8', '6', '4', '24']),
            _item(1, _X_PROMPT, 0, _same('x = 3, 3 × 4 = 12'), code='NUR x 3\nZUR x 4', options=['12', '7', '34', '81']),
            _item(1, _X_PROMPT, 2, _same('5 + 1 = 6, 6 × 2 = 12'),
                  code='NUR x 5\nKAS x 1\nZUR x 2', options=['11', '7', '12', '10']),

            _item(2, _X_PROMPT, 1, _same('1 + 2 + 2 + 2 = 7'), code='NUR x 1\nTAK 3 { KAS x 2 }', options=['3', '7', '6', '9']),
            _item(2, _X_PROMPT, 3, _same('1 × 2 × 2 × 2 = 8'), code='NUR x 1\nTAK 3 { ZUR x 2 }', options=['6', '7', '9', '8']),
            _item(2, _X_PROMPT, 0, _same('0 + 3 + 3 + 3 + 3 = 12'), code='NUR x 0\nTAK 4 { KAS x 3 }', options=['12', '3', '7', '15']),

            _item(3, _X_PROMPT, 1, {
                'ru': 'Внутренний TAK каждый раз прибавляет 3, внешний выполняет его 2 раза: 2 × 3 = 6',
                'uz': "Ichki TAK har safar 3 qo'shadi, tashqi TAK uni 2 marta bajaradi: 2 × 3 = 6",
            }, code='NUR x 0\nTAK 2 {\n  TAK 3 { KAS x 1 }\n}', options=['5', '6', '8', '9']),
            _item(3, _X_PROMPT, 2, {
                'ru': '1-й раз: (1 + 1) × 2 = 4; 2-й раз: (4 + 1) × 2 = 10',
                'uz': '1-marta: (1 + 1) × 2 = 4; 2-marta: (4 + 1) × 2 = 10',
            }, code='NUR x 1\nTAK 2 {\n  KAS x 1\n  ZUR x 2\n}', options=['8', '12', '10', '6']),
            _item(3, _X_PROMPT, 3, {
                'ru': '2 × 2 × 2 × 2 = 16, затем KAS вне цикла: 16 + 1 = 17',
                'uz': "2 × 2 × 2 × 2 = 16, keyin sikldan tashqaridagi KAS: 16 + 1 = 17",
            }, code='NUR x 2\nTAK 3 { ZUR x 2 }\nKAS x 1', options=['18', '9', '16', '17']),
        ],
    },
    {
        'key': 'pseudocode-b', 'family': 'pseudocode',
        'title_ru': 'Язык MINI: NUR, KAS, VEX, QUR, TAK', 'title_uz': 'MINI tili: NUR, KAS, VEX, QUR, TAK',
        'rules_ru': [
            'NUR a 3 — записывает в a значение 3',
            'KAS a b — прибавляет к a значение b (вместо b может стоять число)',
            'VEX a b — меняет местами значения a и b',
            'QUR a > 5 { … } — выполняет команды в скобках, только если условие верно',
            'TAK 3 { … } — повторяет команды в скобках 3 раза',
        ],
        'rules_uz': [
            'NUR a 3 — a ga 3 qiymatini yozadi',
            "KAS a b — a ga b ning qiymatini qo'shadi (b o'rnida son ham bo'lishi mumkin)",
            "VEX a b — a va b qiymatlarini o'rin almashtiradi",
            "QUR a > 5 { … } — shart to'g'ri bo'lsagina qavs ichidagi buyruqlarni bajaradi",
            'TAK 3 { … } — qavs ichidagi buyruqlarni 3 marta takrorlaydi',
        ],
        'items': [
            _item(1, _A_PROMPT, 2, {'ru': 'VEX меняет значения местами: a = 7, b = 4', 'uz': 'VEX qiymatlarni almashtiradi: a = 7, b = 4'},
                  code='NUR a 4\nNUR b 7\nVEX a b', options=['4', '11', '7', '3']),
            _item(1, _A_PROMPT, 0, _same('a = 2 + 5 = 7'), code='NUR a 2\nNUR b 5\nKAS a b', options=['7', '5', '2', '10']),
            _item(1, _A_PROMPT, 1, {'ru': '9 > 5 — условие верно, a = 9 + 1 = 10', 'uz': "9 > 5 — shart to'g'ri, a = 9 + 1 = 10"},
                  code='NUR a 9\nQUR a > 5 { KAS a 1 }', options=['9', '10', '6', '15']),

            _item(2, _A_PROMPT, 3, {
                'ru': '3 > 5 — неверно, команды в скобках пропускаются; a = 3 + 1 = 4',
                'uz': "3 > 5 — noto'g'ri, qavs ichi bajarilmaydi; a = 3 + 1 = 4",
            }, code='NUR a 3\nQUR a > 5 { KAS a 10 }\nKAS a 1', options=['14', '13', '3', '4']),
            _item(2, _A_PROMPT, 1, {'ru': 'После VEX a = 6, b = 1; a = 6 + 1 = 7', 'uz': 'VEX dan keyin a = 6, b = 1; a = 6 + 1 = 7'},
                  code='NUR a 1\nNUR b 6\nVEX a b\nKAS a b', options=['12', '7', '2', '6']),
            _item(2, _A_PROMPT, 2, {'ru': 'b = 3 + 2 = 5, затем a = 2 + 5 = 7', 'uz': 'b = 3 + 2 = 5, keyin a = 2 + 5 = 7'},
                  code='NUR a 2\nNUR b 3\nKAS b a\nKAS a b', options=['5', '8', '7', '10']),

            _item(3, _A_PROMPT, 1, {
                'ru': 'KAS a a удваивает a: 1 → 2 → 4 → 8 → 16',
                'uz': 'KAS a a — a ni ikki barobar oshiradi: 1 → 2 → 4 → 8 → 16',
            }, code='NUR a 1\nTAK 4 { KAS a a }', options=['5', '16', '8', '32']),
            _item(3, {'ru': 'Чему равно b после выполнения программы?', 'uz': 'Dastur bajarilgandan keyin b nechaga teng?'}, 1, {
                'ru': '1-й раз: a = 1, b = 1; 2-й раз: a = 1, b = 2; 3-й раз: a = 2, b = 3',
                'uz': '1-marta: a = 1, b = 1; 2-marta: a = 1, b = 2; 3-marta: a = 2, b = 3',
            }, code='NUR a 0\nNUR b 1\nTAK 3 {\n  KAS a b\n  VEX a b\n}', options=['2', '3', '5', '4']),
            _item(3, _A_PROMPT, 3, {
                'ru': '4 → 5 (4 > 5 неверно) → 6 (5 > 5 неверно) → 16 + 1 = 17 (6 > 5 верно)',
                'uz': "4 → 5 (4 > 5 emas) → 6 (5 > 5 emas) → 16 + 1 = 17 (6 > 5 to'g'ri)",
            }, code='NUR a 4\nTAK 3 {\n  QUR a > 5 { KAS a 10 }\n  KAS a 1\n}', options=['7', '16', '27', '17']),
        ],
    },

    # -- Artificial grammar -----------------------------------------------------------
    {
        'key': 'grammar-a', 'family': 'grammar',
        'title_ru': 'Искусственный язык: словообразование', 'title_uz': "Sun'iy til: so'z yasash",
        'rules_ru': [
            'tavo — книга, lemu — дом, pira — птица',
            'ra- (в начале слова) — большой: ratavo — большая книга',
            'mi- (в начале слова) — маленький: mitavo — маленькая книга',
            '-ki (в конце слова) — множественное число',
            'При добавлении -ki последняя гласная слова выпадает: tavo → tavki (книги)',
        ],
        'rules_uz': [
            'tavo — kitob, lemu — uy, pira — qush',
            "ra- (so'z boshida) — katta: ratavo — katta kitob",
            "mi- (so'z boshida) — kichik: mitavo — kichik kitob",
            "-ki (so'z oxirida) — ko'plik",
            "-ki qo'shilganda so'z oxiridagi unli tushib qoladi: tavo → tavki (kitoblar)",
        ],
        'items': [
            _item(1, {'ru': 'Что означает слово «lemki»?', 'uz': "«lemki» so'zi nimani anglatadi?"}, 1, {
                'ru': 'lemu + -ki → lemki (последняя u выпадает) — дома',
                'uz': 'lemu + -ki → lemki (oxirgi u tushadi) — uylar',
            }, options_ru=['большой дом', 'дома', 'маленький дом', 'дом'], options_uz=['katta uy', 'uylar', 'kichik uy', 'uy']),
            _item(1, {'ru': 'Что означает слово «rapira»?', 'uz': "«rapira» so'zi nimani anglatadi?"}, 2, {
                'ru': 'ra- + pira — большая птица', 'uz': 'ra- + pira — katta qush',
            }, options_ru=['птицы', 'маленькая птица', 'большая птица', 'большие птицы'],
                options_uz=['qushlar', 'kichik qush', 'katta qush', 'katta qushlar']),
            _item(1, {'ru': 'Как сказать «маленький дом»?', 'uz': '«Kichik uy» qanday aytiladi?'}, 1,
                  _same('mi- + lemu = milemu'), options=['ralemu', 'milemu', 'lemki', 'milemki']),

            _item(2, {'ru': 'Как сказать «большие книги»?', 'uz': '«Katta kitoblar» qanday aytiladi?'}, 2, {
                'ru': 'ra- + tavo + -ki, последняя o выпадает: ratavki',
                'uz': 'ra- + tavo + -ki, oxirgi o tushadi: ratavki',
            }, options=['ratavoki', 'tavkira', 'ratavki', 'mitavki']),
            _item(2, {'ru': 'Что означает слово «mipirki»?', 'uz': "«mipirki» so'zi nimani anglatadi?"}, 0, {
                'ru': 'mi- (маленький) + pir(a) + -ki (множ. число) — маленькие птицы',
                'uz': "mi- (kichik) + pir(a) + -ki (ko'plik) — kichik qushlar",
            }, options_ru=['маленькие птицы', 'большие птицы', 'маленькая птица', 'птицы'],
                options_uz=['kichik qushlar', 'katta qushlar', 'kichik qush', 'qushlar']),
            _item(2, {'ru': 'Как сказать «птицы»?', 'uz': '«Qushlar» qanday aytiladi?'}, 2,
                  _same('pira + -ki → pirki'), options=['piraki', 'rapira', 'pirki', 'mipira']),

            _item(3, {'ru': 'sulo — дерево. Как сказать «маленькие деревья»?', 'uz': "sulo — daraxt. «Kichik daraxtlar» qanday aytiladi?"}, 1, {
                'ru': 'mi- + sulo + -ki, последняя o выпадает: misulki',
                'uz': 'mi- + sulo + -ki, oxirgi o tushadi: misulki',
            }, options=['misuloki', 'misulki', 'sulkimi', 'rasulki']),
            _item(3, {'ru': 'Какое слово построено с нарушением правил?', 'uz': "Qaysi so'z qoidaga zid tuzilgan?"}, 2, {
                'ru': 'При добавлении -ki последняя гласная должна выпасть: правильно ratavki',
                'uz': "-ki qo'shilganda oxirgi unli tushishi kerak edi: to'g'risi ratavki",
            }, options=['mipira', 'lemki', 'ratavoki', 'ratavo']),
            _item(3, {'ru': 'kavi — река. Что означает слово «rakavki»?', 'uz': "kavi — daryo. «rakavki» so'zi nimani anglatadi?"}, 3, {
                'ru': 'ra- (большой) + kav(i) + -ki (множ. число) — большие реки',
                'uz': "ra- (katta) + kav(i) + -ki (ko'plik) — katta daryolar",
            }, options_ru=['большая река', 'маленькие реки', 'реки', 'большие реки'],
                options_uz=['katta daryo', 'kichik daryolar', 'daryolar', 'katta daryolar']),
        ],
    },
    {
        'key': 'grammar-b', 'family': 'grammar',
        'title_ru': 'Искусственный язык: построение предложений', 'title_uz': "Sun'iy til: gap tuzish",
        'rules_ru': [
            'dak — видеть, sol — читать',
            'ni — мы, ta — вы',
            'tavo — книга, lemu — дом',
            'Настоящее время: к глаголу добавляется -e (dake — видят сейчас); прошедшее время: -u (daku — видели)',
            'Порядок слов: глагол → кто → что. Например: dake ni lemu — мы видим дом',
        ],
        'rules_uz': [
            "dak — ko'rmoq, sol — o'qimoq",
            'ni — biz, ta — siz',
            'tavo — kitob, lemu — uy',
            "Hozirgi zamon: fe'lga -e qo'shiladi (dake — ko'ryapti); o'tgan zamon: -u qo'shiladi (daku — ko'rdi)",
            "So'z tartibi: fe'l → kim → nimani. Masalan: dake ni lemu — biz uyni ko'ryapmiz",
        ],
        'items': [
            _item(1, {'ru': 'Что означает предложение «sole ta tavo»?', 'uz': '«sole ta tavo» gapi nimani anglatadi?'}, 0, {
                'ru': 'sol + -e (сейчас), ta — вы, tavo — книга', 'uz': 'sol + -e (hozir), ta — siz, tavo — kitob',
            }, options_ru=['Вы читаете книгу', 'Мы читали книгу', 'Вы читали книгу', 'Книга читает вас'],
                options_uz=["Siz kitob o'qiyapsiz", "Biz kitob o'qidik", "Siz kitob o'qidingiz", "Kitob sizni o'qiyapti"]),
            _item(1, {'ru': 'Что означает предложение «daku ni lemu»?', 'uz': '«daku ni lemu» gapi nimani anglatadi?'}, 2, {
                'ru': 'dak + -u (прошедшее), ni — мы, lemu — дом', 'uz': "dak + -u (o'tgan zamon), ni — biz, lemu — uy",
            }, options_ru=['Мы видим дом', 'Вы видели дом', 'Мы видели дом', 'Дом видел нас'],
                options_uz=["Biz uyni ko'ryapmiz", "Siz uyni ko'rdingiz", "Biz uyni ko'rdik", "Uy bizni ko'rdi"]),
            _item(1, {'ru': 'Как сказать «Мы читали книгу»?', 'uz': "«Biz kitob o'qidik» qanday aytiladi?"}, 1, {
                'ru': 'sol + -u (прошедшее), затем ni (мы), затем tavo', 'uz': "sol + -u (o'tgan zamon), keyin ni (biz), keyin tavo",
            }, options=['sole ni tavo', 'solu ni tavo', 'ni solu tavo', 'solu ta tavo']),

            _item(2, {'ru': 'Как сказать «Вы видите дом»?', 'uz': "«Siz uyni ko'ryapsiz» qanday aytiladi?"}, 3, {
                'ru': 'Глагол первым: dake, затем ta, затем lemu', 'uz': "Fe'l birinchi: dake, keyin ta, keyin lemu",
            }, options=['daku ta lemu', 'ta dake lemu', 'dake ni lemu', 'dake ta lemu']),
            _item(2, {'ru': 'Что означает предложение «dake lemu ni»?', 'uz': '«dake lemu ni» gapi nimani anglatadi?'}, 1, {
                'ru': 'Порядок: глагол → кто → что. Здесь «кто» — lemu (дом), «что» — ni (мы)',
                'uz': "Tartib: fe'l → kim → nimani. Bu yerda «kim» — lemu (uy), «nimani» — ni (biz)",
            }, options_ru=['Мы видим дом', 'Дом видит нас', 'Мы видели дом', 'Дом видит вас'],
                options_uz=["Biz uyni ko'ryapmiz", "Uy bizni ko'ryapti", "Biz uyni ko'rdik", "Uy sizni ko'ryapti"]),
            _item(2, {'ru': 'Какое предложение построено правильно?', 'uz': "Qaysi gap to'g'ri tuzilgan?"}, 2, {
                'ru': 'Глагол стоит первым и оканчивается на -e или -u: solu ta tavo — вы читали книгу',
                'uz': "Fe'l birinchi keladi va -e yoki -u bilan tugaydi: solu ta tavo — siz kitob o'qidingiz",
            }, options=['ta solu tavo', 'solo ta tavo', 'solu ta tavo', 'tavo solu ta']),

            _item(3, {'ru': 'kem — писать. Как сказать «Вы писали книгу»?', 'uz': "kem — yozmoq. «Siz kitob yozdingiz» qanday aytiladi?"}, 1, {
                'ru': 'kem + -u (прошедшее), ta — вы, tavo — книга', 'uz': "kem + -u (o'tgan zamon), ta — siz, tavo — kitob",
            }, options=['keme ta tavo', 'kemu ta tavo', 'kemu ni tavo', 'ta kemu tavo']),
            _item(3, {'ru': 'Какое предложение означает «Книга видела дом»?', 'uz': "Qaysi gap «Kitob uyni ko'rdi» ma'nosini beradi?"}, 2, {
                'ru': 'daku (видели) → tavo (кто) → lemu (что)', 'uz': "daku (ko'rdi) → tavo (kim) → lemu (nimani)",
            }, options=['daku lemu tavo', 'dake tavo lemu', 'daku tavo lemu', 'tavo daku lemu']),
            _item(3, {'ru': 'Переведите предложение «daku ta tavo» в настоящее время.', 'uz': "«daku ta tavo» gapini hozirgi zamonga o'tkazing."}, 0, {
                'ru': 'Время меняется только в глаголе: daku → dake', 'uz': "Zamon faqat fe'lda o'zgaradi: daku → dake",
            }, options=['dake ta tavo', 'daku ta tave', 'dake te tavo', 'dake ta tave']),
        ],
    },
]
