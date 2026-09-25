from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email as django_validate_email
from rest_framework import serializers

from apps.i18n import DEFAULT_LANGUAGE

from .models import StudentProfile, User

INVALID_EMAIL_FORMAT = {
    'ru': 'Введите корректный email.',
    'uz': "To‘g‘ri email manzilini kiriting.",
}


class LoginSerializer(serializers.Serializer):
    """Validates the `{{ email }}` / `{{ password }}` fields from the auth screen."""

    # Plain CharField, not EmailField: format errors are raised in validate_email
    # below so they can be localized (this product ships RU/UZ only, no English —
    # see apps/i18n.py), instead of leaking DRF's built-in English message.
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)

    def validate_email(self, value):
        lang = self.context.get('lang', DEFAULT_LANGUAGE)
        value = value.strip()
        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError(INVALID_EMAIL_FORMAT[lang])
        return value


INVALID_EMAIL_DOMAIN = {
    'ru': 'Регистрация доступна только с университетской почтой (@university.edu).',
    'uz': 'Ro‘yxatdan o‘tish faqat universitet emaili (@university.edu) bilan mumkin.',
}
EMAIL_ALREADY_REGISTERED = {
    'ru': 'Аккаунт с этим email уже существует.',
    'uz': 'Bu email bilan akkaunt allaqachon mavjud.',
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
    # Plain CharField, not EmailField: format errors are raised below so they
    # can be localized instead of leaking DRF's built-in English message.
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        lang = self.context.get('lang', DEFAULT_LANGUAGE)
        value = value.strip().lower()
        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError(INVALID_EMAIL_FORMAT[lang])
        domain = value.rsplit('@', 1)[-1]
        if domain != settings.UNIVERSITY_EMAIL_DOMAIN:
            raise serializers.ValidationError(INVALID_EMAIL_DOMAIN[lang])
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(EMAIL_ALREADY_REGISTERED[lang])
        return value

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


STUDENT_PROFILE_FIELDS = ('faculty', 'course', 'group', 'specialization')
PROFILE_FIELD_MAX_LENGTH = 150

PROFILE_ERRORS = {
    'required': {
        'ru': 'Пожалуйста, заполните все поля.',
        'uz': "Iltimos, barcha maydonlarni to'ldiring.",
    },
    'too_long': {
        'ru': f'Значение слишком длинное (не более {PROFILE_FIELD_MAX_LENGTH} символов).',
        'uz': f"Qiymat juda uzun (ko'pi bilan {PROFILE_FIELD_MAX_LENGTH} belgi).",
    },
}


class ProfileUpdateSerializer(serializers.Serializer):
    """
    PATCH /api/accounts/profile/ body. Every field is optional, but one that is
    sent can't be blank. Email is deliberately absent: it is the login, and a
    student's has to stay on UNIVERSITY_EMAIL_DOMAIN, with no mail infra here to
    verify a new address. The student-profile fields are the onboarding-survey
    answers, editable afterwards so a typo'd group doesn't stick forever; the
    view ignores them for non-students.

    Blank/length checks are done in validate() rather than with allow_blank /
    max_length so the errors come out localized, not in DRF's English.
    """

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    faculty = serializers.CharField(required=False, allow_blank=True)
    course = serializers.CharField(required=False, allow_blank=True)
    group = serializers.CharField(required=False, allow_blank=True)
    specialization = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        lang = self.context.get('lang', DEFAULT_LANGUAGE)
        for value in attrs.values():
            if not value:
                raise serializers.ValidationError(PROFILE_ERRORS['required'][lang])
            if len(value) > PROFILE_FIELD_MAX_LENGTH:
                raise serializers.ValidationError(PROFILE_ERRORS['too_long'][lang])
        return attrs


def serialize_profile(user: User) -> dict:
    """GET/PATCH /api/accounts/profile/ response — the settings form's values.
    The survey fields are only present for students."""
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role,
    }
    if user.role == User.Role.STUDENT:
        profile = getattr(user, 'student_profile', None)
        for field in STUDENT_PROFILE_FIELDS:
            data[field] = getattr(profile, field, '') if profile else ''
    return data


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
