import io
from wsgiref.util import FileWrapper

from django.http import FileResponse
from django.template.defaultfilters import date
from django.db.models.functions import Reverse
from api.models import Conference, Delegate, Executive, Forum, MUNDirector, Staff, StudentOfficer
from api.permissions import IsOrganizer, IsAdmin
from rest_framework.decorators import api_view, permission_classes

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm

from pdfs.utils import _register_MUNOL_fonts, _get_transparent_background_logo, _get_fitting_font_size, _filter_queryset_by_uuid
_register_MUNOL_fonts()

        
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

def _create_certificates(participants:list = [], session=1, year=1998, start_day:str='',start_month:str='', end_day:str='', end_month:str='', names: str='', positions: str='', signatures:str = '', duration_days: str = '', number_of_delegates: int = 0, number_of_origin_nations: str = '', number_of_forums: str = ''):
    
    logo = _get_transparent_background_logo()
    
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=portrait(A4))
    c.setTitle("Certificates")
    c.setAuthor("MUNOL")
    c.setSubject("Certificate for MUNOL")
    c.setCreator("MUNOL CMS")
    c.setProducer("MUNOL CMS")
    
    for participant in participants:
        
        #logo in background
        margin = 25
        c.drawImage(logo, margin/2*mm,A4[1]/2- (A4[0]-margin*mm)/2,A4[0]-margin*mm,A4[0]-margin*mm, mask='auto')

        c.setFont('Times-Roman-Small-Caps-Bold', 28)
        c.drawCentredString(A4[0]/2,A4[1]-27*mm,'Certificate of Participation')

        if type(participant) == Delegate:
            c.setFont('Times-Bold', 17)
            c.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            c.drawCentredString(A4[0]/2,A4[1]-75*mm,'has attended the')

            text_object = c.beginText()
            text_object.setTextOrigin(A4[0]/2-36*mm,A4[1]-95*mm)
            
            text_object.textOut(_num2roman(session))
            text_object.setRise(4)
            text_object.textOut(ordinal(session))
            text_object.setRise(0)
            text_object.textOut(' annual session of the')
            c.drawText(text_object)

            c.setFont('Times-Bold', 24)
            c.drawCentredString(A4[0]/2,A4[1]-110*mm,'Model United Nations of Lübeck')

            c.drawCentredString(A4[0]/2,A4[1]-130*mm,f'{start_day} {start_month} - {end_day} {end_month} {year}')

            c.setFont('Times-Bold', 17)
            delegate = 'Ambassador' if participant.ambassador else 'Delegate'
            c.drawCentredString(A4[0]/2,A4[1]-160*mm,f'as the {delegate} of the')
            c.drawCentredString(A4[0]/2,A4[1]-188*mm,'in the')
            c.drawCentredString(A4[0]/2,A4[1]-210*mm,'and is hereby awarded this certificate.')

            c.setFont('Times-Bold', 20)
            c.drawCentredString(A4[0]/2,A4[1]-172*mm, participant.represents.official_name)
            c.drawCentredString(A4[0]/2,A4[1]-198*mm, participant.forum.name)

            c.setFont('CenturyGothicBold', 20)
            c.drawCentredString(A4[0]/2,A4[1]-65*mm, f'{participant.first_name} {participant.last_name}')

            
        if type(participant) == StudentOfficer:
            c.setFont('Times-Roman', 16)
            c.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            c.drawCentredString(A4[0]/2,A4[1]-70*mm,'has successfully participated in')
            c.drawCentredString(A4[0]/2,A4[1]-80*mm,f'the Model United Nations of Lübeck Conference {year} as')
            c.drawCentredString(A4[0]/2,A4[1]-90*mm, f"{participant.position_name}.")

            c.drawCentredString(A4[0]/2,A4[1]-150*mm, "Model United Nations of Lübeck is a simulation conference of the United Nations")
            c.drawCentredString(A4[0]/2,A4[1]-160*mm, "with the goal of encouraging young people's interest for international politics, of")
            c.drawCentredString(A4[0]/2,A4[1]-170*mm, f"ameliorating rhetorical skills and of motivating them to debate. For {duration_days} days,")
            c.drawCentredString(A4[0]/2,A4[1]-180*mm, f"over {number_of_delegates} people of {number_of_origin_nations} nations debated in {number_of_forums} forums on")
            c.drawCentredString(A4[0]/2,A4[1]-190*mm, "political issues of international relevance.")

            c.drawCentredString(A4[0]/2,A4[1]-210*mm, "A Student Officer is responsible for one of the different bodies simulated, is")
            c.drawCentredString(A4[0]/2,A4[1]-220*mm, "chairing the debates, is part of the organisation team and one of the most")
            c.drawCentredString(A4[0]/2,A4[1]-230*mm, "important representatives of the conference.")

            c.setFont('Times-Italic', 20)
            c.drawCentredString(A4[0]/2,A4[1]-60*mm,f'{participant.first_name} {participant.last_name}')

            
        if type(participant) == Executive:
            c.setFont('Times-Bold', 17)
            c.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            c.drawCentredString(A4[0]/2,A4[1]-75*mm,'has attended the')

            text_object = c.beginText()
            text_object.setTextOrigin(A4[0]/2-36*mm,A4[1]-95*mm)
            
            text_object.textOut(_num2roman(session))
            text_object.setRise(4)
            text_object.textOut(ordinal(session))
            text_object.setRise(0)
            text_object.textOut(' annual session of the')
            c.drawText(text_object)

            c.setFont('Times-Bold', 24)
            c.drawCentredString(A4[0]/2,A4[1]-110*mm,'Model United Nations of Lübeck')

            c.drawCentredString(A4[0]/2,A4[1]-130*mm,f'{start_day} {start_month} - {end_day} {end_month} {year}')

            c.setFont('Times-Bold', 17)
            c.drawCentredString(A4[0]/2,A4[1]-160*mm,f'as the')
            c.drawCentredString(A4[0]/2,A4[1]-188*mm,'in the')
            c.drawCentredString(A4[0]/2,A4[1]-210*mm,'and is hereby awarded this certificate.')

            c.setFont('Times-Bold', 20)
            c.drawCentredString(A4[0]/2,A4[1]-172*mm, participant.position_name)
            c.drawCentredString(A4[0]/2,A4[1]-198*mm, "Executive Staff Team")

            c.setFont('CenturyGothicBold', 20)
            c.drawCentredString(A4[0]/2,A4[1]-65*mm, f'{participant.first_name} {participant.last_name}')

            
        if type(participant) == Staff:
            c.setFont('Times-Bold', 17)
            c.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            c.drawCentredString(A4[0]/2,A4[1]-75*mm,'has attended the')

            text_object = c.beginText()
            text_object.setTextOrigin(A4[0]/2-36*mm,A4[1]-95*mm)
            
            text_object.textOut(_num2roman(session))
            text_object.setRise(4)
            text_object.textOut(ordinal(session))
            text_object.setRise(0)
            text_object.textOut(' annual session of the')
            c.drawText(text_object)

            c.setFont('Times-Bold', 24)
            c.drawCentredString(A4[0]/2,A4[1]-110*mm,'Model United Nations of Lübeck')

            c.drawCentredString(A4[0]/2,A4[1]-130*mm,f'{start_day} {start_month} - {end_day} {end_month} {year}')

            c.setFont('Times-Bold', 17)
            c.drawCentredString(A4[0]/2,A4[1]-160*mm,f'as')
            c.drawCentredString(A4[0]/2,A4[1]-188*mm,'in the')
            c.drawCentredString(A4[0]/2,A4[1]-210*mm,'and is hereby awarded this certificate.')

            c.setFont('Times-Bold', 20)
            c.drawCentredString(A4[0]/2,A4[1]-172*mm, participant.position_name)
            c.drawCentredString(A4[0]/2,A4[1]-198*mm, "Staff Team")

            c.setFont('CenturyGothicBold', 20)
            c.drawCentredString(A4[0]/2,A4[1]-65*mm, f'{participant.first_name} {participant.last_name}')


        if type(participant) == MUNDirector:
            c.setFont('Times-Bold', 17)
            c.drawCentredString(A4[0]/2,A4[1]-50*mm,'This is to certify that')

            c.drawCentredString(A4[0]/2,A4[1]-75*mm,'has attended the')

            text_object = c.beginText()
            text_object.setTextOrigin(A4[0]/2-36*mm,A4[1]-95*mm)
            
            text_object.textOut(_num2roman(session))
            text_object.setRise(4)
            text_object.textOut(ordinal(session))
            text_object.setRise(0)
            text_object.textOut(' annual session of the')
            c.drawText(text_object)

            c.setFont('Times-Bold', 24)
            c.drawCentredString(A4[0]/2,A4[1]-110*mm,'Model United Nations of Lübeck')

            c.drawCentredString(A4[0]/2,A4[1]-130*mm,f'{start_day} {start_month} - {end_day} {end_month} {year}')

            c.setFont('Times-Bold', 17)
            c.drawCentredString(A4[0]/2,A4[1]-160*mm,f'as')
            c.drawCentredString(A4[0]/2,A4[1]-188*mm,'and is hereby awarded this certificate.')

            c.setFont('Times-Bold', 20)
            c.drawCentredString(A4[0]/2,A4[1]-172*mm, 'MUN-Director')

            c.setFont('CenturyGothicBold', 20)
            c.drawCentredString(A4[0]/2,A4[1]-65*mm, f'{participant.first_name} {participant.last_name}')

        #signatures
        margin_side  = 20*mm
        margin_bottom = 40*mm
        width = 60*mm

        c.setLineWidth(0.5*mm)
        c.line(A4[0]/2-width,margin_bottom, A4[0]/2+width, margin_bottom)

        c.setFont('Times-Bold', 16)
        c.drawCentredString(A4[0]/2,33*mm,names)

        c.setFont('Times-Bold', 10)
        c.drawCentredString(A4[0]/2,28*mm,f'({positions})')

        if signatures != '':
            c.drawImage(signatures, A4[0]/2,width, 2*width, anchorAtXY=True, preserveAspectRatio=True, mask='auto')
            
            

        #variables for lines in frame
        height_top = 2*mm
        topleft = 11.5*mm
        left = 6*mm
        inner_border_strength = 2*mm

        line_stop = topleft-4*mm

        lines_bottom = A4[1]-line_stop
        right_top = A4[0]-topleft
        quad_height = height_top+4*mm
        quad_length_left = left+4*mm
        quad_length_right = A4[0]-quad_length_left
        right = A4[0]-left
        height_bottom = A4[1]-height_top
        bottom_quad_height = A4[1]-quad_height

        inner_left = left+2*mm
        inner_right = A4[0] - inner_left
        inner_top = height_top +1*mm
        inner_bottom = (A4[1]- inner_top) -1*mm
        inner_top_pos = inner_top + (inner_border_strength/2)

        # defines inner line
        c.setLineWidth(inner_border_strength)
        c.setStrokeColorRGB(68/255, 72/255, 143/255)
        c.setLineCap(2) #round
        c.line(inner_left,inner_top_pos,inner_right,inner_top_pos) #bottom 
        c.line(inner_right,inner_top_pos,inner_right,inner_bottom) #right
        c.line(inner_left,inner_top_pos,inner_left,inner_bottom) #left
        c.line(inner_left,inner_bottom,inner_right,inner_bottom) #top


        # defines outer line
        
        c.setLineWidth(0.5*mm)
        c.setStrokeColorRGB(0,0,0)
        c.line(topleft, height_top, right_top, height_top)  # top
        c.line(right, line_stop, right, lines_bottom)  #right
        c.line(left, line_stop, left, lines_bottom)  #left
        c.line(topleft, height_bottom, right_top, height_bottom)  # bottom

        #Quad Left TOP
        c.line(left,height_top,left,quad_height) # left outer quad side
        c.line(quad_length_left,height_top,quad_length_left,line_stop) # left inner quad side
        c.line(left,height_top,quad_length_left,height_top) # left quad top
        c.line(left,quad_height,topleft,quad_height) # left quad bottom
        c.line(topleft,quad_height,topleft,height_top) # left quad bottom to top
        c.line(quad_length_left,line_stop,quad_height,line_stop) # left inner quad side to left

        #Quad Right TOP
        c.line(right_top,quad_height,right_top,height_top) #right quad bottom to top
        c.line(right,quad_height,right_top,quad_height) #right quad bottom
        c.line(right,height_top,right,quad_height) #right outer quad side
        c.line(quad_length_right,height_top,right,height_top) #right quad top
        c.line(quad_length_right,line_stop,quad_length_right,height_top) #right inner quad side
        c.line(right,line_stop,quad_length_right,line_stop) #right inner quad side to right

        #Quad Left BOTTOM
        c.line(left,height_bottom,left,bottom_quad_height) # left outer quad side
        c.line(quad_length_left,height_bottom,quad_length_left,lines_bottom) # left inner quad side
        c.line(left,height_bottom,quad_length_left,height_bottom) # left quad top
        c.line(left,bottom_quad_height,topleft,bottom_quad_height) # left quad bottom
        c.line(topleft,bottom_quad_height,topleft,height_bottom) # left quad bottom to top
        c.line(quad_length_left,lines_bottom,quad_height,lines_bottom) # left inner quad side to left

        #Quad Right BOTTOM
        c.line(right_top,bottom_quad_height,right_top,height_bottom) #right quad bottom to top
        c.line(right,bottom_quad_height,right_top,bottom_quad_height) #right quad bottom
        c.line(right,height_bottom,right,bottom_quad_height) #right outer quad side
        c.line(quad_length_right,height_bottom,right,height_bottom) #right quad top
        c.line(quad_length_right,lines_bottom,quad_length_right,height_bottom) #right inner quad side
        c.line(right,lines_bottom,quad_length_right,lines_bottom) #right inner quad side to right


        c.showPage()    
    c.save()
    buffer.seek(0)
    return FileResponse(FileWrapper(buffer), filename='certificates.pdf', content_type="application/pdf", as_attachment=False)

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def delegate_certificates(request):
    participants = Delegate.objects
    participants = _filter_queryset_by_uuid(participants, request)
    participants = participants.order_by('school')
    return participant_certificates(request, participants)   

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def executive_certificates(request):
    participants = Executive.objects
    participants = _filter_queryset_by_uuid(participants, request)
    participants = participants.annotate(reverse_position_name=Reverse('position_name')).order_by('reverse_position_name')
    return participant_certificates(request, participants) 

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def mun_director_certificates(request):
    participants = MUNDirector.objects
    participants = _filter_queryset_by_uuid(participants, request)
    participants = participants.order_by('school')
    return participant_certificates(request, participants) 

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def staff_certificates(request):
    participants = Staff.objects
    participants = _filter_queryset_by_uuid(participants, request)
    participants = participants.order_by('position_name')
    return participant_certificates(request, participants)   

