from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .content_loader import publish_module
from .models import (
    DevelopmentAnswer, DevelopmentEnrollment, DevelopmentExercise, DevelopmentLesson,
    DevelopmentModule, DevelopmentSession, DevelopmentSkill, DiagnosticSkillLink,
)
from .validation import ContentValidationError


class DevelopmentAdmin(admin.ModelAdmin):
    """Product admins must also be Django staff; content edits go through seed."""

    actions = None

    def has_module_permission(self, request):
        user = request.user
        return bool(user.is_active and user.is_staff and (user.is_superuser or user.role == 'admin'))

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return tuple(field.name for field in self.model._meta.fields) + tuple(
            field.name for field in self.model._meta.many_to_many
        )


@admin.register(DevelopmentModule)
class ModuleAdmin(DevelopmentAdmin):
    list_display = ('key', 'version', 'title_uz', 'status', 'review_status', 'published_at')
    list_filter = ('status', 'content_language')
    search_fields = ('key', 'title_uz')
    actions = ('publish_selected',)

    @admin.action(description='Publish validated drafts', permissions=['publish'])
    def publish_selected(self, request, queryset):
        for module in queryset:
            try:
                publish_module(module.pk)
            except (ContentValidationError, ValidationError) as exc:
                self.message_user(request, f'{module}: {exc}', level=messages.ERROR)
            else:
                self.message_user(request, f'{module}: published.', level=messages.SUCCESS)

    def has_publish_permission(self, request):
        return self.has_module_permission(request)


@admin.register(DevelopmentSkill)
class SkillAdmin(DevelopmentAdmin):
    list_display = ('key', 'module', 'title_uz')
    list_filter = ('module',)


@admin.register(DevelopmentLesson)
class LessonAdmin(DevelopmentAdmin):
    list_display = ('key', 'module', 'skill', 'order')
    list_filter = ('module',)


@admin.register(DevelopmentExercise)
class ExerciseAdmin(DevelopmentAdmin):
    list_display = ('key', 'module', 'skill', 'purpose', 'format', 'difficulty')
    list_filter = ('module', 'purpose', 'format')
    search_fields = ('key', 'prompt_uz')


@admin.register(DiagnosticSkillLink)
class LinkAdmin(DevelopmentAdmin):
    list_display = ('question', 'skill')


@admin.register(DevelopmentEnrollment)
class EnrollmentAdmin(DevelopmentAdmin):
    list_display = ('student', 'module', 'stage', 'started_at')
    list_filter = ('stage',)


@admin.register(DevelopmentSession)
class SessionAdmin(DevelopmentAdmin):
    list_display = ('enrollment', 'purpose', 'number', 'status', 'score')
    list_filter = ('purpose', 'status')


@admin.register(DevelopmentAnswer)
class AnswerAdmin(DevelopmentAdmin):
    list_display = ('session', 'exercise', 'attempt_number', 'correctness', 'hint_used')
