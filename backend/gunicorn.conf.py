"""Optional release hook for platforms without a separate release command."""

import os


def on_starting(server):
    cluster_three = os.environ.get('DEVELOPMENT_CLUSTER3_PUBLISH_ON_DEPLOY') == '1'
    cluster_two = os.environ.get('DEVELOPMENT_CLUSTER2_PUBLISH_ON_DEPLOY') == '1'
    if not cluster_three and not cluster_two and os.environ.get('DEVELOPMENT_CLUSTER1_PUBLISH_ON_DEPLOY') != '1':
        return
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindmetric.settings')
    import django
    django.setup()
    from django.core.management import call_command
    from django.db import connections

    try:
        # Runs once in the master before serving requests; errors fail the new
        # release rather than exposing partially published content.
        command = 'activate_development_cluster3' if cluster_three else ('activate_development_cluster2' if cluster_two else 'activate_development_cluster1')
        call_command(command)
        server.log.info('Development content release completed: clusters %s.', '1/2/3' if cluster_three else ('1/2' if cluster_two else '1'))
    finally:
        # Never inherit the release connection into forked workers.
        connections.close_all()
