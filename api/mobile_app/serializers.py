from rest_framework import serializers

from api.models import Participant


class RequestLoginCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)


class VerifySerializer(serializers.Serializer):
    token = serializers.CharField()


class LoginProblemSerializer(serializers.Serializer):
    email = serializers.EmailField()


class DigitalBadgeSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = ["first_name", "last_name", "picture", "birthday", "role", "position"]

    def get_position(self, obj: Participant):
        match obj.role:
            case "executive":
                return obj.executive.position_name
            case "delegate":
                return f"{obj.delegate.represents.name} in {obj.delegate.forum.abbreviation}"
            case "student officer":
                return obj.studentofficer.position_name
            case "staff":
                return obj.staff.position_name
            case _:
                return ""
