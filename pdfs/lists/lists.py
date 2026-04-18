import io
from wsgiref.util import FileWrapper
from django.http import FileResponse

from api.models import Delegate, Forum, Issue, MemberOrganization, School
from api.permissions import IsOrganizer, IsAdmin
from rest_framework.decorators import api_view, permission_classes

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, portrait, A4, A3 
from reportlab.lib.units import mm
import textwrap

from pdfs.utils import _register_MUNOL_fonts, _get_transparent_background_logo, _get_fitting_font_size, _get_page_size_from_request
_register_MUNOL_fonts()

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def add_logo_to_canvas(canvas, doc):
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

@api_view(["GET"])
@permission_classes([IsOrganizer|IsAdmin])
def issues_list(request):

    pagesize = portrait(_get_page_size_from_request(request))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    forum_title_style = ParagraphStyle(
        name="ForumTitle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=0,
        spaceAfter=0,
        textColor=colors.black
    )

    subtitle_style = ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        fontSize=12,
        textColor=colors.grey,
        spaceBefore=0,
        spaceAfter=10,
        fontName='CenturyGothicItalic'
    )

    bullet_style = ParagraphStyle(
        name="Bullet",
        parent=styles["Normal"],
        leftIndent=0,
        spaceAfter=2
    )

    story = []

    forums = Forum.objects.all()
       
    for forum in forums:
        # ---- Forum Title ----
        abbreviation = f" ({forum.abbreviation})" if forum.abbreviation else ""
        title_text = f"<b>{forum.name}</b> {abbreviation}"
        story.append(Paragraph(title_text, forum_title_style))

        # ---- Subtitle ----
        if forum.subtitle:
            story.append(Paragraph(forum.subtitle, subtitle_style))

        # ---- Issues (Bullet List) ----
        issue_bullet_items = [
            ListItem(Paragraph(issue.name, bullet_style))
            for issue in  Issue.objects.filter(forum=forum.id)
        ]

        story.append(
            ListFlowable(
                issue_bullet_items,
                bulletType='bullet',
                leftIndent=10
            )
        )

        story.append(Spacer(1, 16))  # space between forums

    

    doc.build(story, onFirstPage=add_logo_to_canvas, onLaterPages=add_logo_to_canvas)

    # return document as pdf file response
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='issues_list.pdf', content_type="application/pdf", as_attachment=False)

@api_view(["GET"])
@permission_classes([IsOrganizer|IsAdmin])
def schools_list(request):

    pagesize = portrait(_get_page_size_from_request(request))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    delegationsStyle = ParagraphStyle(
        name="Delegations",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.grey,
        spaceBefore=0,
        spaceAfter=0,
        fontName='CenturyGothicItalic'
    )
    
    story = []

    schools = []

    for school in School.objects.all().order_by('name'):
        # get all member organizations which are represented by delegates from this school, and get the unique set of those member organizations
        member_orgs = MemberOrganization.objects.filter(delegate__school_id=school.id).distinct()
        member_orgs_text = "("+ ", ".join([member_org.name for member_org in member_orgs])+ ")" if member_orgs else ""
        schools += [ListItem([Paragraph(f"<b>{school.name}</b>, {school.city}, {school.country}", styles["Normal"]),
                             Paragraph(member_orgs_text, delegationsStyle)])]

    story.append(
        ListFlowable(
            schools,
            bulletType='bullet',
            leftIndent=10
        )
    )

    doc.build(story, onFirstPage=add_logo_to_canvas, onLaterPages=add_logo_to_canvas)

    # return document as pdf file response
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='schools_list.pdf', content_type="application/pdf", as_attachment=False)
