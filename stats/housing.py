from django.http import JsonResponse

from api.models import Delegate, Executive, Participant, School, Staff, StudentOfficer

def housing_delegates(request):
    '''
    Returns the numbers of each housing option of all delegates
    '''
    hostel = Delegate.objects.filter(school__housing_delegates=School.HOSTEL).count()
    guest_family = Delegate.objects.filter(school__housing_delegates=School.GUEST_FAMILY).count()
    other = Delegate.objects.filter(school__housing_delegates=School.OTHER).count()
    return JsonResponse({"hostel": hostel, "guest_family": guest_family, "other": other})

def housing_schools(request):
    '''
    Returns the numbers of each housing option of all schools
    '''
    hostel_delegates = School.objects.filter(housing_delegates=School.HOSTEL).count()
    guest_family_delegates = School.objects.filter(housing_delegates=School.GUEST_FAMILY).count()
    other_delegates = School.objects.filter(housing_delegates=School.OTHER).count()
    hostel_mun_directors = School.objects.filter(housing_mun_directors=School.HOSTEL).count()
    guest_family_mun_directors = School.objects.filter(housing_mun_directors=School.GUEST_FAMILY).count()
    other_mun_directors = School.objects.filter(housing_mun_directors=School.OTHER).count()
    return JsonResponse({"hostel": hostel_delegates + hostel_mun_directors, "guest_family": guest_family_delegates+ guest_family_mun_directors, "other": other_delegates + other_mun_directors})

def housing_all(request):
    '''
    Returns the numbers of each housing option for delegates and schools
    '''
    hostel = Delegate.objects.filter(school__housing_delegates=School.HOSTEL).count()
    guest_family = Delegate.objects.filter(school__housing_delegates=School.GUEST_FAMILY).count()
    other = Delegate.objects.filter(school__housing_delegates=School.OTHER).count()
    delegates = {"hostel": hostel, "guest_family": guest_family, "other": other}

    hostel_delegates = School.objects.filter(housing_delegates=School.HOSTEL).count()
    guest_family_delegates = School.objects.filter(housing_delegates=School.GUEST_FAMILY).count()
    other_delegates = School.objects.filter(housing_delegates=School.OTHER).count()
    hostel_mun_directors = School.objects.filter(housing_mun_directors=School.HOSTEL).count()
    guest_family_mun_directors = School.objects.filter(housing_mun_directors=School.GUEST_FAMILY).count()
    other_mun_directors = School.objects.filter(housing_mun_directors=School.OTHER).count()
    schools = {"hostel": hostel_delegates + hostel_mun_directors, "guest_family": guest_family_delegates+ guest_family_mun_directors, "other": other_delegates + other_mun_directors}
    
    return JsonResponse({"delegates": delegates, "schools": schools})