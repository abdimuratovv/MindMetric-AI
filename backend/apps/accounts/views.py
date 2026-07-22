from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.i18n import get_language

from .serializers import LoginSerializer, UserSerializer

INVALID_CREDENTIALS = {
    'ru': 'Пожалуйста, введите university-почту и пароль.',
    'uz': 'Iltimos, universitet emailingiz va parolingizni kiriting.',
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
