import math

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import Throttled
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.i18n import get_language

from .models import StudentProfile, User
from .permissions import IsStudent
from .serializers import (
    STUDENT_PROFILE_FIELDS, LoginSerializer, ProfileUpdateSerializer, RegisterSerializer, StudentProfileSerializer,
    UserSerializer, serialize_profile,
)

INVALID_CREDENTIALS = {
    'ru': 'Неверный email или пароль.',
    'uz': 'Email yoki parol noto‘g‘ri.',
}
NO_ACCOUNT_FOR_ROLE = {
    'ru': {'student': 'студента', 'teacher': 'преподавателя', 'admin': 'администратора'},
    'uz': {'student': 'talaba', 'teacher': "o'qituvchi", 'admin': 'administrator'},
}
NO_ACCOUNT_MESSAGE = {
    'ru': 'Аккаунт {role} с этим email не найден.',
    'uz': 'Ushbu email uchun {role} akkaunti topilmadi.',
}


class LoginView(APIView):
    """
    POST /api/auth/login/  {email, password, role}

    Backs auth.dc.html's `doLogin`. On success returns a JWT plus the {role, user}
    payload App.jsx uses to route to the correct shell (student → selection,
    teacher → teacherReview, admin → admin), same branch as the mockup's
    `goTo(role === 'student' ? 'selection' : ...)`.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        lang = get_language(request)
        serializer = LoginSerializer(data=request.data, context={'lang': lang})
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({'detail': str(first_error)}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        user = authenticate(request, email=data['email'], password=data['password'])
        if user is None:
            # Mirrors {{ loginError }}.
            return Response(
                {'detail': INVALID_CREDENTIALS[lang]},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if user.role != data['role']:
            role_word = NO_ACCOUNT_FOR_ROLE[lang][data['role']]
            return Response(
                {'detail': NO_ACCOUNT_MESSAGE[lang].format(role=role_word)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        })


class RegisterView(APIView):
    """
    POST /api/auth/register/  {first_name, last_name, email, password}

    Creates a role=STUDENT account only. Does NOT log the user in and
    returns no tokens — the frontend sends them back to the login screen
    to sign in with the credentials they just created.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        lang = get_language(request)
        serializer = RegisterSerializer(data=request.data, context={'lang': lang})
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({'detail': str(first_error)}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response({'email': user.email}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """POST /api/auth/logout/ — blacklists the refresh token; mirrors the sidebar's `logout`."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            RefreshToken(request.data.get('refresh')).blacklist()
        except Exception:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(RetrieveAPIView):
    """GET /api/accounts/me/ — hydrates {{ userName }}/{{ userInitial }}/{{ role }}."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CompleteProfileView(APIView):
    """
    POST /api/accounts/complete-profile/  {faculty, course, group, specialization}

    One-time onboarding-survey submission. Creates or updates the caller's
    StudentProfile and stamps completed_at, which is what
    HasCompletedProfile / UserSerializer.profile_completed key off of.
    """

    permission_classes = [IsStudent]

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        serializer = StudentProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(completed_at=timezone.now())
        return Response(UserSerializer(request.user).data)


class ProfileView(APIView):
    """
    GET   /api/accounts/profile/ — the profile-settings form's values.
    PATCH /api/accounts/profile/  {first_name?, last_name?, faculty?, course?, group?, specialization?}

    Any role edits their own name; students also their onboarding-survey
    answers. Returns the refreshed form values plus the UserSerializer payload,
    so the sidebar's name/initials update without a second request.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(serialize_profile(request.user))

    def patch(self, request):
        lang = get_language(request)
        serializer = ProfileUpdateSerializer(data=request.data, context={'lang': lang})
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({'detail': str(first_error)}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        user = request.user

        user_fields = [f for f in ('first_name', 'last_name') if f in data]
        for field in user_fields:
            setattr(user, field, data[field])
        if user_fields:
            user.save(update_fields=user_fields)

        profile_fields = [f for f in STUDENT_PROFILE_FIELDS if f in data]
        if user.role == User.Role.STUDENT and profile_fields:
            # completed_at is left alone: editing answers isn't submitting the
            # survey, which stays the only thing that unlocks the tests.
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            for field in profile_fields:
                setattr(profile, field, data[field])
            profile.save(update_fields=profile_fields)
            user.student_profile = profile

        return Response({'profile': serialize_profile(user), 'user': UserSerializer(user).data})


PASSWORD_ERRORS = {
    'required': {
        'ru': 'Введите текущий и новый пароль.',
        'uz': 'Joriy va yangi parolni kiriting.',
    },
    'wrong_current': {
        'ru': 'Текущий пароль указан неверно.',
        'uz': "Joriy parol noto'g'ri.",
    },
    'same': {
        'ru': 'Новый пароль совпадает с текущим.',
        'uz': 'Yangi parol joriy parol bilan bir xil.',
    },
    'throttled': {
        'ru': 'Слишком много попыток смены пароля. Попробуйте снова через {minutes} мин.',
        'uz': "Parolni o'zgartirishga urinishlar juda ko'p. {minutes} daqiqadan so'ng qayta urinib ko'ring.",
    },
}


def _revoke_other_sessions(user, also_update=()) -> dict:
    """Invalidates every token issued so far (see accounts.authentication) and
    returns a fresh pair for the session that asked, which stays signed in.
    `also_update` saves other changed fields in the same write, so a new
    password can never land without the revocation that goes with it."""
    user.tokens_valid_after = timezone.now()
    user.save(update_fields=['tokens_valid_after', *also_update])
    refresh = RefreshToken.for_user(user)
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}


class ChangePasswordView(APIView):
    """
    POST /api/accounts/change-password/  {current_password, new_password}

    Requires the current password, so a session left open on a shared computer
    can't be used to take the account over. Any non-empty new password is
    accepted, same rule as registration (see settings.AUTH_PASSWORD_VALIDATORS).
    Signs out every other session and returns a new token for this one.
    Throttled per user: the current-password check must not become a way to
    guess it.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'password-change'

    def throttled(self, request, wait):
        # Throttled's own detail appends an English "Expected available in N
        # seconds", so the message is replaced after construction — which still
        # keeps `wait` for the Retry-After header.
        exc = Throttled(wait)
        minutes = max(1, math.ceil(wait / 60)) if wait else 60
        exc.detail = PASSWORD_ERRORS['throttled'][get_language(request)].format(minutes=minutes)
        raise exc

    def post(self, request):
        lang = get_language(request)
        current = request.data.get('current_password')
        new = request.data.get('new_password')
        if not isinstance(current, str) or not isinstance(new, str) or not current or not new.strip():
            return Response({'detail': PASSWORD_ERRORS['required'][lang]}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(current):
            return Response({'detail': PASSWORD_ERRORS['wrong_current'][lang]}, status=status.HTTP_400_BAD_REQUEST)
        if new == current:
            return Response({'detail': PASSWORD_ERRORS['same'][lang]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new)
        return Response(_revoke_other_sessions(user, also_update=['password']))


class SignOutEverywhereView(APIView):
    """POST /api/accounts/sign-out-everywhere/ — ends every other session of this
    account (a forgotten login on a lab computer, say) and keeps this one."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(_revoke_other_sessions(request.user))
