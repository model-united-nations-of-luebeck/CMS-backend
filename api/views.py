from django.shortcuts import render
from rest_framework import generics # generic views for RUD, LC views

from api.serializers import ConferenceSerializer
from api.models import Conference

#For single conferences
class ConferenceRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ConferenceSerializer

    def get_queryset(self):
        return Conference.objects.all()

#For creating and showing all conferences
class ConferenceLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = ConferenceSerializer

    def get_queryset(self):
        return Conference.objects.all()        
