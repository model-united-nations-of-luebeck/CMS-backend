from django.urls import path
from . import placards, badges, certificates

app_name = 'pdfs'

urlpatterns = [
    path('placards', placards.placards, name="placards"),
    path('custom_placard', placards.custom_placard, name="custom placard"),
    path('executive_placards', placards.executive_placards, name="executive placard"),
    path('student_officer_placards', placards.student_officer_placards, name="student officer placard"),

    path('advisor_badge', badges.advisor_badge, name="advisor badges"),
    path('executive_badge', badges.executive_badge, name="executive_badge badges"),
    path('delegate_badge', badges.delegate_badge, name="delegate_badge badges"),
    path('staff_badge', badges.staff_badge, name="staff_badge badges"),
    path('student_officer_badge', badges.student_officer_badge, name="student_officer_badge badges"),
    path('mundirector_badge', badges.mundirector_badge, name="mundirector_badge badges"),
    path('custom_badge', badges.custom_badge, name="custom badges"),

    path('delegate_certificate', certificates.delegate_certificate, name="delegate certificate"),
    path('student_officer_certificate', certificates.student_officer_certificate, name="student officer certificate"),
    path('executive_certificate', certificates.executives_certificate, name="executive certificate"),
    path('staff_certificate', certificates.staff_certificate, name="staff certificate"),
    path('mundirector_certificate', certificates.mundirector_certificate, name="mundirector certificate"),
]

