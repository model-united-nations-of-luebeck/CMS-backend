from django.urls import path
from .placards import placards, custom_placard, executive_placards, student_officer_placards
from .badges import advisor_badge, executive_badge, delegate_badge, staff_badge, student_officer_badge, mundirector_badge, custom_badge
from .certificates import delegate_certificate, student_officer_certificate, executives_certificate, staff_certificate, mundirector_certificate
from .roll_call_lists import forum_roll_call_list
from .signs import sign

app_name = 'pdfs'

urlpatterns = [
    path('placards', placards, name="placards"),
    path('custom_placard', custom_placard, name="custom placard"),
    path('executive_placards', executive_placards, name="executive placard"),
    path('student_officer_placards', student_officer_placards, name="student officer placard"),

    path('advisor_badge', advisor_badge, name="advisor badges"),
    path('executive_badge', executive_badge, name="executive_badge badges"),
    path('delegate_badge', delegate_badge, name="delegate_badge badges"),
    path('staff_badge', staff_badge, name="staff_badge badges"),
    path('student_officer_badge', student_officer_badge, name="student_officer_badge badges"),
    path('mundirector_badge', mundirector_badge, name="mundirector_badge badges"),
    path('custom_badge', custom_badge, name="custom badges"),

    path('delegate_certificate', delegate_certificate, name="delegate certificate"),
    path('student_officer_certificate', student_officer_certificate, name="student officer certificate"),
    path('executive_certificate', executives_certificate, name="executive certificate"),
    path('staff_certificate', staff_certificate, name="staff certificate"),
    path('mundirector_certificate', mundirector_certificate, name="mundirector certificate"),

    path('forum_roll_call_list', forum_roll_call_list, name="forum roll call list"),

    path('signs', sign, name="signs"),
]

