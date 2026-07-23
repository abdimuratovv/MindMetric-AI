from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.i18n import DEFAULT_LANGUAGE

from .models import StudentProfile, User


class LoginSerializer(serializers.Serializer):
    """Validates the `{{ email }}` / `{{ password }}` fields from the auth screen."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)


INVALID_EMAIL_DOMAIN = {
    'ru': 'Регистрация доступна только с университетской почтой (@university.edu).',
    'uz': 'Ro‘yxatdan o‘tish faqat universitet emaili (@university.edu) bilan mumkin.',
}
EMAIL_ALREADY_REGISTERED = {
    'ru': 'Аккаунт с этим email уже существует.',
    'uz': 'Bu email bilan akkaunt allaqachon mavjud.',
}
WEAK_PASSWORD = {
    'ru': 'Пароль слишком простой. Используйте не менее 8 символов, избегайте распространённых и полностью цифровых паролей.',
    'uz': 'Parol juda oddiy. Kamida 8 ta belgidan foydalaning, keng tarqalgan yoki faqat raqamlardan iborat parollardan saqlaning.',
}


class RegisterSerializer(serializers.Serializer):
    """
    POST /api/auth/register/ body. Always creates role=STUDENT — there's no
    role field here at all, admin accounts are only ever provisioned via
    seed_assessment_content. Registering does not log the user in (see
    accounts.views.RegisterView); the frontend routes back to the login
    screen on success.
    """

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        lang = self.context.get('lang', DEFAULT_LANGUAGE)
        value = value.strip().lower()
        domain = value.rsplit('@', 1)[-1]
        if domain != settings.UNIVERSITY_EMAIL_DOMAIN:
            raise serializers.ValidationError(INVALID_EMAIL_DOMAIN[lang])
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(EMAIL_ALREADY_REGISTERED[lang])
        return value

    def validate(self, attrs):
        lang = self.context.get('lang', DEFAULT_LANGUAGE)
        # Unsaved instance so UserAttributeSimilarityValidator can compare
        # the password against email/first_name/last_name.
        dummy_user = User(email=attrs['email'], first_name=attrs['first_name'], last_name=attrs['last_name'])
        try:
            validate_password(attrs['password'], user=dummy_user)
        except DjangoValidationError:
            # Django's own validator messages are English-only; this product
            # ships RU/UZ only, so substitute a single localized message
            # instead of leaking them to the client.
            raise serializers.ValidationError(WEAK_PASSWORD[lang])
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=User.Role.STUDENT,
        )


class StudentProfileSerializer(serializers.ModelSerializer):
    """POST /api/accounts/complete-profile/ body. `completed_at` is stamped
    by the view, not this serializer (see accounts.views.CompleteProfileView)."""

    class Meta:
        model = StudentProfile
        fields = ['faculty', 'course', 'group', 'specialization']


class UserSerializer(serializers.ModelSerializer):
    """Feeds {{ userName }} / {{ userInitial }} / {{ role }} in the sidebar."""

    name = serializers.CharField(source='get_full_name', read_only=True)
    initials = serializers.CharField(read_only=True)
    profile_completed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'initials', 'role', 'program', 'profile_completed']

    def get_profile_completed(self, obj):
        if obj.role != User.Role.STUDENT:
            return True
        profile = getattr(obj, 'student_profile', None)
        return bool(profile and profile.completed_at is not None)
