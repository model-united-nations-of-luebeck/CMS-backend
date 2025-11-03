from django.http import JsonResponse

from api.models import Delegate, Forum

def first_time_delegates_per_forum(request):
    '''
    Returns the numbers of first time delegates and total number of delegates per forum
    '''
    forums = Forum.objects.all()
    result = {}
    for forum in forums:
        first_time_count = Delegate.objects.filter(first_timer=True, forum=forum).count()
        total_count = Delegate.objects.filter(forum=forum).count()
        result[forum.name] = {"first_time": first_time_count, "total": total_count, "abbreviation": forum.abbreviation}
    return JsonResponse(result)
