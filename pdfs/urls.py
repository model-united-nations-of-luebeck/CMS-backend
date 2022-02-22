from django.urls import path
from . import views

app_name = 'pdfs'

urlpatterns = [
    path('placards', views.placards, name="placards"),
    path('custom_placard', views.custom_placard, name="custom placard"),
    path('executive_placards', views.executive_placards, name="executive placard"),
    path('student_officer_placards', views.student_officer_placards, name="student officer placard")
]

