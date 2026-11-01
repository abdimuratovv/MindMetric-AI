"""Deterministically generate standalone draft resources. No DB, app or network."""
import hashlib
from authoring import HERE, compile_module, digest, markdown, write_json
from activities import build as activities, render
from module31 import build as module31
from module32 import build as module32
from module33 import build as module33
from module34 import build as module34

CURRICULUM_SHA = 'c11956549286d3f6c99ae327b0dc0ee6dcdc4714e4e069d385901f0f8d58a473'


def main():
    paths = sorted([*HERE.glob('*.py'), *HERE.glob('bridge.*.md'), HERE / 'debugging-starter.py.txt'])
    manifest = {p.name: hashlib.sha256(p.read_text(encoding='utf-8').encode()).hexdigest() for p in paths}
    write_json(HERE / 'authoring-manifest.json', manifest)
    sources = [{'id': 'source-curriculum', 'filename': 'Oqitish moduli.docx', 'sha256': CURRICULUM_SHA},
               {'id': 'authored-cluster3', 'filename': 'authoring-manifest.json', 'sha256': digest(manifest)}]
    inventory = []
    for build in (module31, module32, module33, module34):
        data, ru = compile_module(build(), sources)
        key = data['module']['key']
        write_json(HERE / f'{key}.v1.json', data)
        write_json(HERE / 'translations' / f'{key}.v1.ru.json', ru)
        topic = data['module']['topic_number']
        for language in ('uz', 'ru'):
            for audience in ('teacher', 'student', 'checks'):
                suffix = '' if audience == 'teacher' else f'.{audience}'
                (HERE / f'{topic}-mavzu.{language}{suffix}.md').write_text(
                    markdown(data, ru, language, audience), encoding='utf-8', newline='\n')
        inventory.append({'key': key, 'topic_number': topic, 'skills': 5, 'lessons': 5,
                          'examples': 5, 'practice': 10, 'precheck': 5, 'postcheck': 5,
                          'source_hash': digest(data)})
    tasks = activities()
    write_json(HERE / 'activities.v1.json', {'resource_format': 'mindmetric-open-activities-v1', 'activities': tasks})
    for task in tasks:
        for language in ('uz', 'ru'):
            for teacher in (False, True):
                suffix = '.teacher' if teacher else '.student'
                (HERE / f"{task['key']}.{language}{suffix}.md").write_text(
                    render(task, language, teacher), encoding='utf-8', newline='\n')
    write_json(HERE / 'inventory.json', {'cluster': 3, 'status': 'draft',
        'integration_status': 'not_importable', 'languages': ['uz', 'ru'],
        'modules': inventory, 'open_activities': len(tasks)})
    print('Generated 4 bilingual modules: 20 lessons/examples, 80 questions, 3 open activities.')


if __name__ == '__main__':
    main()
