from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver

from .models import (
    DevelopmentExercise, DevelopmentLesson, DevelopmentModule,
    DevelopmentSkill, DiagnosticSkillLink,
)


@receiver(pre_delete, sender=DevelopmentModule)
@receiver(pre_delete, sender=DevelopmentSkill)
@receiver(pre_delete, sender=DevelopmentLesson)
@receiver(pre_delete, sender=DevelopmentExercise)
@receiver(pre_delete, sender=DiagnosticSkillLink)
def protect_frozen_content(sender, instance, **kwargs):
    module_id = instance.pk if sender is DevelopmentModule else instance.content_module().pk
    if DevelopmentModule.objects.get(pk=module_id).is_frozen:
        raise ValidationError('Published or enrolled content cannot be deleted.')


@receiver(m2m_changed, sender=DevelopmentSkill.prerequisites.through)
def protect_prerequisites(sender, instance, action, reverse, pk_set, **kwargs):
    if action not in {'pre_add', 'pre_remove', 'pre_clear'}:
        return
    if reverse:
        dependents = instance.dependents.all() if pk_set is None else DevelopmentSkill.objects.filter(pk__in=pk_set)
    else:
        dependents = [instance]
    for dependent in dependents:
        if DevelopmentModule.objects.get(pk=dependent.module_id).is_frozen:
            raise ValidationError('Frozen prerequisites cannot be edited.')
    if action == 'pre_add':
        edges = ((key, instance.pk) for key in pk_set) if reverse else ((instance.pk, key) for key in pk_set)
        for dependent_id, parent_id in edges:
            visited = set()
            remaining = {parent_id}
            while remaining:
                current = remaining.pop()
                if current == dependent_id:
                    raise ValidationError('Prerequisites cannot contain cycles.')
                if current not in visited:
                    visited.add(current)
                    remaining.update(DevelopmentSkill.objects.get(pk=current).prerequisites.values_list('pk', flat=True))
