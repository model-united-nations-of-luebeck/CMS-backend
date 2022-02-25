import io
import os
import textwrap
from wsgiref.util import FileWrapper
import PIL
import base64
from django.http import FileResponse
from django.template.defaultfilters import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3, portrait
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

def _create_forum_roll_call_list(forums:list=[], pagesize=A4):
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=portrait(pagesize))
    p.setTitle("Roll Call List")
    
    for forum in forums:
        
        p.setFont('CenturyGothicBold', 20)
        p.drawCentredString(pagesize[0]/2,pagesize[1]-10*mm,forum.name)

        width = pagesize[0]
        height = pagesize[1]-10*mm
        x =  0
        y = 11*mm

        data = [['Member  |  Date']]
        delegates_in_forum = Delegate.objects.filter(forum=forum)
        for delegate in delegates_in_forum:
            data.append([delegate.represents.placard_name] + [' ']*55)
        
        style = TableStyle([
                            ('LINEBEFORE',(1,0),(-1,-1),0.2,colors.gray),
                            ])
        t = Table(data,  style=style)
        
        #alternating row colors
        for each in range(len(data)):
            if each % 2 == 0:
                bg_color = colors.whitesmoke
            else:
                bg_color = colors.lightgrey

            t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

        
        #manually drawing and splitting table over pages
        w,h = t.wrapOn(p, width, height)
        if w>width or h>height:
            while w>width or h>height:
                splits = t.split(width, height)
                used_w, used_h = splits[0].wrapOn(p, width, height)
                splits[0].drawOn(p, x, pagesize[1]-used_h-y)
                if len(splits)==1:
                    break
                t=splits[1]
                p.showPage()   
        else:
            t.drawOn(p, x, pagesize[1]-h-y)
            p.showPage()   
    p.save()
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='rollcalllist.pdf', content_type="application/pdf", as_attachment=True)

def forum_roll_call_list(request):
    forums = Forum.objects.all()
    ids = None
    if request.GET is not None and 'ids' in request.GET:
        ids = request.GET['ids'].split(",")
        ids = list(map(int, ids)) #cast to ints
    # print only forums with corresponding ids
    filtered_forums = []
    for forum in forums:
        if ids is not None and forum.id not in ids:
            continue
        filtered_forums.append(forum)
    
    pagesize=A4
    if request.GET is not None and 'pagesize' in request.GET:
        pagesize = A3 if request.GET['pagesize'] == 'A3' else A4
    return _create_forum_roll_call_list(filtered_forums, pagesize=pagesize)   
