from django.conf import settings
from rest_framework.permissions import BasePermission

from apps.accounts.permissions import HasCompletedProfile, IsStudent
from .models import DevelopmentAnswer, DevelopmentEnrollment, DevelopmentSession


class IsDevelopmentEnabled(BasePermission):
    def has_permission(self, request, view):
        return settings.DEVELOPMENT_CLUSTER1_ENABLED


class IsDevelopmentOwner(BasePermission):
    """Use with an owner-filtered queryset: lists do not run object permissions."""

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, DevelopmentAnswer):
            obj = obj.session
        if isinstance(obj, DevelopmentSession):
            obj = obj.enrollment
        return isinstance(obj, DevelopmentEnrollment) and obj.student_id == request.user.pk


STUDENT_PERMISSIONS = (IsStudent, HasCompletedProfile, IsDevelopmentEnabled, IsDevelopmentOwner)
