from rest_framework import serializers
from api.models import Conference, School, MemberOrganization, Location, Room, Event, Lunch, Plenary, Forum, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, Advisor, Issue, Document, ResearchReport, PositionPaper

# Serializers convert to JSON and validate data passed

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'year', 'start_date', 'end_date', 'annual_session', 'theme', 'pre_registration_deadline', 'final_registration_deadline', 'position_paper_deadline', 'chair_human', 'vice_chair_human', 'treasurer', 'vice_treasurer']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'street', 'city', 'zipcode', 'country', 'requested', 'housing_delegates', 'housing_mun_directors', 'registration_status', 'fee_paid', 'arrival', 'departure', 'comment']

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

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'role', 'data_consent_time', 'data_consent_ip', 'media_consent_time', 'media_consent_ip']

class DelegateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delegate
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'ambassador', 'first_timer', 'represents', 'school', 'forum']

class StudentOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOfficer
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'position_name', 'school_name', 'forum', 'plenary']

class MUNDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MUNDirector
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'landline_phone', 'english_teacher', 'school']

class ExecutiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executive
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'position_name', 'school_name']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'position_name', 'school_name']

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['id', 'first_name', 'last_name', 'gender', 'pronouns', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'car', 'availability', 'experience', 'help']

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
                                