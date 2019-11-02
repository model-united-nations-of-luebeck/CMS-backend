from django.shortcuts import render
from rest_framework import generics, viewsets # generic views for RUD, LC views; viewsets for ModelViewSets
from api.permissions import MUNOLDjangoModelPermission, MUNOLDjangoModelPermissionsOrAnonReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from api.serializers import ConferenceSerializer, SchoolSerializer, MemberOrganizationSerializer, LocationSerializer, RoomSerializer, EventSerializer, LunchSerializer, PlenarySerializer, ForumSerializer, ParticipantSerializer, DelegateSerializer, StudentOfficerSerializer, MUNDirectorSerializer, ExecutiveSerializer, StaffSerializer, AdvisorSerializer, IssueSerializer, DocumentSerializer, ResearchReportSerializer, PositionPaperSerializer
from api.models import Conference, School, MemberOrganization, Location, Room, Event, Lunch, Plenary, Forum, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, Advisor, Issue, Document, ResearchReport, PositionPaper

class GenericMUNOLViewSet(viewsets.ModelViewSet):
    permission_classes = (MUNOLDjangoModelPermission,)
    
class ConferenceViewSet(GenericMUNOLViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    
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

class DocumentViewSet(GenericMUNOLViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class ResearchReportViewSet(GenericMUNOLViewSet):
    queryset = ResearchReport.objects.all()
    serializer_class = ResearchReportSerializer

class PositionPaperViewSet(GenericMUNOLViewSet):
    queryset = PositionPaper.objects.all()
    serializer_class = PositionPaperSerializer                  