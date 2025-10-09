from django.http import JsonResponse

from api.models import Delegate, MUNDirector, School

def housing_delegates(request):
    '''
    Returns the numbers of each housing option of all delegates
    '''
    hostel = Delegate.objects.filter(school__housing_delegates=School.HOSTEL).count()
    guest_family = Delegate.objects.filter(school__housing_delegates=School.GUEST_FAMILY).count()
    other = Delegate.objects.filter(school__housing_delegates=School.OTHER).count()
    return JsonResponse({"hostel": hostel, "guest_family": guest_family, "other": other})

def housing_mun_directors(request):
    '''
    Returns the numbers of each housing option of all mun directors
    '''
    hostel = MUNDirector.objects.filter(school__housing_mun_directors=School.HOSTEL).count()
    guest_family = MUNDirector.objects.filter(school__housing_mun_directors=School.GUEST_FAMILY).count()
    other = MUNDirector.objects.filter(school__housing_mun_directors=School.OTHER).count()
    return JsonResponse({"hostel": hostel, "guest_family": guest_family, "other": other})

def housing_schools(request):
    '''
    Returns the numbers of each housing option of all schools, only considering the delegates
    '''
    hostel_delegates = School.objects.filter(housing_delegates=School.HOSTEL).count()
    guest_family_delegates = School.objects.filter(housing_delegates=School.GUEST_FAMILY).count()
    other_delegates = School.objects.filter(housing_delegates=School.OTHER).count()
    return JsonResponse({"hostel": hostel_delegates, "guest_family": guest_family_delegates, "other": other_delegates})

def housing_all(request):
    '''
    Returns the numbers of each housing option for delegates and schools (considering only delegates)
    '''
    hostel = Delegate.objects.filter(school__housing_delegates=School.HOSTEL).count()
    guest_family = Delegate.objects.filter(school__housing_delegates=School.GUEST_FAMILY).count()
    other = Delegate.objects.filter(school__housing_delegates=School.OTHER).count()
    delegates = {"hostel": hostel, "guest_family": guest_family, "other": other}

    hostel = MUNDirector.objects.filter(school__housing_mun_directors=School.HOSTEL).count()
    guest_family = MUNDirector.objects.filter(school__housing_mun_directors=School.GUEST_FAMILY).count()
    other = MUNDirector.objects.filter(school__housing_mun_directors=School.OTHER).count()
    mun_directors = {"hostel": hostel, "guest_family": guest_family, "other": other}

    hostel_delegates = School.objects.filter(housing_delegates=School.HOSTEL).count()
    guest_family_delegates = School.objects.filter(housing_delegates=School.GUEST_FAMILY).count()
    other_delegates = School.objects.filter(housing_delegates=School.OTHER).count()
    schools = {"hostel": hostel_delegates, "guest_family": guest_family_delegates, "other": other_delegates}

    return JsonResponse({"delegates": delegates, "mun_directors": mun_directors, "schools": schools})