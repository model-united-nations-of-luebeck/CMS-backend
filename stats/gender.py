from django.http import JsonResponse

from api.models import Delegate, Executive, Participant, Staff, StudentOfficer

def _get_gender_counts(group) -> dict:
    '''
    From a Participant (sub)class, return the gender counts as dictionary
    '''
    male = group.objects.filter(gender=Participant.MALE).count()
    female = group.objects.filter(gender=Participant.FEMALE).count()
    other = group.objects.filter(gender=Participant.OTHER).count()
    return {"male": male, "female":female, "other": other}

def gender_participants(request):
    '''
    Returns the numbers of each gender of all participants
    '''
    return JsonResponse(_get_gender_counts(Participant))

def gender_delegates(request):
    '''
    Returns the numbers of each gender of all delegates
    '''
    return JsonResponse(_get_gender_counts(Delegate))

def gender_student_officers(request):
    '''
    Returns the numbers of each gender of all student officers
    '''
    return JsonResponse(_get_gender_counts(StudentOfficer))

def gender_staff(request):
    '''
    Returns the numbers of each gender of all staff
    '''
    return JsonResponse(_get_gender_counts(Staff))

def gender_executives(request):
    '''
    Returns the numbers of each gender of all executives
    '''
    return JsonResponse(_get_gender_counts(Executive))

def gender_all(request):
    '''
    Returns the numbers of each gender for each participant group
    '''
    response = {}
    groups = [Participant, Delegate, StudentOfficer, Staff, Executive]
    for group in groups:
        response[group.__name__.lower()] = _get_gender_counts(group)
    return JsonResponse(response)