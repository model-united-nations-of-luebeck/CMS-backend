from rest_framework.routers import DefaultRouter

from api.views import ConferenceViewSet, SchoolViewSet, MemberOrganizationViewSet, LocationViewSet, RoomViewSet, EventViewSet, LunchViewSet, PlenaryViewSet, ForumViewSet, ParticipantViewSet, DelegateViewSet, StudentOfficerViewSet, MUNDirectorViewSet, ExecutiveViewSet, StaffViewSet, AdvisorViewSet, IssueViewSet, DocumentViewSet, ResearchReportViewSet, PositionPaperViewSet

app_name = 'api'

#add ModelViewSets to urlpatterns
router = DefaultRouter()
router.register('conferences', ConferenceViewSet)
router.register('schools', SchoolViewSet)
router.register('member-organizations', MemberOrganizationViewSet)
router.register('locations', LocationViewSet)
router.register('rooms', RoomViewSet)
router.register('events', EventViewSet)
router.register('lunches', LunchViewSet)
router.register('plenaries', PlenaryViewSet)
router.register('forums', ForumViewSet)
router.register('participants', ParticipantViewSet)
router.register('delegates', DelegateViewSet)
router.register('student-officers', StudentOfficerViewSet)
router.register('mun-directors', MUNDirectorViewSet)
router.register('executives', ExecutiveViewSet)
router.register('staffs', StaffViewSet)
router.register('advisors', AdvisorViewSet)
router.register('issues', IssueViewSet)
router.register('documents', DocumentViewSet)
router.register('research-reports', ResearchReportViewSet)
router.register('position-papers', PositionPaperViewSet)
urlpatterns = router.urls