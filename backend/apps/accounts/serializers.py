from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):
    """Validates the `{{ email }}` / `{{ password }}` fields from the auth screen."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)


class UserSerializer(serializers.ModelSerializer):
    """Feeds {{ userName }} / {{ userInitial }} / {{ role }} in the sidebar."""

    name = serializers.CharField(source='get_full_name', read_only=True)
    initials = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'initials', 'role', 'program']
