"""Transactional draft imports and explicit publication; no diagnostic writes."""

import json
from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.assessments.models import CognitiveQuestion
from .models import (
    DevelopmentExercise, DevelopmentLesson, DevelopmentModule,
    DevelopmentSkill, DiagnosticSkillLink,
)
from .validation import ContentValidationError, content_hash, require, validate_content


BUNDLED_CONTENT = Path(__file__).resolve().parent / 'content' / 'cluster1' / 'arithmetic-algebra.v1.json'


def bundled_contents(cluster=1):
    """One latest reviewed version per course, sorted by curriculum order."""
    latest = {}
    require(cluster is None or (type(cluster) is int and cluster in (1, 2, 3)), 'Invalid bundle cluster.')
    directories = [BUNDLED_CONTENT.parent.parent / f'cluster{number}' for number in ((1, 2, 3) if cluster is None else (cluster,))]
    for path in sorted(path for directory in directories for path in directory.glob('*.v*.json')):
        data = read_content(path)
        meta = data.get('module', {}) if isinstance(data, dict) else {}
        key, version = meta.get('key'), meta.get('version')
        require(isinstance(key, str) and type(version) is int, f'Invalid module metadata: {path.name}.')
        expected_cluster = int(path.parent.name[-1])
        require(meta.get('cluster', 1) == expected_cluster, f'Content stored in wrong cluster: {path.name}.')
        if key not in latest or version > latest[key]['module']['version']:
            latest[key] = data
    require(bool(latest), 'No bundled content found.')
    return sorted(latest.values(), key=lambda data: (data['module'].get('cluster', 1), data['module'].get('order', 0), data['module']['key']))


def validate_localization(data):
    """Schema two is bilingual from its first import; reject partial releases."""
    if data['schema_version'] < 2:
        return
    from .translations import bundled_translation, validate_translation
    translated = bundled_translation(data['module']['key'], data['module']['version'])
    require(translated is not None, 'Cluster two requires a complete Russian translation.')
    validate_translation(data, translated)


def validate_module_cluster(meta):
    require(not DevelopmentModule.objects.filter(key=meta['key']).exclude(cluster=meta.get('cluster', 1)).exists(),
            'A module key cannot move between clusters.')


def known_skill_graph(excluded=()):
    graph = {}
    for skill in DevelopmentSkill.objects.select_related('module').prefetch_related('prerequisites').order_by('-module__version', 'pk'):
        if (skill.module.key, skill.module.version) not in excluded:
            graph.setdefault(skill.key, [parent.key for parent in skill.prerequisites.all()])
    return graph


def read_content(path):
    path = Path(path)
    if path.stat().st_size > 2_000_000:
        raise ContentValidationError('Content file exceeds 2 MB.')
    try:
        return json.loads(path.read_text(encoding='utf-8'), parse_constant=lambda value: _invalid_constant(value))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ContentValidationError(f'Invalid UTF-8 JSON: {exc}') from exc


def _invalid_constant(value):
    raise ContentValidationError(f'Invalid JSON constant: {value}.')


def validate_dependencies(data):
    # Validate structure before reading arbitrary reference fields.
    meta = data.get('module', {}) if isinstance(data, dict) else {}
    if not isinstance(meta, dict):
        meta = {}
    known = known_skill_graph(excluded=[(meta.get('key'), meta.get('version'))])
    validate_content(data, known_skills=known)
    question_keys = {link['question_key'] for link in data['diagnostic_links']}
    questions = {q.key: q for q in CognitiveQuestion.objects.filter(key__in=question_keys)}
    validate_content(data, known_skills=known, diagnostic_keys=questions.keys())
    validate_module_cluster(meta)
    validate_localization(data)
    return questions


@transaction.atomic
def import_bundle(contents, *, dry_run=False):
    """Validate all references before writing, then import prerequisite-first."""
    require(isinstance(contents, list) and bool(contents), 'A nonempty content bundle is required.')
    identities = []
    for data in contents:
        require(isinstance(data, dict) and isinstance(data.get('module'), dict), 'Invalid bundle module.')
        meta = data['module']
        require(isinstance(meta.get('key'), str) and type(meta.get('version')) is int, 'Invalid bundle identity.')
        require(type(meta.get('order')) is int and type(meta.get('cluster', 1)) is int,
                'Invalid bundle cluster/order.')
        identities.append((meta['key'], meta['version']))
    require(len({key for key, _ in identities}) == len(identities), 'Bundle must contain one version per module key.')
    topics = [(data['module'].get('cluster', 1), data['module'].get('order')) for data in contents]
    require(len(set(topics)) == len(topics), 'Duplicate topic order within a cluster.')
    graph = known_skill_graph(excluded=identities)
    owners = {}
    by_key = {data['module']['key']: data for data in contents}
    for data in contents:
        require(isinstance(data.get('skills'), list), 'Bundle skills must be a list.')
        for skill in data['skills']:
            require(isinstance(skill, dict) and isinstance(skill.get('key'), str), 'Invalid bundle skill.')
            require(skill['key'] not in owners, f'Duplicate skill across bundle: {skill["key"]}.')
            owners[skill['key']] = data['module']['key']
            graph[skill['key']] = skill.get('prerequisite_keys', [])
    questions = set(CognitiveQuestion.objects.values_list('key', flat=True))
    for data in contents:
        validate_content(data, known_skills=graph, diagnostic_keys=questions)
        validate_module_cluster(data['module'])
        validate_localization(data)

    ordered, visited, visiting = [], set(), set()

    def visit(key):
        if key in visited:
            return
        require(key not in visiting, f'Module prerequisite cycle: {key}.')
        visiting.add(key)
        for skill in by_key[key]['skills']:
            for parent in skill['prerequisite_keys']:
                owner = owners.get(parent)
                if owner and owner != key:
                    visit(owner)
        visiting.remove(key)
        visited.add(key)
        ordered.append(by_key[key])

    for data in sorted(contents, key=lambda row: (row['module'].get('cluster', 1), row['module']['order'], row['module']['key'])):
        visit(data['module']['key'])

    results = []
    for data in ordered:
        meta = data['module']
        if dry_run:
            module = DevelopmentModule.objects.filter(key=meta['key'], version=meta['version']).first()
            changed = module is None or module.content_hash != content_hash(data)
            require(not (module and module.is_frozen and changed), 'Frozen content differs; increment module.version.')
        else:
            module, changed = import_content(data)
        results.append((data, module, changed))
    return results


