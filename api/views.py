from django.shortcuts import render
from rest_framework import viewsets # viewsets for ModelViewSets
from api.permissions import MUNOLDjangoModelPermission, MUNOLDjangoModelPermissionsOrAnonReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.serializers import SchoolRegistrationSerializer

from api.serializers import ConferenceSerializer, SchoolSerializer, MemberOrganizationSerializer, LocationSerializer, RoomSerializer, EventSerializer, LunchSerializer, PlenarySerializer, ForumSerializer, ParticipantSerializer, DelegateSerializer, StudentOfficerSerializer, MUNDirectorSerializer, ExecutiveSerializer, StaffSerializer, AdvisorSerializer, IssueSerializer, DocumentSerializer, ResearchReportSerializer, PositionPaperSerializer
from api.models import Conference, School, MemberOrganization, Location, Room, Event, Lunch, Plenary, Forum, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, Advisor, Issue, Document, ResearchReport, PositionPaper

class GenericMUNOLViewSet(viewsets.ModelViewSet):
    permission_classes = (MUNOLDjangoModelPermission,)
    
class ConferenceViewSet(GenericMUNOLViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    permission_classes = (MUNOLDjangoModelPermissionsOrAnonReadOnly,)
    
class SchoolViewSet(GenericMUNOLViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class MemberOrganizationViewSet(GenericMUNOLViewSet):
    queryset = MemberOrganization.objects.all()
    serializer_class = MemberOrganizationSerializer

class LocationViewSet(GenericMUNOLViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class RoomViewSet(GenericMUNOLViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class EventViewSet(GenericMUNOLViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class LunchViewSet(GenericMUNOLViewSet):
    queryset = Lunch.objects.all()
    serializer_class = LunchSerializer

class PlenaryViewSet(GenericMUNOLViewSet):
    queryset = Plenary.objects.all()
    serializer_class = PlenarySerializer

class ForumViewSet(GenericMUNOLViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

class ParticipantViewSet(GenericMUNOLViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class DelegateViewSet(GenericMUNOLViewSet):
    queryset = Delegate.objects.all()
    serializer_class = DelegateSerializer

class StudentOfficerViewSet(GenericMUNOLViewSet):
    queryset = StudentOfficer.objects.all()
    serializer_class = StudentOfficerSerializer

class MUNDirectorViewSet(GenericMUNOLViewSet):
    queryset = MUNDirector.objects.all()
    serializer_class = MUNDirectorSerializer

class ExecutiveViewSet(GenericMUNOLViewSet):
    queryset = Executive.objects.all()
    serializer_class = ExecutiveSerializer

class StaffViewSet(GenericMUNOLViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class AdvisorViewSet(GenericMUNOLViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer

class IssueViewSet(GenericMUNOLViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (MUNOLDjangoModelPermissionsOrAnonReadOnly,)

class DocumentViewSet(GenericMUNOLViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class ResearchReportViewSet(GenericMUNOLViewSet):
    queryset = ResearchReport.objects.all()
    serializer_class = ResearchReportSerializer

class PositionPaperViewSet(GenericMUNOLViewSet):
    queryset = PositionPaper.objects.all()
    serializer_class = PositionPaperSerializer                  


class MUNOLObtainAuthToken(ObtainAuthToken):
    """
    Custom authentication view to return additional user information
    along with the token, e.g. school_id or participant_id.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user

        if hasattr(user, 'school') and user.school is not None:
            return Response({
                'token': token.key,
                'school_id': getattr(user.school, 'id', None),
            })
        elif hasattr(user, 'participant') and user.participant is not None:
            return Response({
                'token': token.key,
                'participant_id': getattr(user.participant, 'id', None),
            })
        else:
            return Response({
                'token': token.key,
            })
        
class SchoolRegisterView(APIView):
    def post(self, request):
        serializer = SchoolRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            school = serializer.save()
            return Response({'school_id': school.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)