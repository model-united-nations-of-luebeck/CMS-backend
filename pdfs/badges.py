import io
import os
import textwrap

from wsgiref.util import FileWrapper
from django.http import FileResponse

from api.models import Advisor, Conference, Delegate, Executive, MUNDirector, Staff, StudentOfficer
from api.permissions import IsOrganizer, IsAdmin
from rest_framework.decorators import api_view, permission_classes

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from django.conf import settings

from pdfs.utils import _register_MUNOL_fonts, _get_transparent_background_logo, _filter_queryset_by_uuid
_register_MUNOL_fonts()

#determine year of current conference
year = Conference.objects.first().start_date.year


ROLE_TO_COLOR = {
    Advisor: (0, 1, 195/255),
    MUNDirector: (16/255,1,0),
    Executive: (1,0,0),
    StudentOfficer: (0,140/255,1),
    Staff: (188/255, 225/255, 1),
    Delegate: (1, 144/255, 0)
}

BADGE_WIDTH = 85 * mm
BADGE_HEIGHT = 55 * mm

COLUMNS = 2
ROWS = 4

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = (PAGE_WIDTH - COLUMNS * BADGE_WIDTH) / 2
MARGIN_Y = (PAGE_HEIGHT - ROWS * BADGE_HEIGHT) / 2

