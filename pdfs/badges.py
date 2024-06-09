import io
import os
import textwrap
from wsgiref.util import FileWrapper
import PIL
import base64
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from api.models import Advisor, Conference, Delegate, Executive, MUNDirector, Participant, Staff, StudentOfficer
from reportlab.lib.utils import ImageReader
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
if  os.path.exists(os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Regular.TTF')):
    pdfmetrics.registerFont(TTFont('CenturyGothic', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Regular.TTF')))
    pdfmetrics.registerFont(TTFont('CenturyGothicBold', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Bold.TTF')))
    pdfmetrics.registerFont(TTFont('CenturyGothicItalic', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Italic.TTF')))

def _get_fitting_fontsize(text: str, default_font_size: int=16, max_width=50*mm):
    width = max_width
    font_size = default_font_size
    while width >= max_width:
        width = stringWidth(text, 'CenturyGothicBold', font_size)
        font_size -= 1
    return font_size
        

def _create_badge(participants:list = [], color:tuple=(255,255,255), year=1998):
    
    logo = ImageReader(os.path.join(settings.MEDIA_ROOT, 'images/logograytransparent.png'))
    
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape((85 * mm, 55 * mm)))
    p.setTitle("Badges")
    
    for participant in participants:
        p.setFont('CenturyGothicBold', 11)
        
        #logo in background
        p.drawImage(logo, 9*mm,7*mm,35*mm,35*mm, mask='auto')
        
        #print badge photo if set
        if hasattr(participant,'base64photo'):
            msg = base64.b64decode(participant.base64photo)
            buf = io.BytesIO(msg)
            bild = ImageReader(PIL.Image.open(buf))
        else:
            image_path = str(participant.picture) if participant.picture !='' and participant.picture else 'images/bild.jpeg'
            bild = ImageReader(os.path.join(settings.MEDIA_ROOT, image_path))


        p.drawImage(bild, 54*mm,8*mm,30*mm,40*mm, mask='auto')

        #colored rectangle at bottom
        p.setFillColor(color, 1)
        p.rect(0,0,85*mm,7*mm,fill=True,stroke=False)
            
        #name
        p.setFillColor((0,0,0), 1)
        p.drawString(3*mm,49*mm,f"{participant.first_name} {participant.last_name}")

        #school or association
        p.setFont('Helvetica-Oblique', 11)
        if type(participant) == Advisor:
            p.drawString(3*mm,44*mm,'- MUNOL Association - ')
        elif type(participant) in [Staff, Executive, StudentOfficer]:
            p.drawString(3*mm,44*mm,str(participant.school_name))
        elif type(participant) in [Delegate, MUNDirector]:
            p.drawString(3*mm,44*mm,str(participant.school.name))
        else:
            p.drawString(3*mm,44*mm,str(participant.affiliation))

        #position, if necessary split in multiple lines
        p.setFont('CenturyGothicBold', 16)
        if type(participant) == Advisor:
            p.drawCentredString(27*mm, 27*mm, 'Conference')
            p.drawCentredString(27*mm, 20*mm, 'Advisor')
        elif type(participant) == MUNDirector:
            p.drawCentredString(27*mm, 24*mm, 'MUN-Director')
        elif type(participant) in [Executive, StudentOfficer, Staff]:
            if _get_fitting_fontsize(participant.position_name, 16,max_width=50*mm) < 16:
                lines = textwrap.wrap(participant.position_name, width=15)
                for index in range(len(lines)):
                    p.drawCentredString(27*mm, 24*mm + len(lines)*2*mm  - index* 6*mm, lines[index])
            else:
                p.drawCentredString(27*mm, 24*mm, participant.position_name)
        elif type(participant) == Delegate:
            lines = textwrap.wrap(participant.represents.placard_name, width=16)
            for index in range(len(lines)):
                p.drawCentredString(27*mm, 30*mm + len(lines)*2*mm  - index* 6*mm, lines[index])

            lines = textwrap.wrap(participant.forum.name, width=15)
            for index in range(len(lines)):
                p.drawCentredString(27*mm, 15*mm + len(lines)*2*mm  - index* 6*mm, lines[index])
        else:
            lines = textwrap.wrap(participant.position, width=15)
            for index in range(len(lines)):
                p.drawCentredString(27*mm, 24*mm + len(lines)*2*mm  - index* 6*mm, lines[index])
            
        #year
        p.setFont('CenturyGothicBold', 8)
        p.drawCentredString(27*mm, 2.5*mm, f"MUNOL {year}")
        
    p.showPage()    
    p.save()
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='badges.pdf', content_type="application/pdf", as_attachment=True)

def advisor_badge(request):
    participants = Advisor.objects.all()
    return participant_badge(request, participants, color=(0, 1, 195/255))

def mundirector_badge(request):
    participants = MUNDirector.objects.all()
    return participant_badge(request, participants, color=(16/255,1,0))

def executive_badge(request):
    participants = Executive.objects.all()
    return participant_badge(request, participants, color=(1,0,0))

def student_officer_badge(request):
    participants = StudentOfficer.objects.all()
    return participant_badge(request, participants, color=(0,140/255,1))

def staff_badge(request):
    participants = Staff.objects.all()
    return participant_badge(request, participants, color=(188/255, 225/255, 1))    

def delegate_badge(request):
    participants = Delegate.objects.all()
    return participant_badge(request, participants, color=(1, 144/255, 0))   

def custom_badge(request):
    participant = Participant()
    color = (1,1,1)
    if request.GET is not None and 'first_name' in request.GET:
        setattr(participant,'first_name',request.GET['first_name'])
    if request.GET is not None and 'last_name' in request.GET:
        setattr(participant,'last_name',request.GET['last_name'])
    if request.GET is not None and 'affiliation' in request.GET:
        setattr(participant,'affiliation',request.GET['affiliation'])
    if request.GET is not None and 'position' in request.GET:
        setattr(participant,'position',request.GET['position'])
    if request.GET is not None and 'color' in request.GET:
        color=request.GET['color']
    if request.GET is not None and 'base64photo' in request.GET:
        setattr(participant,'base64photo',str(request.GET['base64photo']).replace(" ", "+"))
    
    return participant_badge(request, [participant], color = color)    

def participant_badge(request, participants, color):
    ids = None
    if request.GET is not None and 'ids' in request.GET:
        ids = request.GET['ids'].split(",")
        ids = list(map(int, ids)) #cast to ints
    # print only participants with corresponding ids
    filtered_participants = []
    for participant in participants:
        if ids is not None and participant.id not in ids:
            continue
        filtered_participants.append(participant)

    #determine year of current conference
    year = Conference.objects.first().start_date.year
    return _create_badge(participants = filtered_participants, color=color, year=year)

