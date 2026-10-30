from django.apps import AppConfig


class DevelopmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.development'
    verbose_name = 'Student development'

    def ready(self):
        from . import signals  # noqa: F401
