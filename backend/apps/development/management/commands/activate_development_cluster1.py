"""Explicit, atomic release operation; never creates accounts or diagnostic scores."""

import os

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from apps.development.content_loader import bundled_contents, import_bundle, publish_module
from apps.development.translations import bundled_translation


class Command(BaseCommand):
    help = 'Import and publish the reviewed cluster-one bundle for an authorized release.'

    def handle(self, *args, **options):
        if os.environ.get('RENDER') and connection.vendor != 'postgresql':
            raise CommandError('Cluster-one release on Render requires persistent PostgreSQL.')
        with transaction.atomic():
            if connection.vendor == 'postgresql':
                # Serialize this release across overlapping Gunicorn masters/instances.
                with connection.cursor() as cursor:
                    cursor.execute('SELECT pg_advisory_xact_lock(%s)', [192837465])
            results = import_bundle(bundled_contents())
            for _, module, _ in results:
                translated=bundled_translation(module.key,module.version)
                if translated and translated['source_hash']!=module.content_hash:
                    raise CommandError('Translation source differs from the published module.')
                publish_module(module.pk)
        self.stdout.write(self.style.SUCCESS(
            f'Cluster-one release ready: {len(results)} published modules; database={connection.vendor}.'
        ))
