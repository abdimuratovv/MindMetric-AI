"""
Seed content for the patience indicator (AnagramItem).

Per language, six words per difficulty tier plus six unsolvable letter sets, so
a retake can draw a completely fresh set. Unsolvable sets are real words with
one letter swapped ("near-words"), so they look just as solvable as the rest.
Where the same letters spell more than one word, every such word is accepted.
Uzbek words avoid the o'/g'/sh/ch digraphs so every tile is one letter.
"""

_WORDS = {
    'ru': {
        'easy': [['КНИГА'], ['ШКОЛА'], ['ЛАМПА'], ['ОКНО'], ['СЛОН'], ['ПТИЦА']],
        'medium': [['ДОРОГА', 'ГОРОДА'], ['СОБАКА'], ['МАШИНА'], ['ЯБЛОКО'], ['ПЛАНЕТА'], ['КАРТИНА']],
        'hard': [['ПРОГРАММА'], ['БИБЛИОТЕКА'], ['ТЕЛЕВИЗОР'], ['АЛГОРИТМ', 'ЛОГАРИТМ'], ['ПОДСОЛНУХ'], ['КАРАНДАШ']],
        'unsolvable': ['ДОРОПА', 'МАШИРН', 'ПЛАНЕКА', 'ТЕЛЕВИЗОН', 'ПРОГРАМУА', 'КАРАНТАШ'],
    },
    'uz': {
        'easy': [['KITOB'], ['QALAM'], ['OLMA', 'OLAM'], ['BOLA'], ['BOZOR'], ['BAHOR']],
        'medium': [['DAFTAR'], ['MAKTAB'], ['YULDUZ'], ['TARVUZ'], ['DARAXT'], ['DOSTON']],
        'hard': [['AVTOBUS'], ['TELEFON'], ['MUSTAQIL'], ['TARJIMON'], ['TELEVIZOR'], ['KUTUBXONA']],
        'unsolvable': ['DAKTAR', 'MOKTAB', 'YILDUZ', 'TELEFAN', 'MUSTAKIR', 'TARJIBON'],
    },
}


def _build():
    items = []
    for language, tiers in _WORDS.items():
        for difficulty in ('easy', 'medium', 'hard'):
            for n, answers in enumerate(tiers[difficulty], start=1):
                assert all(sorted(a) == sorted(answers[0]) for a in answers), answers
                items.append({
                    'key': f'anagram-{language}-{difficulty}-{n}', 'language': language, 'difficulty': difficulty,
                    'letters': answers[0], 'answers': answers,
                })
        for n, letters in enumerate(tiers['unsolvable'], start=1):
            items.append({
                'key': f'anagram-{language}-unsolvable-{n}', 'language': language, 'difficulty': 'unsolvable',
                'letters': letters, 'answers': [],
            })
    return items


ANAGRAM_ITEMS = _build()
