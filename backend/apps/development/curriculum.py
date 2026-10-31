"""Presentation metadata; content and progress stay owned by module versions."""

CLUSTERS = {
    1: {
        'uz': ('Intellektual akademik blok', 'Matematika, mantiq va diskret savodxonlik.'),
        'ru': ('Интеллектуальный академический блок', 'Математика, логика и дискретная грамотность.'),
    },
    2: {
        'uz': ('Algoritmik-amaliy blok', 'Algoritmlar, shartlar, sikllar va amaliy yechimlar.'),
        'ru': ('Алгоритмико-практический блок', 'Алгоритмы, условия, циклы и практические решения.'),
    },
}


def cluster_cards(modules, language='uz'):
    language = language if language in ('uz', 'ru') else 'uz'
    return [
        {'id': number, 'title': CLUSTERS[number][language][0],
         'description': CLUSTERS[number][language][1],
         'module_count': sum(module.cluster == number for module in modules)}
        for number in sorted({module.cluster for module in modules})
    ]
