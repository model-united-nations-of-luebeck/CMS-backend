from django.http import JsonResponse

from api.models import Delegate, Executive, Participant, School, Staff, StudentOfficer

def housing_delegates(request):
    '''
    Returns the numbers of each housing option of all delegates
    '''
    hostel = Delegate.objects.filter(school__housing=School.HOSTEL).count()
    guest_family = Delegate.objects.filter(school__housing=School.GUEST_FAMILY).count()
    other = Delegate.objects.filter(school__housing=School.OTHER).count()
    return JsonResponse({"hostel": hostel, "guest_family": guest_family, "other": other})

def housing_schools(request):
    '''
    Returns the numbers of each housing option of all schools
    '''
    hostel = School.objects.filter(housing=School.HOSTEL).count()
    guest_family = School.objects.filter(housing=School.GUEST_FAMILY).count()
    other = School.objects.filter(housing=School.OTHER).count()
    return JsonResponse({"hostel": hostel, "guest_family": guest_family, "other": other})

def housing_all(request):
    '''
    Returns the numbers of each housing option for delegates and schools
    '''
    hostel = Delegate.objects.filter(school__housing=School.HOSTEL).count()
    guest_family = Delegate.objects.filter(school__housing=School.GUEST_FAMILY).count()
    other = Delegate.objects.filter(school__housing=School.OTHER).count()
    delegates = {"hostel": hostel, "guest_family": guest_family, "other": other}

    hostel = School.objects.filter(housing=School.HOSTEL).count()
    guest_family = School.objects.filter(housing=School.GUEST_FAMILY).count()
    other = School.objects.filter(housing=School.OTHER).count()
    schools = {"hostel": hostel, "guest_family": guest_family, "other": other}
    
    return JsonResponse({"delegates": delegates, "schools": schools})