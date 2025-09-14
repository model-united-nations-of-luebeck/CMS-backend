from rest_framework import serializers
from drf_base64.serializers import ModelSerializer as Base64ModelSerializer
from django.contrib.auth.models import User
from api.models import Conference, School, MemberOrganization, Location, Room, Event, Lunch, Plenary, Forum, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, Advisor, Issue, Document, ResearchReport, PositionPaper
from django.core.mail import send_mail
from django.urls import reverse

# Serializers convert to JSON and validate data passed

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'year', 'start_date', 'end_date', 'annual_session', 'theme', 'pre_registration_deadline', 'final_registration_deadline', 'position_paper_deadline', 'chair_human', 'vice_chair_human', 'treasurer', 'vice_treasurer']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'street', 'city', 'zipcode', 'country', 'requested', 'housing_delegates', 'housing_mun_directors', 'registration_status', 'fee_paid', 'arrival', 'departure', 'comment']

class SchoolRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = School
        fields = ['username', 'password', 'name']  # include your school fields

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, password=password)
        school = School.objects.create(user=user, **validated_data)
        return school


class MemberOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberOrganization
        fields = ['id', 'name', 'official_name', 'placard_name', 'status', 'active', 'flag'] 

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude', 'zoom_level', 'address']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'latitude', 'longitude', 'zoom_level', 'address', 'room_number', 'floor']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'day', 'start_time', 'end_time', 'info', 'location', 'relevance']

class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = ['id', 'name', 'day', 'start_time', 'end_time', 'info', 'location']

class PlenarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Plenary
        fields = ['id', 'name', 'abbreviation', 'location', 'lunches']

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'name', 'abbreviation', 'subtitle', 'email', 'room', 'plenary', 'lunches']

class ParticipantSerializer(Base64ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'picture', 'birthday', 'extras', 'role', 'data_consent_time', 'data_consent_ip', 'media_consent_time', 'media_consent_ip']

    def update(self, instance, validated_data):
        old_email = instance.email
        new_email = validated_data.get('email', old_email)

        # Do actual update
        instance = super().update(instance, validated_data)

        # If email changes, send a confirmation email
        if new_email and new_email != old_email:
            request = self.context.get('request')
            if request:
                edit_url = request.build_absolute_uri(reverse("participant_update", args=[instance.pk]))
            send_mail(
                "Thank yo for registering",
                f"Your registration worked! You can update it here: {edit_url}",
                "noreply@munol.org",
                [new_email],
            )
        return instance

class DelegateSerializer(Base64ModelSerializer):
    class Meta:
        model = Delegate
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'picture', 'birthday', 'extras', 'data_consent_time', 'data_consent_ip', 'media_consent_time', 'media_consent_ip', 'ambassador', 'first_timer', 'represents', 'school', 'forum']

class StudentOfficerSerializer(Base64ModelSerializer):
    class Meta:
        model = StudentOfficer
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'picture', 'birthday', 'extras', 'data_consent_time', 'data_consent_ip', 'media_consent_time', 'media_consent_ip', 'position_name', 'school_name', 'forum', 'plenary']

class MUNDirectorSerializer(Base64ModelSerializer):
    class Meta:
        model = MUNDirector
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'picture', 'birthday', 'extras', 'data_consent_time', 'data_consent_ip', 'media_consent_time', 'media_consent_ip', 'english_teacher', 'school']

class ExecutiveSerializer(Base64ModelSerializer):
    class Meta:
        model = Executive
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'picture', 'birthday', 'extras', 'data_consent_time', 'data_consent_ip', 'media_consent_time', 'media_consent_ip', 'position_name', 'school_name']

class StaffSerializer(Base64ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'picture', 'birthday', 'extras', 'data_consent_time', 'data_consent_ip', 'media_consent_time', 'media_consent_ip', 'position_name', 'school_name']

class AdvisorSerializer(Base64ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'picture', 'birthday', 'extras', 'data_consent_time', 'data_consent_ip', 'media_consent_time', 'media_consent_ip', 'car', 'availability', 'experience', 'help']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'name', 'forum']
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'file', 'created', 'author']
        
class ResearchReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchReport
        fields = ['id', 'name', 'file', 'created', 'author', 'issue']
                
class PositionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionPaper
        fields = ['id', 'name', 'file', 'created', 'author', 'delegate']
                                