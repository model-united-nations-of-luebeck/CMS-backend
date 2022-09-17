from django.http import JsonResponse
from django.db.models import Count
from api.models import Delegate, MUNDirector, School

def _get_origin_counts(group) -> dict:
    '''
    From delegates or MUN Directors, return the origin counts as dictionary
    '''
    
    # TMS
    queryset = group.objects.all()
    names = ['Thomas', 'Mann']
    for name in names:
        queryset = queryset.filter(school__name__icontains=name)
    tms = queryset.count()

    # Lübeck
    names = ['Lübeck', 'Luebeck', 'HL']
    luebeck = 0
    # for name in names:
    #     queryset = group.objects.all()
    #     queryset = queryset.filter(school__city__icontains=name)
    #     luebeck += queryset.count()
    # luebeck = luebeck - tms

    # Germany
    names = ["Germany", "Deutschland"]
    national = 0
    for name in names:
        queryset = group.objects.all()
        queryset = queryset.filter(school__country__icontains=name)
        national += queryset.count()
    national = national - luebeck - tms

    # International
    international = group.objects.all().count() - national - luebeck - tms

    return {"tms": tms, "luebeck":luebeck, "national": national, "international": international}

def _get_origin_counts_school() -> dict:
    '''
    From delegates or MUN Directors, return the origin counts as dictionary
    '''
    
    # TMS
    queryset = School.objects.all()
    names = ['Thomas', 'Mann']
    for name in names:
        queryset = queryset.filter(name__icontains=name)
    tms = queryset.count()

    # Lübeck
    names = ['Lübeck', 'Luebeck', 'HL']
    luebeck = 0
    # for name in names:
    #     queryset = School.objects.all()
    #     queryset = queryset.filter(city__icontains=name)
    #     luebeck += queryset.count()
    # luebeck = luebeck - tms

    # Germany
    names = ["Germany", "Deutschland"]
    national = 0
    for name in names:
        queryset = School.objects.all()
        queryset = queryset.filter(country__icontains=name)
        national += queryset.count()
    national = national - luebeck - tms

    # International
    international = School.objects.all().count() - national - luebeck - tms

    return {"tms": tms, "luebeck":luebeck, "national": national, "international": international}

def origin_delegates(request):
    '''
    Returns the numbers of each origin of all delegates
    '''
    return JsonResponse(_get_origin_counts(Delegate))

def origin_mun_directors(request):
    '''
    Returns the numbers of each origin of all MUN Directors
    '''
    return JsonResponse(_get_origin_counts(MUNDirector))

def origin_schools(request):
    '''
    Returns the numbers of each origin of all schools
    '''
    return JsonResponse(_get_origin_counts_school())


def origin_all(request):
    '''
    Returns the numbers of each origin for each participant group
    '''
    response = {}
    groups = [Delegate, MUNDirector]
    for group in groups:
        response[group.__name__.lower()] = _get_origin_counts(group)
    response['school'] = _get_origin_counts_school()
    return JsonResponse(response)

def delegates_from_countries(request):
    '''
    Returns the numbers of delegates from each unique country
    '''
    queryset = Delegate.objects.all().values('school__country').annotate(total=Count('school__country'))
    return JsonResponse({"origin": list(queryset)})
