import io
from wsgiref.util import FileWrapper
from django.http import FileResponse
from django.db.models.functions import Reverse

from api.models import Delegate, Executive, Forum, Issue, MemberOrganization, Plenary, School, Staff, StudentOfficer
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

@api_view(["GET"])
@permission_classes([IsOrganizer|IsAdmin])
def roll_call_list_plenaries(request):

    pagesize = landscape(_get_page_size_from_request(request))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
        title="Roll Call List - Forums",
        author="MUNOL CMS"
    )

    styles = getSampleStyleSheet()
    cell_style = styles["BodyText"]
    
    story = []

    for plenary in Plenary.objects.all():
        # Title
        story.append(Paragraph(f"Roll Call List - {plenary.abbreviation}", styles["Title"]))
        story.append(Spacer(1, 12))

        n_cols = 20

        # Table data
        data = [
            ["Delegation", "Delegates", *([""]*n_cols)]
        ]

        forums_in_plenary = Forum.objects.filter(plenary=plenary.id)
        delegates_in_plenary = Delegate.objects.filter(forum__in=forums_in_plenary)
        member_organizations_in_plenary = MemberOrganization.objects.filter(id__in=delegates_in_plenary.values('represents_id')).distinct()

        for org in member_organizations_in_plenary:
            delegation = delegates_in_plenary.filter(represents=org)
            data.append([
                Paragraph(f"<b>{org.name}</b>{'*' if org.status not in [MemberOrganization.MEMBER_STATE, MemberOrganization.FORMER_MEMBER] else ''} <font size=8><i>{org.official_name}</i></font>", cell_style),
                Paragraph(f"{len(delegation)}: <font size=8>{', '.join([f'{d.forum.abbreviation}' for d in delegation])}</font>", cell_style),
                
                *[Paragraph("O", cell_style)]*n_cols,
            ])

        # Table
        table = Table(data, colWidths=[80*mm, 30*mm, *[7*mm]*n_cols], repeatRows=1)

        table_style= [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

            ("ALIGN", (0, 0), (-1, -1), "LEFT"),

            ("FONTNAME", (0, 0), (-1, 0), "CenturyGothicBold"),
            ("FONTSIZE", (0, 0), (-1, -1), 14),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ("BACKGROUND", (0, 1), (-1, -1), colors.transparent),
            ("FONTNAME", (0, 1), (-1, -1), "CenturyGothic"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.transparent, with_alpha(colors.lightgrey, 0.5)]),
            ("FONTSIZE", (0, 1), (-1, -1), 11),
        ]

        table.setStyle(TableStyle(table_style))

        story.append(table)
        story.append(PageBreak())

    doc.build(story, onFirstPage=add_logo_to_canvas, onLaterPages=add_logo_to_canvas)

    

    # return document as pdf file response
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='roll_call_list_plenaries.pdf', content_type="application/pdf", as_attachment=False)
