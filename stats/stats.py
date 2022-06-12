from django.http import JsonResponse
from django.db.models import Avg, Min, Max
from api.models import Advisor, Delegate, Executive, Forum, Issue, MUNDirector, MemberOrganization, Participant, Staff, StudentOfficer

def number_of_forums(request):
    '''
    Returns the numbers of forums
    '''
    return JsonResponse({"number_of_forums":Forum.objects.all().distinct().count()})

def number_of_issues(request):
    '''
    Returns the numbers of issues
    '''
    return JsonResponse({"number_of_issues":Issue.objects.all().distinct().count()})

def number_of_simulated_member_organizations(request):
    '''
    Returns the numbers of simulated member organizations
    '''
    return JsonResponse({"number_of_simulated_member_organizations":MemberOrganization.objects.filter(active=True).distinct().count()})

def number_of_delegates(request):
    '''
    Returns the numbers of delegates
    '''
    return JsonResponse({"number_of_delegates":Delegate.objects.all().distinct().count()})

def number_of_student_officers(request):
    '''
    Returns the numbers of student officers
    '''
    return JsonResponse({"number_of_student_officers":StudentOfficer.objects.all().distinct().count()})

def number_of_mun_directors(request):
    '''
    Returns the numbers of MUN directors
    '''
    return JsonResponse({"number_of_mun_directors":MUNDirector.objects.all().distinct().count()})

def number_of_executives(request):
    '''
    Returns the numbers of executives
    '''
    return JsonResponse({"number_of_executives":Executive.objects.all().distinct().count()})

def number_of_staff(request):
    '''
    Returns the numbers of staff
    '''
    return JsonResponse({"number_of_staff":Staff.objects.all().distinct().count()})

def number_of_advisors(request):
    '''
    Returns the numbers of advisors
    '''
    return JsonResponse({"number_of_advisors":Advisor.objects.all().distinct().count()})


def number_of_participants(request):
    '''
    Returns the numbers of participants
    '''
    return JsonResponse({"number_of_participants":Participant.objects.all().distinct().count()})

def birthday_stats(request):
    '''
    Returns the average, min and max birtday of all participants
    '''
    return JsonResponse({
    "minimum_birthday":Participant.objects.all().aggregate(Min('birthday')),
    "maximum_birthday":Participant.objects.all().aggregate(Max('birthday'))})

def all_stats(request):

    return JsonResponse({"number_of_forums":Forum.objects.all().distinct().count(),
                "number_of_issues":Issue.objects.all().distinct().count(),
                "number_of_simulated_member_organizations":MemberOrganization.objects.filter(active=True).distinct().count(),
                "number_of_delegates":Delegate.objects.all().distinct().count(),
                "number_of_student_officers":StudentOfficer.objects.all().distinct().count(),
                "number_of_mun_directors":MUNDirector.objects.all().distinct().count(),
                "number_of_executives":Executive.objects.all().distinct().count(),
                "number_of_staff":Staff.objects.all().distinct().count(),
                "number_of_advisors":Advisor.objects.all().distinct().count(),
                "number_of_participants":Participant.objects.all().distinct().count(),
                "minimum_birthday":Participant.objects.all().aggregate(Min('birthday')),
                "maximum_birthday":Participant.objects.all().aggregate(Max('birthday'))})

    
