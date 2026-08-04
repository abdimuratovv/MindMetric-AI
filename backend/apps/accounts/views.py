from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.i18n import get_language

from .models import StudentProfile
from .permissions import IsStudent
from .serializers import LoginSerializer, RegisterSerializer, StudentProfileSerializer, UserSerializer

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
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
