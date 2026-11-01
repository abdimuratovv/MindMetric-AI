"""Atomically publish all three reviewed clusters, retaining frozen versions."""
import os
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from apps.development.content_loader import bundled_contents, import_bundle, publish_module
from apps.development.translations import validate_release_translations
from apps.development.validation import ContentValidationError, require


class Command(BaseCommand):
    help = 'Import and publish the 16 reviewed bilingual modules atomically; no accounts or scores.'

    def handle(self, *args, **options):
        if os.environ.get('RENDER') and connection.vendor != 'postgresql':
            raise CommandError('Development release on Render requires persistent PostgreSQL.')
        try:
            with transaction.atomic():
                if connection.vendor == 'postgresql':
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT pg_advisory_xact_lock(%s)', [192837465])
                contents = bundled_contents(cluster=None)
                require(len(contents) == 16, 'Combined release requires exactly sixteen reviewed modules.')
                for cluster, count in ((1, 6), (2, 6), (3, 4)):
                    members = [d for d in contents if d['module'].get('cluster', 1) == cluster]
                    require(len(members) == count and {d['module']['order'] for d in members} == set(range(1, count + 1)),
                            f'Cluster {cluster} release requires all {count} reviewed topics.')
                validate_release_translations(contents)
                results = import_bundle(contents)
                for _, module, _ in results:
                    publish_module(module.pk)
        except (OSError, ContentValidationError, ValidationError) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(
            f'Development release ready: {len(results)} published modules in clusters 1/2/3; database={connection.vendor}.'
        ))
