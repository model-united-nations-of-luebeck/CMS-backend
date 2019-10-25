from django.shortcuts import render
from rest_framework import generics # generic views for RUD, LC views
from api.permissions import MUNOLDjangoModelPermission

from api.serializers import ConferenceSerializer, SchoolSerializer, MemberOrganizationSerializer, LocationSerializer, RoomSerializer, EventSerializer, LunchSerializer, PlenarySerializer, ForumSerializer, ParticipantSerializer, DelegateSerializer, StudentOfficerSerializer, MUNDirectorSerializer, ExecutiveSerializer, StaffSerializer, AdvisorSerializer, IssueSerializer, DocumentSerializer, ResearchReportSerializer, PositionPaperSerializer
from api.models import Conference, School, MemberOrganization, Location, Room, Event, Lunch, Plenary, Forum, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, Advisor, Issue, Document, ResearchReport, PositionPaper

#For single conferences
class ConferenceRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ConferenceSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Conference.objects.all()

#For creating and showing all conferences
class ConferenceLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = ConferenceSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Conference.objects.all()        


class SchoolRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = SchoolSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return School.objects.all()

class SchoolLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = SchoolSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return School.objects.all() 


class MemberOrganizationRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = MemberOrganizationSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return MemberOrganization.objects.all()

class MemberOrganizationLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = MemberOrganizationSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return MemberOrganization.objects.all() 

class LocationRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = LocationSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Location.objects.all()

class LocationLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = LocationSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Location.objects.all()  

        
class RoomRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = RoomSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Room.objects.all()

class RoomLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = RoomSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Room.objects.all()  

class EventRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = EventSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Event.objects.all()

class EventLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = EventSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Event.objects.all()       

class LunchRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = LunchSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Lunch.objects.all()

class LunchLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = LunchSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Lunch.objects.all() 

class PlenaryRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PlenarySerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Plenary.objects.all()

class PlenaryLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = PlenarySerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Plenary.objects.all()  

class ForumRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ForumSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Forum.objects.all()

class ForumLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = ForumSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Forum.objects.all()  

class ParticipantRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ParticipantSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Participant.objects.all()

class ParticipantLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = ParticipantSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Participant.objects.all()                                                 

class DelegateRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = DelegateSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Delegate.objects.all()

class DelegateLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = DelegateSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Delegate.objects.all()  

class StudentOfficerRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = StudentOfficerSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return StudentOfficer.objects.all()

class StudentOfficerLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = StudentOfficerSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return StudentOfficer.objects.all()                                                                 

class MUNDirectorRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = MUNDirectorSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return MUNDirector.objects.all()

class MUNDirectorLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = MUNDirectorSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return MUNDirector.objects.all()   

class ExecutiveRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ExecutiveSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Executive.objects.all()

class ExecutiveLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = ExecutiveSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Executive.objects.all() 

class StaffRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = StaffSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Staff.objects.all()

class StaffLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = StaffSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Staff.objects.all()                                                                                         

class AdvisorRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = AdvisorSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Advisor.objects.all()

class AdvisorLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = AdvisorSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Advisor.objects.all()   

class IssueRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = IssueSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Issue.objects.all()

class IssueLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = IssueSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Issue.objects.all()  

class DocumentRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = DocumentSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Document.objects.all()

class DocumentLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = DocumentSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return Document.objects.all()   

class ResearchReportRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ResearchReportSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return ResearchReport.objects.all()

class ResearchReportLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = ResearchReportSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return ResearchReport.objects.all()                                                                                                                         
class PositionPaperRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PositionPaperSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return PositionPaper.objects.all()

class PositionPaperLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = PositionPaperSerializer
    permission_classes = (MUNOLDjangoModelPermission,)

    def get_queryset(self):
        return PositionPaper.objects.all()                                                                                                                                 