@api_view(["POST"])
@permission_classes([IsOrganizer|IsAdmin])
def student_officer_certificates(request):
    participants = StudentOfficer.objects
    participants = _filter_queryset_by_uuid(participants, request)
    participants = participants.annotate(reverse_position_name=Reverse('position_name')).order_by('reverse_position_name')
    return participant_certificates(request, participants)   

def participant_certificates(request, participants):

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

    # student officer extra information
    day_count = end_date.day - start_date.day + 1
    number_words = {
        1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
        16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
        21: "twenty-one", 22: "twenty-two", 23: "twenty-three", 24: "twenty-four", 25: "twenty-five",
        26: "twenty-six", 27: "twenty-seven", 28: "twenty-eight", 29: "twenty-nine", 30: "thirty",
        31: "thirty-one",
    }
    duration_days = number_words.get(day_count, str(day_count))
    number_of_delegates = Delegate.objects.count()
    number_of_origin_nations = Delegate.objects.values_list('school__country', flat=True).distinct().count()
    number_of_origin_nations = number_words.get(number_of_origin_nations, str(number_of_origin_nations))
    number_of_forums = Forum.objects.count()
    number_of_forums = number_words.get(number_of_forums, str(number_of_forums))

    # signatures
    names = request.data.get('names', '') 
    positions = request.data.get('positions', '') 
    signatures = request.data.get('signatures', '')
    
    return _create_certificates(participants = participants, session=session, year=year, start_day=start_day, start_month=start_month, end_day=end_day, end_month=end_month, names=names, positions=positions, signatures=signatures, duration_days=duration_days, number_of_delegates=number_of_delegates, number_of_origin_nations=number_of_origin_nations, number_of_forums=number_of_forums)
