"""Authorized combined release; prerequisites and bilingual resources are atomic."""
import os

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from apps.development.content_loader import bundled_contents, import_bundle, publish_module
from apps.development.translations import bundled_translation, validate_release_translations
from apps.development.validation import ContentValidationError, require


class Command(BaseCommand):
    help = 'Import and publish reviewed clusters one and two atomically; no accounts or scores.'

    def handle(self, *args, **options):
        if os.environ.get('RENDER') and connection.vendor != 'postgresql':
            raise CommandError('Development release on Render requires persistent PostgreSQL.')
        try:
            with transaction.atomic():
                if connection.vendor == 'postgresql':
                    with connection.cursor() as cursor:
                        # Same lock as cluster one's release; overlapping releases serialize.
                        cursor.execute('SELECT pg_advisory_xact_lock(%s)', [192837465])
                contents = bundled_contents(cluster=None)
                for cluster in (1, 2):
                    members = [d for d in contents if d['module'].get('cluster', 1) == cluster]
                    require(len(members) == 6 and {d['module']['order'] for d in members} == set(range(1, 7)),
                            f'Cluster {cluster} release requires all six reviewed topics.')
                validate_release_translations(contents)
                results = import_bundle(contents)
                for _, module, _ in results:
                    translated = bundled_translation(module.key, module.version)
                    if translated and translated['source_hash'] != module.content_hash:
                        raise CommandError('Translation source differs from the published module.')
                    if module.cluster == 2 and translated is None:
                        raise CommandError('Cluster two requires complete Russian resources.')
                    publish_module(module.pk)
        except (OSError, ContentValidationError, ValidationError) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(
            f'Development release ready: {len(results)} published modules in clusters 1/2; database={connection.vendor}.'
        ))
