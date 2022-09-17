from tracemalloc import start
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta

from api.models import Advisor, Conference, Delegate, Executive, MUNDirector, Participant, Staff, StudentOfficer

def _get_age_counts(group) -> dict:
    '''
    From a Participant (sub)class, return the age groups counts as dictionary
    '''
    start_date = Conference.objects.first().startdate
    not_defined = group.objects.filter(birthday__isnull=True).count()
    under_16 = group.objects.filter(birthday__gt=start_date - relativedelta(years=16)).count()
    middle = group.objects.filter(birthday__lte=start_date - relativedelta(years=16),birthday__gt=start_date - relativedelta(years=18)).count()
    over_18 = group.objects.filter(birthday__lte=start_date - relativedelta(years=18)).count()
    return {"not defined": not_defined, "under_16": under_16, "16_to_18": middle, "over_18": over_18}

def age_participants(request):
    '''
    Returns the numbers of each age groups of all participants
    '''
    return JsonResponse(_get_age_counts(Participant))

def age_delegates(request):
    '''
    Returns the numbers of each age groups of all delegates
    '''
    return JsonResponse(_get_age_counts(Delegate))

def age_student_officers(request):
    '''
    Returns the numbers of each age groups of all student officers
    '''
    return JsonResponse(_get_age_counts(StudentOfficer))

def age_staff(request):
    '''
    Returns the numbers of each age groups of all staff
    '''
    return JsonResponse(_get_age_counts(Staff))

def age_executives(request):
    '''
    Returns the numbers of each age groups of all executives
    '''
    return JsonResponse(_get_age_counts(Executive))

def age_mundirectors(request):
    '''
    Returns the numbers of each age groups of all MUN Directors
    '''
    return JsonResponse(_get_age_counts(MUNDirector))

def age_advisors(request):
    '''
    Returns the numbers of each age groups of all advisors
    '''
    return JsonResponse(_get_age_counts(Advisor))

def age_all(request):
    '''
    Returns the numbers of each age groups for each participant group
    '''
    response = {}
    groups = [Participant, Delegate, StudentOfficer, Staff, Executive, MUNDirector, Advisor]
    for group in groups:
        response[group.__name__.lower()] = _get_age_counts(group)
    return JsonResponse(response)

def birthdays_during_conference(request):
    '''
    Returns the persons and dates of participants how have birthday during the conference
    '''
    conference = Conference.objects.first()
    start_date = conference.startdate
    end_date = conference.enddate
    conference_days = [start_date+relativedelta(days=x) for x in range((end_date - start_date).days+1)]
    
    birthdays = []
    for day in conference_days:
        participants = Participant.objects.filter(birthday__day=day.day, birthday__month=day.month)
        for participant in participants:
            birthdays.append({"name":f"{participant.first_name} {participant.last_name}", 
                              "date": day,
                              "id": participant.id})
    
    return JsonResponse({"birthdays":birthdays})

