from django.db import models


class InstitutionSettings(models.Model):
    """Singleton row (pk=1) holding what the admin dashboard header shows."""

    name = models.CharField(max_length=160, blank=True)
    academic_term = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name_plural = 'Institution settings'

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