@transaction.atomic
def import_content(data, *, dry_run=False):
    questions = validate_dependencies(data)
    meta = data['module']
    digest = content_hash(data)
    module = DevelopmentModule.objects.select_for_update().filter(key=meta['key'], version=meta['version']).first()
    if module and module.is_frozen:
        require(module.content_hash == digest, 'Frozen content differs; increment module.version.')
        return module, False
    if dry_run:
        return module, bool(module is None or module.content_hash != digest)

    # Unique (key, version) resolves simultaneous imports; get_or_create handles
    # the insert race, then the row lock serializes reconciliation.
    module, created = DevelopmentModule.objects.get_or_create(
        key=meta['key'], version=meta['version'],
        defaults={'title_uz': meta['title_uz'], 'content_hash': digest},
    )
    module = DevelopmentModule.objects.select_for_update().get(pk=module.pk)
    if module.is_frozen:
        require(module.content_hash == digest, 'Frozen content differs; increment module.version.')
        return module, False
    changed = created or module.content_hash != digest
    for field in ('order', 'title_uz', 'content_language', 'indicator_keys', 'review_status'):
        setattr(module, field, meta[field])
    module.title_ru = meta.get('title_ru') or ''
    module.cluster = meta.get('cluster', 1)
    module.content_hash = digest
    module.content_snapshot = data
    module.blueprint = data['blueprint']
    module.save()

    skills = {}
    for row in data['skills']:
        skill, _ = DevelopmentSkill.objects.update_or_create(
            module=module, key=row['key'], defaults={'title_uz': row['title_uz'], 'indicator_keys': row['indicator_keys']},
        )
        skills[row['key']] = skill
    for row in data['skills']:
        parents = []
        for key in row['prerequisite_keys']:
            parent = skills.get(key)
            if parent is None:
                parent = DevelopmentSkill.objects.filter(key=key).order_by('-module__version', 'pk').first()
            require(parent is not None, f'Missing prerequisite: {key}.')
            parents.append(parent)
        skills[row['key']].prerequisites.set(parents)

    for order, row in enumerate(data['lessons']):
        DevelopmentLesson.objects.update_or_create(module=module, key=row['key'], defaults={
            'skill': skills[row['skill_key']], 'order': order, 'title_uz': row['title_uz'],
            'theory_uz': row['theory_uz'], 'worked_example_uz': row['worked_example'],
        })
    for row in data['exercises']:
        defaults = {field: row[field] for field in (
            'purpose', 'format', 'difficulty', 'prompt_uz', 'options', 'answer_key',
            'solution_steps_uz', 'hint_uz', 'common_error_uz', 'source',
        )}
        defaults['skill'] = skills[row['skill_key']]
        DevelopmentExercise.objects.update_or_create(module=module, key=row['key'], defaults=defaults)
    expected_links = set()
    for row in data['diagnostic_links']:
        for key in row['skill_keys']:
            link, _ = DiagnosticSkillLink.objects.update_or_create(
                question=questions[row['question_key']], skill=skills[key],
                defaults={'rationale_uz': row['rationale_uz']},
            )
            expected_links.add(link.pk)
    DiagnosticSkillLink.objects.filter(skill__module=module).exclude(pk__in=expected_links).delete()
    module.lessons.exclude(key__in=[row['key'] for row in data['lessons']]).delete()
    module.exercises.exclude(key__in=[row['key'] for row in data['exercises']]).delete()
    obsolete = module.skills.exclude(key__in=skills)
    require(not DevelopmentSkill.objects.filter(prerequisites__in=obsolete).exclude(module=module).exists(),
            'Another module depends on a removed skill; use a new version.')
    obsolete.delete()
    return module, changed


@transaction.atomic
def publish_module(module_id):
    module = DevelopmentModule.objects.select_for_update().get(pk=module_id)
    if module.status == DevelopmentModule.Status.PUBLISHED:
        return module
    if module.is_frozen:
        raise ValidationError('Only a new draft may be published.')
    # Reconcile the validated manifest rather than trusting separately edited rows.
    module, _ = import_content(module.content_snapshot)
    module.status = DevelopmentModule.Status.PUBLISHED
    module.save()
    return module
