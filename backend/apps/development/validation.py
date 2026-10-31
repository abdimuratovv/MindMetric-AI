"""Validate legacy academic and bilingual algorithmic content before writes."""

import hashlib
import json
import re
from collections import Counter

from .numeric import parse_numeric


class ContentValidationError(ValueError):
    pass


def content_hash(data):
    raw = json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def require(condition, message):
    if not condition:
        raise ContentValidationError(message)


def text(value, label, maximum=None):
    require(isinstance(value, str) and bool(value.strip()), f'{label}: nonempty text required.')
    require(maximum is None or len(value) <= maximum, f'{label}: text is too long.')


def strings(value, label):
    require(isinstance(value, list) and bool(value), f'{label}: nonempty list required.')
    for item in value:
        text(item, label)


def records(value, label):
    require(isinstance(value, list) and bool(value), f'{label}: nonempty list required.')
    require(all(isinstance(row, dict) for row in value), f'{label}: object records required.')
    return value


def keyed(value, label):
    rows = records(value, label)
    result = {}
    for row in rows:
        key = row.get('key')
        require(isinstance(key, str) and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', key))
                and len(key) <= 64, f'{label}: invalid key.')
        require(key not in result, f'{label}: duplicate key {key}.')
        result[key] = row
    return result


def validate_content(data, *, known_skills=None, diagnostic_keys=None):
    try:
        return _validate_content(data, known_skills=known_skills, diagnostic_keys=diagnostic_keys)
    except ContentValidationError:
        raise
    except (TypeError, KeyError, ValueError, RecursionError) as exc:
        raise ContentValidationError(f'Malformed content: {exc}') from exc


