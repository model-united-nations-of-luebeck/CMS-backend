import io
import os
from wsgiref.util import FileWrapper
from django.http import FileResponse
from django.conf import settings
from django.db.models.functions import Reverse

from api.models import Advisor, Conference, Delegate, Executive, Forum, Issue, MUNDirector, MemberOrganization, Participant, School, Staff, StudentOfficer
from api.permissions import IsOrganizer, IsAdmin
from rest_framework.decorators import api_view, permission_classes

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, portrait, A4, A3 
from reportlab.lib.units import mm


from pdfs.utils import _register_MUNOL_fonts, _get_transparent_background_logo, _get_fitting_font_size, _get_page_size_from_request
_register_MUNOL_fonts()

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
def with_alpha(color, alpha):
    return colors.Color(color.red, color.green, color.blue, alpha=alpha)

def add_logo_to_canvas(canvas, doc):
    # Refactor into utils, template
    canvas.saveState()
    logo = _get_transparent_background_logo()
    logo_size = 50 * mm
    canvas.drawImage(
        logo,
        doc.pagesize[0] - logo_size + 20,
        -20,
        width=logo_size,
        height=logo_size,
        mask='auto'
    )

    canvas.restoreState()

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def participants_list(request):

    pagesize = portrait(_get_page_size_from_request(request))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
        title="Participants List",
        author="MUNOL CMS"
    )

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "CenturyGothic"
    styles["Title"].fontName = "CenturyGothicBold"
    cell_style = styles["BodyText"]
    cell_style.fontName = "CenturyGothic"
    cell_style.fontSize = 8
    
    story = []

    story.append(Paragraph(f"Participants List", styles["Title"]))

    # Table data
    data = [
        ["", "","Name", "Position", "School", "Birthdate"]
    ]

    
    participants = Participant.objects.select_related('delegate', 'studentofficer', 'mundirector', 'executive', 'staff', 'advisor').order_by('first_name', 'last_name')
    for participant in participants:

        school_name = ""
        for attr in [model.__name__.lower() for model in [Delegate, MUNDirector]]:
            if hasattr(participant, attr):
                school = getattr(participant, attr).school
                if school:
                    school_name = f"{school.name}, <font size=6>{school.city}, {school.country}</font>"
                else:
                    school_name = ""
        for attr in [model.__name__.lower() for model in [Executive, Staff, StudentOfficer]]:
            if hasattr(participant, attr):
                school_name = getattr(participant, attr).school_name
        
        position = ""
        for attr in [model.__name__.lower() for model in [Delegate]]:
            if hasattr(participant, attr):
                delegate = getattr(participant, attr)
                position = f"{delegate.represents.name} in {delegate.forum.abbreviation}"
        for attr in [model.__name__.lower() for model in [Executive, Staff, StudentOfficer]]:
            if hasattr(participant, attr):
                position = getattr(participant, attr).position_name
        for attr in [model.__name__.lower() for model in [MUNDirector, Advisor]]:
            if hasattr(participant, attr):
                position = dict(Participant.ROLE_CHOICES).get(participant.role, participant.role)

        if participant.birthday:
            age = (Conference.objects.first().start_date - participant.birthday).days // 365
            birthdate = f"{participant.birthday.strftime('%d. %m. %Y')} ({age})"
        else: 
            birthdate = "N/A"

        data.append([
            Paragraph("" if participant.media_consent_time else f"<img src='{os.path.join(settings.MEDIA_ROOT, 'images/camera-off.png')}' width='10' height='10'/>", cell_style),
            Paragraph("" if participant.organizers_notice_time else f"<img src='{os.path.join(settings.MEDIA_ROOT, 'images/account-off.png')}' width='10' height='10'/>", cell_style),
            Paragraph(f"{participant.first_name} {participant.last_name} <font size=6>({participant.pronouns})</font>", cell_style),
            
            Paragraph(f"{position}", cell_style),
            Paragraph(f"{school_name}", cell_style),
            Paragraph(f"{birthdate}", cell_style),
            
        ])

    # Table
    table = Table(data, colWidths=[5*mm, 5*mm,50*mm, 40*mm, 65*mm, 30*mm], repeatRows=1)

    table_style= [
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

        ("ALIGN", (0, 0), (-1, -1), "LEFT"),

        ("FONTNAME", (0, 0), (-1, 0), "CenturyGothicBold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("BACKGROUND", (0, 1), (-1, -1), colors.transparent),
        ("FONTNAME", (0, 1), (-1, -1), "CenturyGothic"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.transparent, with_alpha(colors.lightgrey, 0.5)]),
    ]


    table.setStyle(TableStyle(table_style))

    story.append(table)

    doc.build(story, onFirstPage=add_logo_to_canvas, onLaterPages=add_logo_to_canvas)

    

    # return document as pdf file response
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='participants_list.pdf', content_type="application/pdf", as_attachment=False)
