"""Optional release hook for platforms without a separate release command."""

import os


def on_starting(server):
    if os.environ.get('DEVELOPMENT_CLUSTER1_PUBLISH_ON_DEPLOY') != '1':
        return
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindmetric.settings')
    import django
    django.setup()
    from django.core.management import call_command
    from django.db import connections

    try:
        # Runs once in the master before serving requests; errors fail the new
        # release rather than exposing partially published content.
        call_command('activate_development_cluster1')
        server.log.info('Cluster-one content release completed.')
    finally:
        # Never inherit the release connection into forked workers.
        connections.close_all()
