import io
from wsgiref.util import FileWrapper
from django.http import FileResponse
from django.db.models.functions import Reverse

from api.models import Advisor, Delegate, Executive, Forum, Issue, MemberOrganization, School
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
def advisors_list(request):

    pagesize = landscape(_get_page_size_from_request(request))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
        title="Advisors List",
        author="MUNOL CMS"
    )

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "CenturyGothic"
    styles["Title"].fontName = "CenturyGothicBold"
    cell_style = styles["BodyText"]
    cell_style.fontName = "CenturyGothic"
    
    story = []

    
    # Title
    story.append(Paragraph("Advisors List", styles["Title"]))
    story.append(Spacer(1, 12))

    # Table data
    data = [
        ["Name", "Email", "Phone", "Experience", "Help", "Car", "Availability"]
    ]

    advisors = Advisor.objects.all().order_by('first_name', 'last_name')
    for advisor in advisors:
        data.append([
            Paragraph(f"{advisor.first_name} {advisor.last_name}", cell_style),
            Paragraph(advisor.email, cell_style),
            Paragraph(str(advisor.mobile), cell_style),
            Paragraph(advisor.experience, cell_style),
            Paragraph(advisor.help, cell_style),
            Paragraph("Yes" if advisor.car else "No", cell_style),
            Paragraph(advisor.availability, cell_style),
        ])

    # Table
    table = Table(data, colWidths=[30*mm, 40*mm, 30*mm, 70*mm, 30*mm, 20*mm, 50*mm], repeatRows=1)

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
    return FileResponse(FileWrapper(buffer), filename='advisors_list.pdf', content_type="application/pdf", as_attachment=False)
