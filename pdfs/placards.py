import io
from wsgiref.util import FileWrapper
from django.http import FileResponse

from api.models import Delegate, Executive, Forum, MemberOrganization, StudentOfficer
from api.permissions import IsOrganizer, IsAdmin
from rest_framework.decorators import api_view, permission_classes

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4,A3 

from pdfs.utils import _register_MUNOL_fonts, _get_transparent_background_logo, _get_fitting_font_size, _filter_queryset_by_uuid
_register_MUNOL_fonts()


def _create_placards_file(names: list[str] = [], pagesize=A4):
    logo = _get_transparent_background_logo()
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(pagesize), initialFontName='CenturyGothicBold')
    c.setTitle("Placards")
    c.setAuthor("MUNOL")
    c.setSubject("Placards for MUNOL Conference")
    c.setCreator("MUNOL CMS")
    c.setProducer("MUNOL CMS")
    
    for name in names:
       
        image_size = 265 if pagesize==A4 else 360
        font_height = 20 if pagesize==A4 else 30
        center_margin = 20 if pagesize==A4 else 30
        margin = 50

        c.setFontSize(_get_fitting_font_size(name, 142 if pagesize==A4 else 200, max_width= pagesize[1]))
        
        c.drawImage(logo, pagesize[1]/2 - image_size/2,  center_margin, image_size, image_size, mask='auto')
        c.drawCentredString(pagesize[1]/2, pagesize[0]*1/4 - font_height, name)
        
        
        c.rotate(180)
        
        c.drawImage(logo,-pagesize[1]/2 - image_size/2,-pagesize[0] + center_margin, image_size, image_size, mask='auto')
        c.drawCentredString(-pagesize[1]/2, -pagesize[0]*3/4 - font_height, name)
        
        c.showPage()    

    # Close the PDF object cleanly, and we're done.
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers present the option to save the file.
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='placards.pdf', content_type="application/pdf", as_attachment=False)


def _create_organizers_placards_file(organizers: list = [], pagesize=A4):
    logo = _get_transparent_background_logo()
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(pagesize), initialFontName='CenturyGothicBold')
    c.setTitle("Placards")
    c.setAuthor("MUNOL")
    c.setSubject("Placards for MUNOL Conference")
    c.setCreator("MUNOL CMS")
    c.setProducer("MUNOL CMS")
    for organizer in organizers:
       
        image_size = 100 if pagesize==A4 else 130
        font_height = 20 if pagesize==A4 else 30
        center_margin = 190 if pagesize==A4 else 280
        margin = 50

        name = f"{organizer.first_name.strip()} {organizer.last_name.strip()}"
        position_name = organizer.position_name.strip()
        
        position_font_size = _get_fitting_font_size(position_name, 80 if pagesize==A4 else 100, 'CenturyGothic', max_width=pagesize[1] - margin)
        name_font_size = _get_fitting_font_size(name, 60 if pagesize==A4 else 100, 'CenturyGothic', max_width=pagesize[1] - margin)
        
        c.drawImage(logo, pagesize[1]/2 - image_size/2,  center_margin, image_size, image_size, mask='auto')
        
        c.setFont('CenturyGothic', name_font_size)
        c.drawCentredString(pagesize[1]/2, pagesize[0]*1/10 - font_height, name)
        
        c.setFont('CenturyGothicBold', position_font_size)
        c.drawCentredString(pagesize[1]/2, pagesize[0]*2/8 - font_height, position_name)

        c.rotate(180)
        
        c.drawImage(logo,-pagesize[1]/2 - image_size/2,-pagesize[0] + center_margin, image_size, image_size, mask='auto')
        
        c.setFont('CenturyGothic', name_font_size)
        c.drawCentredString(-pagesize[1]/2, -pagesize[0]*9/10 - font_height, name)
        
        c.setFont('CenturyGothicBold', position_font_size)
        c.drawCentredString(-pagesize[1]/2, -pagesize[0]*6/8 - font_height, position_name)
        

        c.showPage()    

    # Close the PDF object cleanly, and we're done.
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers present the option to save the file.
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='placards.pdf', content_type="application/pdf", as_attachment=False)

def _get_page_size_from_request(request):
    if request.GET is not None and 'pagesize' in request.GET:
        return A3 if request.GET['pagesize'] == 'A3' else A4
    return A4

@api_view(["GET"])
@permission_classes([IsOrganizer|IsAdmin])
def executive_placards(request):
    queryset = Executive.objects
    executives = _filter_queryset_by_uuid(queryset, request)
    executives = executives.order_by('position_name')
    
    return _create_organizers_placards_file(executives, _get_page_size_from_request(request))

