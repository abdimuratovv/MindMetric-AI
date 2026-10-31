"""Generate draft JSON/Markdown resources only; no Django or production writes."""
import hashlib
from pathlib import Path

from authoring import HERE, compile_module, digest, markdown, write_json
from module21 import build as module21
from module22 import build as module22
from module23 import build as module23
from module24 import build as module24
from module25 import build as module25
from module26 import build as module26
from projects import build as projects


def main():
    files = ['authoring.py', 'build_resources.py', 'module21.py', 'module22.py', 'module23.py',
             'module24.py', 'module25.py', 'module26.py', 'projects.py', 'pseudocode.uz.md', 'pseudocode.ru.md']
    # Text source hashes use LF on every checkout, including Windows autocrlf.
    manifest = {name: hashlib.sha256((HERE / name).read_text(encoding='utf-8').encode('utf-8')).hexdigest() for name in files}
    write_json(HERE / 'authoring-manifest.json', manifest)
    sources = [
        {'id': 'source-curriculum', 'filename': 'Oqitish moduli.docx',
         'sha256': 'c11956549286d3f6c99ae327b0dc0ee6dcdc4714e4e069d385901f0f8d58a473'},
        {'id': 'authored-cluster2', 'filename': 'authoring-manifest.json',
         'sha256': hashlib.sha256((HERE / 'authoring-manifest.json').read_text(encoding='utf-8').encode('utf-8')).hexdigest()}
    ]
    inventory = []
    for build in [module21, module22, module23, module24, module25, module26]:
        data, ru = compile_module(build(), sources)
        if data['module']['order'] == 6:
            data['projects'] = []
            ru['projects'] = {}
            for project in projects():
                row = {'key': project['key'], 'assessment': 'self_review'}
                local = {}
                for name in ('title', 'brief', 'constraints', 'steps', 'deliverables', 'rubric'):
                    value = project[name]
                    row[name + '_uz'] = value['uz'] if isinstance(value, dict) else [p['uz'] for p in value]
                    local[name] = value['ru'] if isinstance(value, dict) else [p['ru'] for p in value]
                data['projects'].append(row)
                ru['projects'][project['key']] = local
        ru['source_hash'] = digest(data)
        key = data['module']['key']
        write_json(HERE / f'{key}.v1.json', data)
        write_json(HERE / 'translations' / f'{key}.v1.ru.json', ru)
        for language in ('uz', 'ru'):
            text = markdown(data, ru, language)
            for project in data.get('projects', []):
                local = ru['projects'][project['key']]
                pick = lambda name: local[name] if language == 'ru' else project[name + '_uz']
                text += '\n## ' + pick('title') + '\n\n' + pick('brief') + '\n\n'
                labels = {'uz': ['Cheklovlar', 'Bosqichlar', 'Taqdim etiladigan ishlar', 'O‘zini tekshirish'],
                          'ru': ['Ограничения', 'Этапы', 'Материалы результата', 'Самопроверка']}
                for name, label in zip(('constraints', 'steps', 'deliverables', 'rubric'), labels[language]):
                    text += '### ' + label + '\n\n' + '\n'.join('- ' + p for p in pick(name)) + '\n\n'
            path = HERE / f"2.{data['module']['order']}-mavzu.{language}.md"
            path.write_text(text.rstrip() + '\n', encoding='utf-8', newline='\n')
        inventory.append({'key': key, 'topic_number': data['module']['topic_number'], 'title_uz': data['module']['title_uz'],
                          'title_ru': ru['title'], 'skills': 5, 'lessons': 5, 'exercises': 20,
                          'practice': 10, 'precheck': 5, 'postcheck': 5,
                          'projects': len(data.get('projects', [])), 'source_hash': digest(data)})
    write_json(HERE / 'inventory.json', {'cluster': 2, 'status': 'draft', 'languages': ['uz', 'ru'], 'modules': inventory})
    print('Generated: 6 modules, 30 lessons/examples, 120 exercises, 2 projects; UZ/RU; draft only.')


if __name__ == '__main__':
    main()