def _validate_content(data, *, known_skills=None, diagnostic_keys=None):
    require(isinstance(data, dict), 'Content must be an object.')
    schema = data.get('schema_version')
    require(type(schema) is int and schema in (1, 2), 'Unsupported schema_version.')
    module = data.get('module')
    require(isinstance(module, dict), 'module is required.')
    keyed([module], 'module')
    require(type(module.get('version')) is int and module['version'] >= 1, 'Invalid module version.')
    require(type(module.get('order')) is int and 0 <= module['order'] <= 32767, 'Invalid module order.')
    require(module.get('status') == 'draft', 'Imports must be draft; publish explicitly in admin.')
    require(module.get('content_language') == 'uz', 'Schema 1 supports Uzbek content with explicit fallback.')
    text(module.get('title_uz'), 'module.title_uz', 200)
    require(module.get('title_ru') is None or isinstance(module['title_ru'], str), 'Invalid title_ru.')
    require(len(module.get('title_ru') or '') <= 200, 'title_ru is too long.')
    text(module.get('review_status'), 'module.review_status', 40)
    if schema == 1:
        require(type(module.get('cluster', 1)) is int and module.get('cluster', 1) == 1,
                'Schema 1 belongs to cluster one.')
        require(not data.get('projects') and not data.get('notation_uz'), 'New study resources require schema 2.')
        indicators = {'math', 'logic', 'iq'}
    else:
        require(type(module.get('cluster')) is int and module['cluster'] == 2, 'Schema 2 requires cluster two.')
        require(module['order'] in range(1, 7), 'Invalid cluster-two order.')
        require(module.get('topic_number') == f"2.{module['order']}", 'Topic number mismatch.')
        indicators = {'algorithmic', 'creative', 'problem_solving'}
        strings(data.get('notation_uz'), 'notation_uz')
        require(len(data['notation_uz']) <= 16, 'Too many notation rules.')
        for rule in data['notation_uz']:
            text(rule, 'notation_uz', 1000)
        projects = data.get('projects', [])
        require(isinstance(projects, list) and len(projects) <= 10, 'Invalid projects.')
        if projects:
            keyed(projects, 'projects')
        fields = {'key', 'assessment', 'title_uz', 'brief_uz', 'constraints_uz',
                  'steps_uz', 'deliverables_uz', 'rubric_uz'}
        for project in projects:
            require(set(project) == fields and project['assessment'] == 'self_review',
                    'Projects must be self-review study resources, without grading keys.')
            text(project['title_uz'], 'project.title_uz', 200)
            text(project['brief_uz'], 'project.brief_uz')
            for field in ('constraints_uz', 'steps_uz', 'deliverables_uz', 'rubric_uz'):
                strings(project[field], 'project.' + field)
    strings(module.get('indicator_keys'), 'module.indicator_keys')
    require(set(module['indicator_keys']) <= indicators, 'Invalid indicators for this cluster.')

    sources = records(data.get('sources'), 'sources')
    source_ids = set()
    for source in sources:
        text(source.get('id'), 'source.id')
        require(source['id'] not in source_ids, 'Duplicate source id.')
        source_ids.add(source['id'])
        text(source.get('filename'), 'source.filename')
        require(isinstance(source.get('sha256'), str) and bool(re.fullmatch(r'[0-9a-fA-F]{64}', source['sha256'])),
                'Invalid source SHA-256.')

    skills = keyed(data.get('skills'), 'skills')
    require(len(skills) == 5, 'The pilot requires five skills per module.')
    graph = dict(known_skills or {})
    for key, skill in skills.items():
        text(skill.get('title_uz'), f'{key}.title_uz', 200)
        strings(skill.get('indicator_keys'), f'{key}.indicator_keys')
        require(set(skill['indicator_keys']) <= set(module['indicator_keys']), f'{key}: invalid indicators.')
        parents = skill.get('prerequisite_keys')
        require(isinstance(parents, list) and all(isinstance(parent, str) for parent in parents)
                and len(parents) == len(set(parents)), f'{key}: invalid prerequisites.')
        graph[key] = parents
    completed = set()

    def visit(key, ancestors):
        require(key in graph, f'Unknown prerequisite skill: {key}.')
        require(key not in ancestors, f'Prerequisite cycle: {key}.')
        if key in completed:
            return
        for parent in graph[key]:
            visit(parent, ancestors | {key})
        completed.add(key)

    for key in skills:
        visit(key, set())

    lessons = keyed(data.get('lessons'), 'lessons')
    require(Counter(row.get('skill_key') for row in lessons.values()) == Counter({key: 1 for key in skills}),
            'Each skill needs exactly one lesson in the pilot.')
    for key, lesson in lessons.items():
        text(lesson.get('title_uz'), f'{key}.title_uz', 200)
        strings(lesson.get('theory_uz'), f'{key}.theory_uz')
        example = lesson.get('worked_example')
        require(isinstance(example, dict), f'{key}: worked_example required.')
        text(example.get('prompt_uz'), f'{key}.example.prompt')
        strings(example.get('solution_steps_uz'), f'{key}.example.solution')
        text(example.get('answer_uz'), f'{key}.example.answer')

    exercises = keyed(data.get('exercises'), 'exercises')
    require(len(exercises) == 20, 'The pilot requires 20 exercises.')
    prompts = set()
    for key, question in exercises.items():
        require(question.get('skill_key') in skills, f'{key}: unknown skill.')
        require(question.get('purpose') in {'practice', 'precheck', 'postcheck'}, f'{key}: invalid purpose.')
        require(question.get('difficulty') in {'easy', 'medium', 'hard'}, f'{key}: invalid difficulty.')
        text(question.get('prompt_uz'), f'{key}.prompt_uz')
        require(question['prompt_uz'].strip() not in prompts, f'{key}: duplicate prompt.')
        prompts.add(question['prompt_uz'].strip())
        strings(question.get('solution_steps_uz'), f'{key}.solution_steps_uz')
        text(question.get('common_error_uz'), f'{key}.common_error_uz')
        if question['purpose'] == 'practice':
            text(question.get('hint_uz'), f'{key}.hint_uz')
        else:
            require(question.get('hint_uz') is None, f'{key}: checks cannot expose hints.')
        source = question.get('source')
        require(isinstance(source, dict) and source.get('id') in source_ids, f'{key}: unknown source.')
        require(source.get('origin') in {'authored', 'adapted'}, f'{key}: invalid origin.')
        text(source.get('locator'), f'{key}.source.locator')
        answer = question.get('answer_key')
        require(isinstance(answer, dict), f'{key}: answer_key required.')
        if question.get('format') == 'numeric':
            require(question.get('options') == [] and set(answer) == {'value'}, f'{key}: numeric schema.')
            try:
                parse_numeric(answer['value'])
            except ValueError as exc:
                raise ContentValidationError(f'{key}: {exc}') from exc
        elif question.get('format') == 'single':
            options = records(question.get('options'), f'{key}.options')
            ids = []
            for option in options:
                text(option.get('id'), f'{key}.option.id', 64)
                text(option.get('text_uz'), f'{key}.option.text')
                text(option.get('feedback_uz'), f'{key}.option.feedback')
                ids.append(option['id'])
            require(len(ids) >= 2 and len(set(ids)) == len(ids), f'{key}: duplicate or missing options.')
            require(set(answer) == {'option_id'} and answer['option_id'] in ids, f'{key}: invalid option answer.')
        else:
            raise ContentValidationError(f'{key}: schema 1 supports numeric and single formats.')
    for key in skills:
        require(Counter(q['purpose'] for q in exercises.values() if q['skill_key'] == key)
                == {'practice': 2, 'precheck': 1, 'postcheck': 1}, f'{key}: expected 2/1/1 coverage.')

    blueprint = data.get('blueprint')
    require(isinstance(blueprint, dict), 'blueprint required.')
    for purpose in ('precheck', 'practice', 'postcheck'):
        order = blueprint.get(purpose + '_order')
        require(isinstance(order, list) and all(isinstance(key, str) for key in order), f'{purpose}: invalid order.')
        require(len(order) == len(set(order)) and set(order)
                == {key for key, q in exercises.items() if q['purpose'] == purpose}, f'{purpose}: incomplete order.')
    pairs = records(blueprint.get('matched_pairs'), 'matched_pairs')
    require(Counter(pair.get('skill_key') for pair in pairs) == Counter({key: 1 for key in skills}), 'Invalid pair coverage.')
    for pair in pairs:
        for purpose in ('precheck', 'postcheck'):
            question = exercises.get(pair.get(purpose + '_key'))
            require(question is not None and question['purpose'] == purpose
                    and question['skill_key'] == pair['skill_key'] and question['difficulty'] == pair.get('difficulty'),
                    f'{pair["skill_key"]}: invalid matched pair.')
    require(blueprint.get('unseen_postcheck_sets') == 1, 'Pilot contains one postcheck set.')
    text(blueprint.get('comparison_note_uz'), 'blueprint.comparison_note_uz')
    text(blueprint.get('exhaustion_note_uz'), 'blueprint.exhaustion_note_uz')

    links = data.get('diagnostic_links')
    require(isinstance(links, list) and all(isinstance(link, dict) for link in links), 'diagnostic_links must be a list of objects.')
    if not links:
        text(module.get('diagnostic_coverage_note_uz'), 'module.diagnostic_coverage_note_uz')
    seen = set()
    for link in links:
        text(link.get('question_key'), 'diagnostic.question_key', 60)
        strings(link.get('skill_keys'), 'diagnostic.skill_keys')
        require(len(set(link['skill_keys'])) == len(link['skill_keys']) and set(link['skill_keys']) <= skills.keys(),
                'Invalid diagnostic skill references.')
        text(link.get('rationale_uz'), 'diagnostic.rationale_uz')
        for skill in link['skill_keys']:
            identity = (link['question_key'], skill)
            require(identity not in seen, f'Duplicate diagnostic link: {identity}.')
            seen.add(identity)
        if diagnostic_keys is not None:
            require(link['question_key'] in diagnostic_keys, f'Missing diagnostic question: {link["question_key"]}.')
    return data
