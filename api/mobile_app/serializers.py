from drf_base64.serializers import ModelSerializer
from rest_framework import serializers

from api.models import Participant


class RequestLoginCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)


class DigitalBadgeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display')
    class Meta:
        model = Participant
        # This should NEVER serialize __all__, app_code or app_code_expires_by
        fields = ['first_name', 'last_name', 'picture', 'birthday', 'role', 'position']


class MigratedParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        # This should NEVER serialize __all__, app_code or app_code_expires_by
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras',
                  'role', 'position']
