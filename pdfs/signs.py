import io
from wsgiref.util import FileWrapper
from django.http import FileResponse

from api.permissions import IsOrganizer, IsAdmin
from rest_framework.decorators import api_view, permission_classes

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4, A3 
from reportlab.lib.units import mm
import textwrap

from pdfs.utils import _register_MUNOL_fonts, _get_transparent_background_logo, _get_fitting_font_size, _get_page_size_from_request
_register_MUNOL_fonts()

def _create_sign(label:str='', pagesize=A4):
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(pagesize), initialFontName='CenturyGothicBold')
    c.setTitle("Sign")
    c.setAuthor("MUNOL")
    c.setSubject("Sign for MUNOL Conference")
    c.setCreator("MUNOL CMS")
    c.setProducer("MUNOL CMS")

    logo = _get_transparent_background_logo()
    
    #logo in background
    margin = pagesize[0]/4
    size = pagesize[0] - margin
    c.drawImage(logo, pagesize[1]/2 - size/2, pagesize[0]/2 - size/2, size,size,mask='auto')

    c.setFont('CenturyGothicBold', 142 if pagesize==A4 else 200)

    split_text = label.split("\n")
    lines = [line.replace('--', ' ') for part in split_text for line in textwrap.wrap(part, width=15)]

    line_offset = 50 * mm if pagesize==A4 else 70 * mm

    for index, line in enumerate(lines):
        c.drawCentredString(pagesize[1]/2,pagesize[0]/2-pagesize[0]/20 - index * line_offset + (len(lines)-1)/2*line_offset, line)

    c.showPage()   
    c.save()
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='sign.pdf', content_type="application/pdf", as_attachment=False)

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def sign(request):
    
    label = request.data.get('label', '')
    
    return _create_sign(label, pagesize=_get_page_size_from_request(request))   
