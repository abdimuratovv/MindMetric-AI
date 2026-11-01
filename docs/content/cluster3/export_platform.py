"""Export reviewed standalone drafts into the schema-3 platform contract."""
from copy import deepcopy
from authoring import HERE, b, digest, write_json
from activities import build as activities
import json

INDICATORS = {1: ['patience', 'attention', 'problem_solving'], 2: ['teamwork'],
              3: ['attention'], 4: ['learning_speed']}
RULES = [b(s) for s in [
    'Python 3: = qiymat beradi; ==, !=, <, >, <=, >= taqqoslaydi. || Python 3: = присваивает; ==, !=, <, >, <=, >= сравнивают.',
    'Python bloklari : va bir xil chekinish bilan yoziladi; satr oxirida ; majburiy emas. || Блоки Python записываются с : и одинаковым отступом; ; в конце строки не обязательна.',
    'Ro‘yxat indekslari 0 dan boshlanadi. range(a, b) yuqori b chegarasini kiritmaydi. || Индексы списков начинаются с 0. range(a, b) не включает верхнюю границу b.',
    'and, or, not — mantiqiy amallar; True va False mantiqiy qiymatlar. || and, or, not — логические операции; True и False — логические значения.',
    'None — alohida qiymat. return funksiyadan natija beradi; print qiymatni ko‘rsatadi. || None — отдельное значение. return возвращает результат функции; print показывает значение.',
    'Trace jadvali satrdan keyingi holatni yozadi. Debugger strelkasi hali bajarilmagan satrni ko‘rsatadi. || Таблица трассировки записывает состояние после строки. Стрелка отладчика показывает ещё не выполненную строку.',
    'Git: working tree — ishchi nusxa, index — tanlangan holat, commit — mahalliy tarix. || Git: working tree — рабочая копия, index — выбранное состояние, commit — локальная история.',
    'StudyTools 1.0 — kursning lokal o‘quv API si. Topshiriqdagi hujjat va versiyaga amal qiling. || StudyTools 1.0 — локальный учебный API курса. Следуйте документации и версии из задания.'
]]


def main():
    root = HERE.parents[2]
    tasks = {p['key']: p for p in activities()}
    task_keys = {1: 'debugging-challenge', 2: 'team-library', 4: 'documentation-lab'}
    exports = []
    for path in sorted(HERE.glob('*.v1.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        if 'module' not in data:
            continue
        data = deepcopy(data)
        meta = data['module']; order = meta['order']; key = meta['key']
        ru = json.loads((HERE / 'translations' / f'{key}.v1.ru.json').read_text(encoding='utf-8'))
        data.pop('resource_format'); data.pop('integration_status')
        data['schema_version'] = 3
        meta['indicator_keys'] = INDICATORS[order]
        meta['diagnostic_coverage_note_uz'] = 'Aniq diagnostika savoli xaritasi tasdiqlanmagan; boshlang‘ich tekshiruvdan foydalaning.'
        data['notation_uz'] = [p['uz'] for p in RULES]
        ru['notation'] = [p['ru'] for p in RULES]
        for skill in data['skills']:
            skill['indicator_keys'] = INDICATORS[order]
        for lesson in data['lessons']:
            lesson['theory_uz'].insert(0, 'Natija: ' + lesson.pop('outcome_uz'))
            target = ru['lessons'][lesson['key']]
            target['theory'].insert(0, 'Результат: ' + target.pop('outcome'))
        for exercise in data['exercises']:
            exercise['difficulty'] = 'medium'
        for pair in data['blueprint']['matched_pairs']:
            pair['difficulty'] = 'medium'
        data['blueprint'].update(
            comparison_note_uz='Ko‘nikmalar bo‘yicha juftlangan; statistik tenglashtirish yoki shaxs xususiyatlari o‘sishi da’vosi yo‘q.',
            exhaustion_note_uz='Bitta mustaqil yakuniy to‘plam mavjud; qayta mashq mustaqil o‘sish o‘lchovi emas.')
        data['projects'] = []; ru['projects'] = {}
        if order in task_keys:
            task = tasks[task_keys[order]]
            fields = {'title': task['title'], 'brief': task['goal'],
                      'constraints': task['materials'] + task['contract'], 'steps': task['steps'],
                      'deliverables': task['deliverables'], 'rubric': task['rubric']}
            project = {'key': task['key'], 'assessment': 'self_review'}
            local = {}
            for field, value in fields.items():
                project[field + '_uz'] = value['uz'] if isinstance(value, dict) else [p['uz'] for p in value]
                local[field] = value['ru'] if isinstance(value, dict) else [p['ru'] for p in value]
            data['projects'].append(project); ru['projects'][task['key']] = local
        data['study_files'] = []; ru['study_files'] = {}
        if order in (1, 4):
            filename = 'debugging-starter.py.txt' if order == 1 else 'lab_studytools.py'
            title = b('Debugging uchun starter || Стартовый код для отладки' if order == 1 else
                      'StudyTools 1.0 o‘quv API kodi || Код учебного API StudyTools 1.0')
            file_key = 'debugging-starter' if order == 1 else 'studytools-api'
            data['study_files'].append({'key': file_key, 'title_uz': title['uz'], 'filename': filename,
                                       'content': (HERE / filename).read_text(encoding='utf-8')})
            ru['study_files'][file_key] = {'title': title['ru']}
        # Teacher-only activity solutions and reference code never enter platform payloads.
        ru['source_hash'] = digest(data)
        for folder in (HERE / 'platform', root / 'backend/apps/development/content/cluster3'):
            write_json(folder / f'{key}.v1.json', data)
        for folder in (HERE / 'platform/translations', root / 'backend/apps/development/content/translations'):
            write_json(folder / f'{key}.v1.ru.json', ru)
        exports.append({'key': key, 'source_hash': digest(data), 'cluster': 3, 'schema_version': 3})
    write_json(HERE / 'platform/inventory.json', exports)
    print(f'Exported {len(exports)} schema-3 modules and complete Russian overlays.')


if __name__ == '__main__':
    main()
