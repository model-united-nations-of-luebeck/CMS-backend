import io
from wsgiref.util import FileWrapper
from django.http import FileResponse
from django.db.models.functions import Reverse

from api.models import Delegate, Executive, Forum, Issue, MemberOrganization, School, StudentOfficer
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
    TableStyle
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
def student_officers_list(request):

    pagesize = landscape(_get_page_size_from_request(request))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
        title="Student Officer List",
        author="MUNOL CMS"
    )

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "CenturyGothic"
    styles["Title"].fontName = "CenturyGothicBold"
    cell_style = styles["BodyText"]
    cell_style.fontName = "CenturyGothic"
    
    story = []

    
    # Title
    story.append(Paragraph("Student Officer List", styles["Title"]))
    story.append(Spacer(1, 12))

    # Table data
    data = [
        ["Name", "Position", "Email", "Phone"]
    ]

    student_officers = StudentOfficer.objects.all().order_by('forum__id')
    for officer in student_officers:
        data.append([
            Paragraph(f"{officer.first_name} {officer.last_name}", cell_style),
            Paragraph(officer.position_name, cell_style),
            Paragraph(officer.email, cell_style),
            Paragraph(str(officer.mobile), cell_style),
        ])

    # Table
    table = Table(data, colWidths=[60*mm, 100*mm, 80*mm, 40*mm], repeatRows=1)

    table_style= [
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

        ("ALIGN", (0, 0), (-1, -1), "LEFT"),

        ("FONTNAME", (0, 0), (-1, 0), "CenturyGothicBold"),
        ("FONTSIZE", (0, 0), (-1, -1), 14),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("BACKGROUND", (0, 1), (-1, -1), colors.transparent),
        ("FONTNAME", (0, 1), (-1, -1), "CenturyGothic"),
        ("FONTSIZE", (0, 1), (-1, -1), 11),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.transparent, with_alpha(colors.lightgrey, 0.5)]),
    ]

    table.setStyle(TableStyle(table_style))

    story.append(table)

    doc.build(story, onFirstPage=add_logo_to_canvas, onLaterPages=add_logo_to_canvas)

    # return document as pdf file response
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='student_officer_list.pdf', content_type="application/pdf", as_attachment=False)
