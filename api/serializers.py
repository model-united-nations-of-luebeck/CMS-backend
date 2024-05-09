from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from api.models import Conference, School, MemberOrganization, Location, Room, Event, Lunch, Plenary, Forum, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, Advisor, Issue, Document, ResearchReport, PositionPaper

# Serializers convert to JSON and validate data passed

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'year', 'startdate', 'enddate', 'annual_session', 'theme', 'pre_registration_deadline', 'final_registration_deadline', 'position_paper_deadline', 'chairhuman', 'vice_chairhuman', 'treasurer', 'vice_treasurer']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'street', 'city', 'zipcode', 'country', 'requested', 'housing_delegates', 'housing_mun_directors', 'registration_status', 'fee', 'arrival', 'departure', 'comment']

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

class EventSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationship
    location = LocationSerializer(allow_null=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'day', 'start_time', 'end_time', 'info', 'location', 'relevance']

class LunchSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationship
    location = LocationSerializer(allow_null=True)

    class Meta:
        model = Lunch
        fields = ['id', 'name', 'day', 'start_time', 'end_time', 'info', 'location']

class PlenarySerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationship
    location = LocationSerializer(allow_null=True)
    lunches = LunchSerializer(many=True, allow_null=True)

    class Meta:
        model = Plenary
        fields = ['id', 'name', 'abbreviation', 'location', 'lunches']

class ForumSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationships
    plenary = PlenarySerializer(allow_null=True)
    room = RoomSerializer(allow_null=True)
    lunches = LunchSerializer(many=True, allow_null=True)

    class Meta:
        model = Forum
        fields = ['id', 'name', 'abbreviation', 'subtitle', 'email', 'room', 'plenary', 'lunches']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'role']

class DelegateSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationships
    represents = MemberOrganizationSerializer(allow_null=True)
    school = SchoolSerializer(allow_null=True)
    forum = ForumSerializer(allow_null=True)

    class Meta:
        model = Delegate
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'ambassador', 'represents', 'school', 'forum']

class StudentOfficerSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationships
    forum = ForumSerializer(allow_null=True)
    plenary = PlenarySerializer(allow_null=True)

    class Meta:
        model = StudentOfficer
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'position_name', 'position_level', 'school_name', 'forum', 'plenary']

class MUNDirectorSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationship
    school = SchoolSerializer(allow_null=True)

    class Meta:
        model = MUNDirector
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'landline_phone', 'english_teacher', 'school']

class ExecutiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executive
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'position_name', 'position_level', 'department_name', 'school_name']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'position_name', 'school_name']

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'mobile', 'diet', 'picture', 'birthday', 'extras', 'car', 'availability', 'experience', 'help']

class IssueSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationship
    forum = ForumSerializer(allow_null=True)

    class Meta:
        model = Issue
        fields = ['id', 'name', 'forum']
       
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'file', 'created', 'author']
       
class ResearchReportSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationship
    issue = IssueSerializer(allow_null=True)

    class Meta:
        model = ResearchReport
        fields = ['id', 'name', 'file', 'created', 'author', 'issue']
                
class PositionPaperSerializer(WritableNestedModelSerializer):
    # Direct Foreign Key Relationship
    delegate = DelegateSerializer(allow_null=True)

    class Meta:
        model = PositionPaper
        fields = ['id', 'name', 'file', 'created', 'author', 'delegate']
                                