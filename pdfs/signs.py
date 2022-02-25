import io
import os
import textwrap
from wsgiref.util import FileWrapper
import PIL
import base64
from django.http import FileResponse
from django.template.defaultfilters import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.units import mm
from api.models import Delegate, Forum, MemberOrganization
from reportlab.lib.utils import ImageReader
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
pdfmetrics.registerFont(TTFont('CenturyGothic', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Regular.TTF')))
pdfmetrics.registerFont(TTFont('CenturyGothicBold', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Bold.TTF')))
pdfmetrics.registerFont(TTFont('CenturyGothicItalic', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Italic.TTF')))
pdfmetrics.registerFont(TTFont('Times-Roman-Small-Caps-Bold', os.path.join(settings.MEDIA_ROOT, 'fonts/Times-Roman-Small-Caps-Bold.ttf')))

def _create_sign(text:str='', pagesize=A4):
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(pagesize))
    p.setTitle("Sign")
    
    logo = ImageReader(os.path.join(settings.MEDIA_ROOT, 'images/logograytransparent.png'))
    
    #logo in background
    margin = pagesize[0]/4
    size = pagesize[0] - margin
    p.drawImage(logo, pagesize[1]/2 - size/2, pagesize[0]/2 - size/2, size,size,mask='auto')

    p.setFont('CenturyGothicBold', 142 if pagesize==A4 else 242)
    p.drawCentredString(pagesize[1]/2,pagesize[0]/2-pagesize[0]/20,text)


    p.showPage()   
    p.save()
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='sign.pdf', content_type="application/pdf", as_attachment=True)

def sign(request):
    
    text=''
    if request.GET is not None and 'text' in request.GET:
        text = request.GET['text']

    pagesize=A4
    if request.GET is not None and 'pagesize' in request.GET:
        pagesize = A3 if request.GET['pagesize'] == 'A3' else A4
    return _create_sign(text, pagesize=pagesize)   
