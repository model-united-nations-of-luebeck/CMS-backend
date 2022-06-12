from django.http import JsonResponse

from api.models import Participant

def diet(request):
    '''
    Returns the numbers of each lunch diet option
    '''
    meat = Participant.objects.filter(diet=Participant.MEAT).count()
    vegetarian = Participant.objects.filter(diet=Participant.VEGETARIAN).count()
    vegan = Participant.objects.filter(diet=Participant.VEGAN).count()
    return JsonResponse({"meat": meat, "vegetarian": vegetarian, "vegan": vegan})
