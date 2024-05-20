import io
import os
import textwrap
from wsgiref.util import FileWrapper
import PIL
import base64
from django.http import FileResponse
from django.template.defaultfilters import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
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
    pdfmetrics.registerFont(TTFont('Times-Roman-Small-Caps-Bold', os.path.join(settings.MEDIA_ROOT, 'fonts/Times-Roman-Small-Caps-Bold.ttf')))

def _get_fitting_fontsize(text: str, default_font_size: int=16, max_width=50*mm):
    width = max_width
    font_size = default_font_size
    while width >= max_width:
        width = stringWidth(text, 'CenturyGothicBold', font_size)
        font_size -= 1
    return font_size
        
num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
           (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

ordinal = lambda n: "%s" % ("tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

def _num2roman(num):

    roman = ''
    while num > 0:
        for i, r in num_map:
            while num >= i:
                roman += r
                num -= i
    return roman

def _create_certificate(participants:list = [], session=1, year=1998, startday:str='',startmonth:str='', endday:str='', endmonth:str='', secgen:str='', depsecgen:str='', cms:str=''):
    
    logo = ImageReader(os.path.join(settings.MEDIA_ROOT, 'images/logograytransparent.png'))
    
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=portrait(A4))
    p.setTitle("Certificates")
    
    for participant in participants:
        

        #logo in background
        margin = 25
        p.drawImage(logo, margin/2*mm,A4[1]/2- (A4[0]-margin*mm)/2,A4[0]-margin*mm,A4[0]-margin*mm, mask='auto')

        p.setFont('Times-Roman-Small-Caps-Bold', 28)
        p.drawCentredString(A4[0]/2,A4[1]-27*mm,'Certificate of Participation')

        if type(participant) == Delegate:
            p.setFont('Times-Bold', 17)
            p.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            p.drawCentredString(A4[0]/2,A4[1]-75*mm,'has attended the')

            textobject = p.beginText()
            textobject.setTextOrigin(A4[0]/2-36*mm,A4[1]-95*mm)
            
            textobject.textOut(_num2roman(session))
            textobject.setRise(4)
            textobject.textOut(ordinal(session))
            textobject.setRise(0)
            textobject.textOut(' annual session of the')
            p.drawText(textobject)

            p.setFont('Times-Bold', 24)
            p.drawCentredString(A4[0]/2,A4[1]-110*mm,'Model United Nations of Lübeck')

            p.drawCentredString(A4[0]/2,A4[1]-130*mm,f'{startday} {startmonth} - {endday} {endmonth} {year}')

            p.setFont('Times-Bold', 17)
            delegate = 'Ambassador' if participant.ambassador else 'Delegate'
            p.drawCentredString(A4[0]/2,A4[1]-160*mm,f'as the {delegate} of the')
            p.drawCentredString(A4[0]/2,A4[1]-188*mm,'in the')
            p.drawCentredString(A4[0]/2,A4[1]-210*mm,'and is hereby awarded this certificate.')

            p.setFont('Times-Bold', 20)
            p.drawCentredString(A4[0]/2,A4[1]-172*mm, participant.represents.official_name)
            p.drawCentredString(A4[0]/2,A4[1]-198*mm, participant.forum.name)

            p.setFont('CenturyGothicBold', 20)
            p.drawCentredString(A4[0]/2,A4[1]-65*mm, f'{participant.first_name} {participant.last_name}')

            #signatures
            margin_side  = 20*mm
            margin_bottom = 40*mm
            width = 60*mm

            p.setLineWidth(0.5*mm)
            p.line(margin_side,margin_bottom, margin_side+width, margin_bottom)
            p.line(A4[0]-margin_side-width,margin_bottom, A4[0]-margin_side, margin_bottom)

            p.setFont('Times-Bold', 16)
            p.drawCentredString(margin_side + width/2,33*mm,secgen)
            p.drawCentredString(A4[0]-margin_side - width/2,33*mm,depsecgen)

            p.setFont('Times-Bold', 10)
            p.drawCentredString(margin_side + width/2,28*mm,f'(Secretary-General MUNOL {year})')
            p.drawCentredString(A4[0]-margin_side - width/2,28*mm, f'(Deputy Secretary-General MUNOL {year})')
            
        if type(participant) == StudentOfficer:
            p.setFont('Times-Roman', 16)
            p.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            p.drawCentredString(A4[0]/2,A4[1]-70*mm,'has successfully participated in')
            p.drawCentredString(A4[0]/2,A4[1]-80*mm,f'the Model United Nations of Lübeck Conference {year} as')
            p.drawCentredString(A4[0]/2,A4[1]-90*mm, f"{participant.position_name}.")

            p.drawCentredString(A4[0]/2,A4[1]-150*mm, "Model United Nations of Lübeck is a simulation conference of the United Nations")
            p.drawCentredString(A4[0]/2,A4[1]-160*mm, "with the goal of encouraging young people's interest for international politics, of")
            p.drawCentredString(A4[0]/2,A4[1]-170*mm, "ameliorating rhetorical skills and of motivating them to debate. For five days,")
            p.drawCentredString(A4[0]/2,A4[1]-180*mm, "over 60 people of three nations debated in five forums on political issues of")
            p.drawCentredString(A4[0]/2,A4[1]-190*mm, "international relevance.")

            p.drawCentredString(A4[0]/2,A4[1]-210*mm, "A Student Officer is responsible for one of the different bodies simulated, is")
            p.drawCentredString(A4[0]/2,A4[1]-220*mm, "chairing the debates, is part of the organisation team and one of the most")
            p.drawCentredString(A4[0]/2,A4[1]-230*mm, "important representatives of the conference.")

            p.setFont('Times-Italic', 20)
            p.drawCentredString(A4[0]/2,A4[1]-60*mm,f'{participant.first_name} {participant.last_name}')

            #signatures
            margin_side  = 20*mm
            margin_bottom = 40*mm
            width = 60*mm

            p.setLineWidth(0.5*mm)
            p.line(margin_side,margin_bottom, margin_side+width, margin_bottom)
            p.line(A4[0]-margin_side-width,margin_bottom, A4[0]-margin_side, margin_bottom)

            p.setFont('Times-Bold', 16)
            p.drawCentredString(margin_side + width/2,33*mm,secgen)
            p.drawCentredString(A4[0]-margin_side - width/2,33*mm,depsecgen)

            p.setFont('Times-Bold', 10)
            p.drawCentredString(margin_side + width/2,28*mm,f'(Secretary-General MUNOL {year})')
            p.drawCentredString(A4[0]-margin_side - width/2,28*mm, f'(Deputy Secretary-General MUNOL {year})')
            
        if type(participant) == Executive:
            p.setFont('Times-Bold', 17)
            p.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            p.drawCentredString(A4[0]/2,A4[1]-75*mm,'has attended the')

            textobject = p.beginText()
            textobject.setTextOrigin(A4[0]/2-36*mm,A4[1]-95*mm)
            
            textobject.textOut(_num2roman(session))
            textobject.setRise(4)
            textobject.textOut(ordinal(session))
            textobject.setRise(0)
            textobject.textOut(' annual session of the')
            p.drawText(textobject)

            p.setFont('Times-Bold', 24)
            p.drawCentredString(A4[0]/2,A4[1]-110*mm,'Model United Nations of Lübeck')

            p.drawCentredString(A4[0]/2,A4[1]-130*mm,f'{startday} {startmonth} - {endday} {endmonth} {year}')

            p.setFont('Times-Bold', 17)
            p.drawCentredString(A4[0]/2,A4[1]-160*mm,f'as the')
            p.drawCentredString(A4[0]/2,A4[1]-188*mm,'in the')
            p.drawCentredString(A4[0]/2,A4[1]-210*mm,'and is hereby awarded this certificate.')

            p.setFont('Times-Bold', 20)
            p.drawCentredString(A4[0]/2,A4[1]-172*mm, participant.position_name)
            p.drawCentredString(A4[0]/2,A4[1]-198*mm, "Executive Staff Team")

            p.setFont('CenturyGothicBold', 20)
            p.drawCentredString(A4[0]/2,A4[1]-65*mm, f'{participant.first_name} {participant.last_name}')

            #signatures
            margin_side  = 20*mm
            margin_bottom = 40*mm
            width = 60*mm

            p.setLineWidth(0.5*mm)
            p.line(A4[0]/2-width,margin_bottom, A4[0]/2+width, margin_bottom)

            p.setFont('Times-Bold', 16)
            p.drawCentredString(A4[0]/2,33*mm,cms)

            p.setFont('Times-Bold', 10)
            p.drawCentredString(A4[0]/2,28*mm,f'(Conference Managers MUNOL {year})')
            
        if type(participant) == Staff:
            p.setFont('Times-Bold', 17)
            p.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            p.drawCentredString(A4[0]/2,A4[1]-75*mm,'has attended the')

            textobject = p.beginText()
            textobject.setTextOrigin(A4[0]/2-36*mm,A4[1]-95*mm)
            
            textobject.textOut(_num2roman(session))
            textobject.setRise(4)
            textobject.textOut(ordinal(session))
            textobject.setRise(0)
            textobject.textOut(' annual session of the')
            p.drawText(textobject)

            p.setFont('Times-Bold', 24)
            p.drawCentredString(A4[0]/2,A4[1]-110*mm,'Model United Nations of Lübeck')

            p.drawCentredString(A4[0]/2,A4[1]-130*mm,f'{startday} {startmonth} - {endday} {endmonth} {year}')

            p.setFont('Times-Bold', 17)
            p.drawCentredString(A4[0]/2,A4[1]-160*mm,f'as')
            p.drawCentredString(A4[0]/2,A4[1]-188*mm,'in the')
            p.drawCentredString(A4[0]/2,A4[1]-210*mm,'and is hereby awarded this certificate.')

            p.setFont('Times-Bold', 20)
            p.drawCentredString(A4[0]/2,A4[1]-172*mm, participant.position_name)
            p.drawCentredString(A4[0]/2,A4[1]-198*mm, "Staff Team")

            p.setFont('CenturyGothicBold', 20)
            p.drawCentredString(A4[0]/2,A4[1]-65*mm, f'{participant.first_name} {participant.last_name}')

            #signatures
            margin_side  = 20*mm
            margin_bottom = 40*mm
            width = 60*mm

            p.setLineWidth(0.5*mm)
            p.line(A4[0]/2-width,margin_bottom, A4[0]/2+width, margin_bottom)

            p.setFont('Times-Bold', 16)
            p.drawCentredString(A4[0]/2,33*mm,cms)

            p.setFont('Times-Bold', 10)
            p.drawCentredString(A4[0]/2,28*mm,f'(Conference Managers MUNOL {year})')

        if type(participant) == MUNDirector:
            p.setFont('Times-Bold', 17)
            p.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            p.drawCentredString(A4[0]/2,A4[1]-75*mm,'has attended the')

            textobject = p.beginText()
            textobject.setTextOrigin(A4[0]/2-36*mm,A4[1]-95*mm)
            
            textobject.textOut(_num2roman(session))
            textobject.setRise(4)
            textobject.textOut(ordinal(session))
            textobject.setRise(0)
            textobject.textOut(' annual session of the')
            p.drawText(textobject)

            p.setFont('Times-Bold', 24)
            p.drawCentredString(A4[0]/2,A4[1]-110*mm,'Model United Nations of Lübeck')

            p.drawCentredString(A4[0]/2,A4[1]-130*mm,f'{startday} {startmonth} - {endday} {endmonth} {year}')

            p.setFont('Times-Bold', 17)
            p.drawCentredString(A4[0]/2,A4[1]-160*mm,f'as')
            p.drawCentredString(A4[0]/2,A4[1]-188*mm,'and is hereby awarded this certificate.')

            p.setFont('Times-Bold', 20)
            p.drawCentredString(A4[0]/2,A4[1]-172*mm, 'MUN-Director')

            p.setFont('CenturyGothicBold', 20)
            p.drawCentredString(A4[0]/2,A4[1]-65*mm, f'{participant.first_name} {participant.last_name}')

            #signatures
            margin_side  = 20*mm
            margin_bottom = 40*mm
            width = 60*mm

            p.setLineWidth(0.5*mm)
            p.line(A4[0]/2-width,margin_bottom, A4[0]/2+width, margin_bottom)

            p.setFont('Times-Bold', 16)
            p.drawCentredString(A4[0]/2,33*mm,cms)

            p.setFont('Times-Bold', 10)
            p.drawCentredString(A4[0]/2,28*mm,f'(Conference Managers MUNOL {year})')
                

        #variables for lines in frame
        heighttop = 2*mm
        topleft = 11.5*mm
        left = 6*mm
        innerborderstrenght = 2*mm

        linestop = topleft-4*mm

        linesbottom = A4[1]-linestop
        righttop = A4[0]-topleft
        quadheight = heighttop+4*mm
        quadlengthleft = left+4*mm
        quadlengthright = A4[0]-quadlengthleft
        right = A4[0]-left
        heightbottom = A4[1]-heighttop
        bottomquadheight = A4[1]-quadheight

        innerleft = left+2*mm
        innerright = A4[0] - innerleft
        innertop = heighttop +1*mm
        innerbottom = (A4[1]- innertop) -1*mm
        innertoppos = innertop + (innerborderstrenght/2)

        # defines inner line
        p.setLineWidth(innerborderstrenght)
        p.setStrokeColorRGB(68/255, 72/255, 143/255)
        p.setLineCap(2) #round
        p.line(innerleft,innertoppos,innerright,innertoppos) #bottom 
        p.line(innerright,innertoppos,innerright,innerbottom) #right
        p.line(innerleft,innertoppos,innerleft,innerbottom) #left
        p.line(innerleft,innerbottom,innerright,innerbottom) #top


        # defines outer line
        
        p.setLineWidth(0.5*mm)
        p.setStrokeColorRGB(0,0,0)
        p.line(topleft, heighttop, righttop, heighttop)  # top
        p.line(right, linestop, right, linesbottom)  #right
        p.line(left, linestop, left, linesbottom)  #left
        p.line(topleft, heightbottom, righttop, heightbottom)  # bottom

        #Quad Left TOP
        p.line(left,heighttop,left,quadheight) # left outer quad side
        p.line(quadlengthleft,heighttop,quadlengthleft,linestop) # left inner quad side
        p.line(left,heighttop,quadlengthleft,heighttop) # left quad top
        p.line(left,quadheight,topleft,quadheight) # left quad bottom
        p.line(topleft,quadheight,topleft,heighttop) # left quad bottom to top
        p.line(quadlengthleft,linestop,quadheight,linestop) # left inner quad side to left

        #Quad Right TOP
        p.line(righttop,quadheight,righttop,heighttop) #right quad bottom to top
        p.line(right,quadheight,righttop,quadheight) #right quad bottom
        p.line(right,heighttop,right,quadheight) #right outer quad side
        p.line(quadlengthright,heighttop,right,heighttop) #right quad top
        p.line(quadlengthright,linestop,quadlengthright,heighttop) #right inner quad side
        p.line(right,linestop,quadlengthright,linestop) #right inner quad side to right

        #Quad Left BOTTOM
        p.line(left,heightbottom,left,bottomquadheight) # left outer quad side
        p.line(quadlengthleft,heightbottom,quadlengthleft,linesbottom) # left inner quad side
        p.line(left,heightbottom,quadlengthleft,heightbottom) # left quad top
        p.line(left,bottomquadheight,topleft,bottomquadheight) # left quad bottom
        p.line(topleft,bottomquadheight,topleft,heightbottom) # left quad bottom to top
        p.line(quadlengthleft,linesbottom,quadheight,linesbottom) # left inner quad side to left

        #Quad Right BOTTOM
        p.line(righttop,bottomquadheight,righttop,heightbottom) #right quad bottom to top
        p.line(right,bottomquadheight,righttop,bottomquadheight) #right quad bottom
        p.line(right,heightbottom,right,bottomquadheight) #right outer quad side
        p.line(quadlengthright,heightbottom,right,heightbottom) #right quad top
        p.line(quadlengthright,linesbottom,quadlengthright,heightbottom) #right inner quad side
        p.line(right,linesbottom,quadlengthright,linesbottom) #right inner quad side to right


    p.showPage()    
    p.save()
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='certificates.pdf', content_type="application/pdf", as_attachment=True)

def delegate_certificate(request):
    participants = Delegate.objects.all()
    return participant_certificate(request, participants)   

def executives_certificate(request):
    participants = Executive.objects.all()
    return participant_certificate(request, participants) 

def mundirector_certificate(request):
    participants = MUNDirector.objects.all()
    return participant_certificate(request, participants) 

def staff_certificate(request):
    participants = Staff.objects.all()
    return participant_certificate(request, participants)   

def student_officer_certificate(request):
    participants = StudentOfficer.objects.all()
    return participant_certificate(request, participants)   

def participant_certificate(request, participants):
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

    #determine dates of current conference
    conference = Conference.objects.first()
    start_date = conference.start_date
    start_day = start_date.day
    start_month = date(start_date, 'F')
    end_date = conference.end_date
    end_day = end_date.day
    end_month= date(end_date, 'F')
    year = start_date.year
    session = conference.annual_session
    
    
    return _create_certificate(participants = filtered_participants, session=session, year=year, startday=start_day, startmonth=start_month, endday=end_day, endmonth=end_month, secgen="Tom Rix", depsecgen="Tom Rix", cms='Tom Rix & Tom Rix')