def _draw_badges(participants:list = [], page_size=A4):
    
    logo = _get_transparent_background_logo()
    
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=page_size if page_size == A4 else landscape((BADGE_WIDTH, BADGE_HEIGHT)), initialFontName='CenturyGothicBold')
    c.setTitle("Badges")
    c.setAuthor("MUNOL")
    c.setSubject("Badges for MUNOL Conference")
    c.setCreator("MUNOL CMS")
    c.setProducer("MUNOL CMS")
    

    for i, p in enumerate(participants):
        col = i % COLUMNS
        row = i // COLUMNS % ROWS
        x = MARGIN_X + col * BADGE_WIDTH
        y = PAGE_HEIGHT - MARGIN_Y - (row + 1) * BADGE_HEIGHT
        c.saveState()
        if page_size == A4:
            c.translate(x + i%2*mm, y - i//2*mm)
        
        c.setFont('CenturyGothicBold', 11)

        # Draw dashed border around badge
        c.setDash(1,5)
        c.setLineWidth(0.2)
        c.setStrokeColor((0,0,0), 0.2)
        c.rect(0, 0, BADGE_WIDTH, BADGE_HEIGHT, stroke=1, fill=0)
        c.setDash()  # Reset dash pattern
        
        # Logo in background
        c.drawImage(logo, 9*mm,8*mm,35*mm,35*mm, mask='auto')
        
        
        # handle photo for custom badges
        if 'photo' in p and p['photo']:
            photo = p['photo'] 
        else:
            # Print badge photo if set
            image_path = str(p['picture']) if p['picture'] !='' and p['picture'] else 'images/default_photo.png'
            photo = ImageReader(os.path.join(settings.MEDIA_ROOT, image_path))

        c.drawImage(photo, 54*mm,8*mm,30*mm,40*mm, mask='auto')

        # colored rectangle at bottom
        c.setFillColor(p['color'], 1)
        c.rect(0,0,85*mm,7*mm,fill=True,stroke=False)
            
        # name
        c.setFillColor((0,0,0), 1)
        c.drawString(3*mm,49*mm, f"{p['name']}")

        # school or association
        c.setFont('Helvetica-Oblique', 11)
        c.drawString(3*mm,44*mm, p['affiliation'])

        # position, if necessary split in multiple lines
        c.setFont('CenturyGothicBold', 16)
        split_text = p['position'].split("\n") # Work around for new lines between placard name and forum name, which caused issues with textwrap
        lines = [line.replace('--', ' ') for part in split_text for line in textwrap.wrap(part, width=15)]
        
        for index, line in enumerate(lines):
            c.drawCentredString(27*mm, 24*mm + len(lines)*2*mm  - index* 6*mm, line)
            
        # year
        c.setFont('CenturyGothicBold', 8)
        c.drawCentredString(27*mm, 2.5*mm, f"MUNOL {year}")

        # no media consent icon
        # if p['media_consent'] == False:
        #     c.drawImage(ImageReader(os.path.join(settings.MEDIA_ROOT, 'images/camera-off.png')), 78*mm, 1*mm, 5*mm, 5*mm, mask='auto')

        # place 8 badges per page, then create new page
        c.restoreState()

        if (i + 1) % (COLUMNS * ROWS) == 0 or page_size != A4:
            c.showPage()
      
    c.save()
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='badges.pdf', content_type="application/pdf", as_attachment=False)

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def advisor_badges(request):
    queryset = Advisor.objects
    participants = _filter_queryset_by_uuid(queryset, request)
    participants = participants.order_by('first_name', 'last_name')
    badge_infos = [{
        "uuid": p.id,
        "name": f"{p.first_name} {p.last_name}",
        "affiliation": "- MUNOL Association -",
        "position": "Conference Advisor",
        "color": ROLE_TO_COLOR[Advisor],
        "picture": p.picture,
        "media_consent": p.media_consent_time is not None
    } for p in participants]
    return _draw_badges(badge_infos, request.data.get('page_size', A4))

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def mun_director_badges(request):
    queryset = MUNDirector.objects
    participants = _filter_queryset_by_uuid(queryset, request)
    participants = participants.order_by('school')
    badge_infos = [{
        "name": f"{p.first_name} {p.last_name}",
        "affiliation": p.school.name,
        "position": "MUN-Director",
        "color": ROLE_TO_COLOR[MUNDirector],
        "picture": p.picture,
        "media_consent": p.media_consent_time is not None
    } for p in participants]
    return _draw_badges(badge_infos, request.data.get('page_size', A4))

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def executive_badges(request):
    queryset = Executive.objects
    participants = _filter_queryset_by_uuid(queryset, request)
    participants = participants.order_by('position_name')
    badge_infos = [{
        "name": f"{p.first_name} {p.last_name}",
        "affiliation": p.school_name,
        "position": p.position_name,
        "color": ROLE_TO_COLOR[Executive],
        "picture": p.picture,
        "media_consent": p.media_consent_time is not None
    } for p in participants]
    return _draw_badges(badge_infos, request.data.get('page_size', A4))

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def student_officer_badges(request):
    queryset = StudentOfficer.objects
    participants = _filter_queryset_by_uuid(queryset, request)
    participants = participants.order_by('position_name')
    badge_infos = [{
        "name": f"{p.first_name} {p.last_name}",
        "affiliation": p.school_name,
        "position": p.position_name,
        "color": ROLE_TO_COLOR[StudentOfficer],
        "picture": p.picture,
        "media_consent": p.media_consent_time is not None
    } for p in participants]
    return _draw_badges(badge_infos, request.data.get('page_size', A4))

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def staff_badges(request):
    queryset = Staff.objects
    participants = _filter_queryset_by_uuid(queryset, request)
    participants = participants.order_by('position_name')
    badge_infos = [{
        "name": f"{p.first_name} {p.last_name}",
        "affiliation": p.school_name,
        "position": p.position_name,
        "color": ROLE_TO_COLOR[Staff],
        "picture": p.picture,
        "media_consent": p.media_consent_time is not None
    } for p in participants]
    return _draw_badges(badge_infos, request.data.get('page_size', A4))

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def delegate_badges(request):
    participants = Delegate.objects
    participants = _filter_queryset_by_uuid(participants, request)
    participants = participants.order_by('school')
    badge_infos = [{
        "name": f"{p.first_name} {p.last_name}",
        "affiliation": p.school.name if p.school else "",
        "position": f"{p.represents.placard_name}\n--\n{p.forum.abbreviation}" if p.represents and p.forum else "", 
        "color": ROLE_TO_COLOR[Delegate],
        "picture": p.picture,
        "media_consent": p.media_consent_time is not None
    } for p in participants]
    return _draw_badges(badge_infos, request.data.get('page_size', A4))

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def custom_badge(request):
    
    color = request.data.get('color', '#FFFFFF') 
    color = tuple(int(color.lstrip('#')[i:i+2], 16)/255 for i in (0, 2, 4))
   
    badge_info = {
        "name": f"{request.data.get('first_name', '')} {request.data.get('last_name', '')}",
        "affiliation": request.data.get('affiliation', ''),
        "position": request.data.get('position', ''),
        "color": color,
        "photo": request.data.get('photo', ''), # picture is explicitly different from photo
        "media_consent": request.data.get('media_consent', False)
    }
    page_size = A4 if request.data.get('page_size') == 'A4' else None
    return _draw_badges([badge_info], page_size)    