@api_view(["GET"])
@permission_classes([IsOrganizer|IsAdmin])
def student_officer_placards(request):

    queryset = StudentOfficer.objects
    student_officers = _filter_queryset_by_uuid(queryset, request)
    student_officers = student_officers.order_by('forum__id')

    return _create_organizers_placards_file(student_officers, _get_page_size_from_request(request))

@api_view(["GET"])
@permission_classes([IsOrganizer|IsAdmin])
def delegate_placards_forum(request):
    
    voting_rights = request.GET.get('voting_rights', 'vote')
    if voting_rights == 'vote':
        voting_statuses = [MemberOrganization.MEMBER_STATE, MemberOrganization.FORMER_MEMBER]
    elif voting_rights == 'novote':
        voting_statuses = [MemberOrganization.OBSERVER_STATE, MemberOrganization.NON_GOVERNMENTAL_ORGANIZATION, MemberOrganization.INTER_GOVERNMENTAL_ORGANIZATION, MemberOrganization.UN_SUB_BODY]
    
    forum_divider = request.GET.get('forum_divider', 'false').lower() == 'true'

    forum_ids = request.GET.get('forum_ids', [])
    forum_ids = forum_ids.split(",")
    forum_ids = list(map(int, forum_ids)) #cast to ints
    forums = Forum.objects.filter(id__in=forum_ids)

    names = []
    for forum in forums:

        if forum_divider:
            names += [f"*** {forum.abbreviation} ***"]
        delegates_in_forum_filtered_by_voting_rights = Delegate.objects.filter(forum=forum, represents__status__in=voting_statuses)
        delegates_in_forum_filtered_by_voting_rights = delegates_in_forum_filtered_by_voting_rights.order_by('represents__official_name')
        for delegate in delegates_in_forum_filtered_by_voting_rights:
            names += [delegate.represents.placard_name]
           
    return _create_placards_file(names = names, pagesize= _get_page_size_from_request(request))

@api_view(["GET"])
@permission_classes([IsOrganizer|IsAdmin])
def delegate_placards_plenary(request):
    
    voting_rights = request.GET.get('voting_rights', 'vote')
    if voting_rights == 'vote':
        voting_statuses = [MemberOrganization.MEMBER_STATE, MemberOrganization.FORMER_MEMBER]
    elif voting_rights == 'novote':
        voting_statuses = [MemberOrganization.OBSERVER_STATE, MemberOrganization.NON_GOVERNMENTAL_ORGANIZATION, MemberOrganization.INTER_GOVERNMENTAL_ORGANIZATION, MemberOrganization.UN_SUB_BODY]
    
    plenary_ids = request.GET.get('plenary_ids', [])
    plenary_ids = plenary_ids.split(",")
    plenary_ids = list(map(int, plenary_ids)) #cast to ints
    
    names = []
    for plenary_id in plenary_ids:
        forums_in_plenary = Forum.objects.filter(plenary=plenary_id)
        delegates_in_plenary_filtered_by_voting_rights = Delegate.objects.filter(forum__in=forums_in_plenary, represents__status__in=voting_statuses)
        member_organizations_in_plenary = MemberOrganization.objects.filter(id__in=delegates_in_plenary_filtered_by_voting_rights.values('represents_id')).distinct()
        for member in member_organizations_in_plenary:
            names += [member.placard_name]
           
    return _create_placards_file(names = names, pagesize= _get_page_size_from_request(request))

@api_view(["GET"])
@permission_classes([IsOrganizer|IsAdmin])
def delegate_placards_ceremony(request):
    
    
    names = []
    delegates = Delegate.objects.all()
    member_organizations_represented = MemberOrganization.objects.filter(id__in=delegates.values('represents_id')).distinct()
    member_organizations_represented = member_organizations_represented.order_by('official_name')
    for member in member_organizations_represented:
        names += [member.placard_name]
           
    return _create_placards_file(names = names, pagesize= _get_page_size_from_request(request))

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def custom_placard(request):
    page_size = A4 if request.data.get('page_size') == 'A4' else A3
    name = request.data.get('name', '')
    position = request.data.get('position', '')
    if position == '':
        return _create_placards_file(names=[name], pagesize=page_size)
    else:
        class CustomOrganizer:
            def __init__(self, name, position):
                self.first_name = name
                self.last_name = ''
                self.position_name = position

        custom_organizer = CustomOrganizer(name, position)
        return _create_organizers_placards_file(organizers=[custom_organizer], pagesize=page_size)
