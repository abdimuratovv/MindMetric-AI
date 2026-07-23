from rest_framework.permissions import BasePermission

from .models import User


class _HasRole(BasePermission):
    role = None

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == self.role
        )


class IsStudent(_HasRole):
    role = User.Role.STUDENT


class IsAdmin(_HasRole):
    role = User.Role.ADMIN


class HasCompletedProfile(BasePermission):
    """Gate for the test-start endpoints — denies students who haven't
    submitted the one-time onboarding survey yet (StudentProfile.completed_at
    is null). Always paired with IsStudent, so non-students never reach this."""

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        profile = getattr(user, 'student_profile', None)
        return bool(profile and profile.completed_at is not None)
