import io
from tkinter import Image
from wsgiref.util import FileWrapper
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4,A3 
from api.models import Executive, MemberOrganization, StudentOfficer
from reportlab.lib.utils import ImageReader
from django.conf import settings
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('CenturyGothic', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Regular.TTF')))
pdfmetrics.registerFont(TTFont('CenturyGothicBold', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Bold.TTF')))

def _get_fitting_fontsize(placard_name: str, default_font_size: int=142,  pagesize = A4, margin:int = 50):
    width = pagesize[1]
    font_size = default_font_size
    while width >= pagesize[1] - margin:
        width = stringWidth(placard_name, 'CenturyGothicBold', font_size)
        font_size -= 1
    return font_size

def _create_delegates_placards(member_ids:list=None, pagesize=A4):
    member_names = []
    mos = MemberOrganization.objects.all()
    for member in mos:
        # print only members with corresponding ids
        if member_ids is not None and member.id not in member_ids:
            continue
        member_names.append(member.placard_name)
    
    return _create_placards_file(member_names, pagesize=pagesize)
        

def _create_placards_file(names: list = [], pagesize=A4):
    logo = ImageReader(os.path.join(settings.MEDIA_ROOT, 'images/logogray.png'))
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(pagesize), initialFontName='CenturyGothicBold')
    p.setTitle("Placards")
    
    for name in names:
       
        image_size = 265 if pagesize==A4 else 360
        font_height = 20 if pagesize==A4 else 30
        center_margin = 20 if pagesize==A4 else 30

        p.setFontSize(_get_fitting_fontsize(name, 142 if pagesize==A4 else 200, pagesize))
        
        p.drawImage(logo, pagesize[1]/2 - image_size/2,  center_margin, image_size, image_size, mask='auto')
        p.drawCentredString(pagesize[1]/2, pagesize[0]*1/4 - font_height, name)
        
        
        p.rotate(180)
        
        p.drawImage(logo,-pagesize[1]/2 - image_size/2,-pagesize[0] + center_margin, image_size, image_size, mask='auto')
        p.drawCentredString(-pagesize[1]/2, -pagesize[0]*3/4 - font_height, name)
        
        p.showPage()    

    # Close the PDF object cleanly, and we're done.
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers present the option to save the file.
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='placards.pdf', content_type="application/pdf", as_attachment=True)


def _create_orga_placards_file(officers: list = [], pagesize=A4):
    logo = ImageReader(os.path.join(settings.MEDIA_ROOT, 'images/logogray.png'))
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(pagesize), initialFontName='CenturyGothicBold')
    p.setTitle("Placards")
    
    for officer in officers:
       
        image_size = 100 if pagesize==A4 else 130
        font_height = 20 if pagesize==A4 else 30
        center_margin = 190 if pagesize==A4 else 280

        name = f"{officer.first_name} {officer.last_name}"

        p.setFontSize(_get_fitting_fontsize(officer.position_name, 80 if pagesize==A4 else 100, pagesize))
        
        p.drawImage(logo, pagesize[1]/2 - image_size/2,  center_margin, image_size, image_size, mask='auto')
        
        p.setFont('CenturyGothic',_get_fitting_fontsize(name, 80 if pagesize==A4 else 100, pagesize))
        p.drawCentredString(pagesize[1]/2, pagesize[0]*1/10 - font_height, name)
        
        p.setFont('CenturyGothicBold',_get_fitting_fontsize(officer.position_name, 100 if pagesize==A4 else 100, pagesize))
        p.drawCentredString(pagesize[1]/2, pagesize[0]*2/8 - font_height, officer.position_name)
        
        
        p.rotate(180)
        
        p.drawImage(logo,-pagesize[1]/2 - image_size/2,-pagesize[0] + center_margin, image_size, image_size, mask='auto')
        
        p.setFont('CenturyGothic',_get_fitting_fontsize(name, 80 if pagesize==A4 else 100, pagesize))
        p.drawCentredString(-pagesize[1]/2, -pagesize[0]*9/10 - font_height, name)
        
        p.setFont('CenturyGothicBold',_get_fitting_fontsize(officer.position_name, 80 if pagesize==A4 else 100, pagesize))
        p.drawCentredString(-pagesize[1]/2, -pagesize[0]*6/8 - font_height, officer.position_name)
        

        p.showPage()    

    # Close the PDF object cleanly, and we're done.
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers present the option to save the file.
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='placards.pdf', content_type="application/pdf", as_attachment=True)

def executive_placards(request):
    filtered_executives = []
    pagesize = A4
    if request.GET is not None and 'ids' in request.GET:
        ids = request.GET['ids'].split(",")
        ids = list(map(int, ids)) #cast to ints
        
        executives = Executive.objects.all()
        
        for executive in executives:
            # print only members with corresponding ids
            if ids is not None and executive.id not in ids:
                continue
            filtered_executives.append(executive)
    
    if request.GET is not None and 'pagesize' in request.GET:
        pagesize = A3 if request.GET['pagesize'] == 'A3' else A4
    return _create_orga_placards_file(officers=filtered_executives, pagesize=pagesize)

def student_officer_placards(request):
    filtered_student_officers = []
    pagesize = A4
    if request.GET is not None and 'ids' in request.GET:
        ids = request.GET['ids'].split(",")
        ids = list(map(int, ids)) #cast to ints
        
        student_officers = StudentOfficer.objects.all()
        
        for student_officer in student_officers:
            # print only members with corresponding ids
            if ids is not None and student_officer.id not in ids:
                continue
            filtered_student_officers.append(student_officer)
    
    if request.GET is not None and 'pagesize' in request.GET:
        pagesize = A3 if request.GET['pagesize'] == 'A3' else A4
    return _create_orga_placards_file(officers=filtered_student_officers, pagesize=pagesize)


def placards(request):
    ids = None
    pagesize = A4
    if request.GET is not None and 'ids' in request.GET:
        ids = request.GET['ids'].split(",")
        ids = list(map(int, ids)) #cast to ints
    if request.GET is not None and 'pagesize' in request.GET:
        pagesize = A3 if request.GET['pagesize'] == 'A3' else A4
    return _create_delegates_placards(member_ids = ids, pagesize=pagesize)

def custom_placard(request):
    name = ''
    pagesize = A4
    if request.GET is not None and 'name' in request.GET:
        name = request.GET['name']
    if request.GET is not None and 'pagesize' in request.GET:
        pagesize = A3 if request.GET['pagesize'] == 'A3' else A4
    return _create_placards_file(names=[name], pagesize=pagesize)
