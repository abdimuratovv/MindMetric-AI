"""Version/hash-bound language overlays; never modify frozen content or grading."""
import json
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from .validation import ContentValidationError, content_hash, require, text

DIRECTORY=Path(__file__).resolve().parent/'content/translations'


def validate_translation(source, translated):
    try:
        return _validate_translation(source, translated)
    except ContentValidationError:
        raise
    except (TypeError, KeyError, ValueError, AttributeError) as exc:
        raise ContentValidationError(f'Malformed translation: {exc}') from exc


def _validate_translation(source, translated):
    require(isinstance(translated, dict), 'Translation must be an object.')
    require(translated.get('module_key')==source['module']['key'], 'Translation module mismatch.')
    require(translated.get('version')==source['module']['version'], 'Translation version mismatch.')
    require(translated.get('language')=='ru', 'Unsupported translation language.')
    require(translated.get('source_hash')==content_hash(source), 'Translation source hash mismatch.')
    def field(original,value,label):
        text(value,label)
        # Grammar can reorder numbers, but cannot add/drop/change constants.
        numbers=lambda s:Counter(re.findall(r'\d+|[⁰¹²³⁴⁵⁶⁷⁸⁹]+',s))
        require(numbers(original)==numbers(value),f'{label}: mathematical constants changed.')
    def lines(original,value,label):
        require(isinstance(value,list) and len(value)==len(original),f'{label}: missing paragraphs.')
        for a,b in zip(original,value):field(a,b,label)
    field(source['module']['title_uz'],translated.get('title'),'title')
    for category in ('skills','lessons','exercises'):
        require(isinstance(translated.get(category),dict),f'Missing translated {category}.')
        require(set(translated[category])=={r['key'] for r in source[category]},f'Incomplete translated {category}.')
    for skill in source['skills']:
        field(skill['title_uz'],translated['skills'][skill['key']],skill['key'])
    for lesson in source['lessons']:
        target=translated['lessons'][lesson['key']]
        field(lesson['title_uz'],target.get('title'),lesson['key'])
        lines(lesson['theory_uz'],target.get('theory'),lesson['key'])
        example=target.get('worked_example',{})
        field(lesson['worked_example']['prompt_uz'],example.get('prompt'),lesson['key'])
        lines(lesson['worked_example']['solution_steps_uz'],example.get('solution_steps'),lesson['key'])
        field(lesson['worked_example']['answer_uz'],example.get('answer'),lesson['key'])
    for question in source['exercises']:
        target=translated['exercises'][question['key']]
        require('answer_key' not in target, 'Translations cannot override grading.')
        field(question['prompt_uz'],target.get('prompt'),question['key'])
        if source['schema_version'] == 2:
            operators = r'←|==|!=|≥|≤|[<>]|\b(?:TRUE|FALSE|AND|OR|NOT|TO|OUTPUT|RETURN|INPUT|DECISION|START|END|div|mod)\b'
            require(Counter(re.findall(operators, question['prompt_uz'])) == Counter(re.findall(operators, target['prompt'])),
                    f'{question["key"]}: code operators changed.')
        lines(question['solution_steps_uz'],target.get('solution_steps'),question['key'])
        field(question['common_error_uz'],target.get('common_error'),question['key'])
        if question['purpose']=='practice':field(question['hint_uz'],target.get('hint'),question['key'])
        else:require(target.get('hint') is None,'Check translations cannot contain hints.')
        require(set(target.get('options',{}))=={o['id'] for o in question['options']},'Translated option IDs changed.')
        for option in question['options']:
            item=target['options'][option['id']]
            field(option['text_uz'],item.get('text'),question['key'])
            field(option['feedback_uz'],item.get('feedback'),question['key'])
    if source['schema_version'] == 2:
        require(set(translated) <= {'module_key', 'version', 'language', 'source_hash', 'title',
                                   'skills', 'lessons', 'exercises', 'notation', 'projects'}, 'Unknown translation fields.')
        lines(source['notation_uz'], translated.get('notation'), 'notation')
        projects = source.get('projects', [])
        local = translated.get('projects', {})
        require(isinstance(local, dict) and set(local) == {p['key'] for p in projects}, 'Incomplete translated projects.')
        for project in projects:
            target = local[project['key']]
            require(set(target) == {'title', 'brief', 'constraints', 'steps', 'deliverables', 'rubric'},
                    'Invalid project translation fields.')
            for name in ('title', 'brief'):
                field(project[name + '_uz'], target[name], project['key'])
            for name in ('constraints', 'steps', 'deliverables', 'rubric'):
                lines(project[name + '_uz'], target[name], project['key'])
    return translated


@lru_cache(maxsize=32)
def bundled_translation(key,version):
    path=DIRECTORY/f'{key}.v{version}.ru.json'
    if not path.exists():return None
    matches = [directory / f'{key}.v{version}.json' for directory in
               (DIRECTORY.parent / 'cluster1', DIRECTORY.parent / 'cluster2')]
    matches = [source for source in matches if source.exists()]
    require(len(matches) == 1, 'Translation needs exactly one canonical source.')
    try:
        return validate_translation(json.loads(matches[0].read_text(encoding='utf-8')),
                                    json.loads(path.read_text(encoding='utf-8')))
    except (ValueError, UnicodeError) as exc:
        raise ContentValidationError(f'Invalid translation JSON: {exc}') from exc


def validate_release_translations(contents):
    """Every topic in an advertised bilingual release needs a complete overlay."""
    for source in contents:
        meta = source['module']
        translated = bundled_translation(meta['key'], meta['version'])
        require(translated is not None, f'{meta["key"]}: complete Russian resources required for release.')
        validate_translation(source, translated)


class ContentLocale:
    def __init__(self,module,language='uz'):
        candidate=bundled_translation(module.key,module.version) if language=='ru' else None
        self.data=candidate if candidate and candidate['source_hash']==module.content_hash else None
        self.language='ru' if self.data else 'uz'

    def title(self,module):return self.data['title'] if self.data else module.title_uz
    def skill(self,key,original):return self.data['skills'].get(key,original) if self.data else original
    def lesson(self,key):return self.data['lessons'][key] if self.data else None
    def exercise(self,key):return self.data['exercises'][key] if self.data else None
    def progress(self,skills):
        return [{**skill,'title':self.skill(skill['key'],skill['title']),'content_language':self.language} for skill in skills]

    def notation(self, module):
        return self.data.get('notation', []) if self.data else module.content_snapshot.get('notation_uz', [])

    def projects(self, module):
        result = []
        for project in module.content_snapshot.get('projects', []):
            fields = ('title', 'brief', 'constraints', 'steps', 'deliverables', 'rubric')
            translated = self.data['projects'][project['key']] if self.data else None
            result.append({'key': project['key'], 'assessment': 'self_review', 'content_language': self.language,
                           **{name: translated[name] if translated else project[name + '_uz'] for name in fields}})
        return result
