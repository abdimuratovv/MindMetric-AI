"""Version/hash-bound language overlays; never modify frozen content or grading."""
import json
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from .validation import content_hash, require, text

DIRECTORY=Path(__file__).resolve().parent/'content/translations'


def validate_translation(source, translated):
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
        lines(question['solution_steps_uz'],target.get('solution_steps'),question['key'])
        field(question['common_error_uz'],target.get('common_error'),question['key'])
        if question['purpose']=='practice':field(question['hint_uz'],target.get('hint'),question['key'])
        else:require(target.get('hint') is None,'Check translations cannot contain hints.')
        require(set(target.get('options',{}))=={o['id'] for o in question['options']},'Translated option IDs changed.')
        for option in question['options']:
            item=target['options'][option['id']]
            field(option['text_uz'],item.get('text'),question['key'])
            field(option['feedback_uz'],item.get('feedback'),question['key'])
    return translated


@lru_cache(maxsize=32)
def bundled_translation(key,version):
    path=DIRECTORY/f'{key}.v{version}.ru.json'
    if not path.exists():return None
    source=DIRECTORY.parent/'cluster1'/f'{key}.v{version}.json'
    return validate_translation(json.loads(source.read_text(encoding='utf-8')),json.loads(path.read_text(encoding='utf-8')))


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
