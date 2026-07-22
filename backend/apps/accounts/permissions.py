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


class IsTeacher(_HasRole):
    role = User.Role.TEACHER


class IsAdmin(_HasRole):
    role = User.Role.ADMIN
