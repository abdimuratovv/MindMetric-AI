from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from apps.development.content_loader import BUNDLED_CONTENT, bundled_contents, import_bundle, import_content, read_content
from apps.development.validation import ContentValidationError


class Command(BaseCommand):
    help = 'Validate and import development content as draft, without creating accounts or scores.'

    def add_arguments(self, parser):
        parser.add_argument('--path', default=None, help='UTF-8 JSON manifest; defaults to the 1.1 module.')
        parser.add_argument('--all', action='store_true', help='Import all bundled modules atomically, prerequisite-first.')
        parser.add_argument('--cluster', choices=['1', '2', 'all'], default='1', help='Bundle scope for --all; legacy default is cluster one.')
        parser.add_argument('--dry-run', action='store_true', help='Validate content and database references without writes.')

    def handle(self, *args, **options):
        try:
            if options['all'] and options['path']:
                raise CommandError('--all and --path cannot be used together.')
            if options['cluster'] != '1' and not options['all']:
                raise CommandError('--cluster requires --all.')
            if options['all']:
                cluster = None if options['cluster'] == 'all' else int(options['cluster'])
                results = import_bundle(bundled_contents(cluster=cluster), dry_run=options['dry_run'])
            else:
                data = read_content(options['path'] or BUNDLED_CONTENT)
                module, changed = import_content(data, dry_run=options['dry_run'])
                results = [(data, module, changed)]
        except (OSError, ContentValidationError, ValidationError, IntegrityError) as exc:
            raise CommandError(str(exc)) from exc
        for data, module, changed in results:
            action = 'Validated without writes' if options['dry_run'] else ('Imported draft' if changed else 'Content unchanged')
            meta = data['module']
            self.stdout.write(self.style.SUCCESS(
                f'{action}: {meta["key"]} v{meta["version"]}; '
                f'{len(data["skills"])} skills, {len(data["lessons"])} lessons, {len(data["exercises"])} exercises.'
            ))
