from django.urls import path
from . import placards, badges, certificates, roll_call_lists, signs

app_name = 'pdfs'

urlpatterns = [
    path('delegate_placards_forum', placards.delegate_placards_forum, name="delegate placards forum"),
    path('delegate_placards_plenary', placards.delegate_placards_plenary, name="delegate placards plenary"),
    path('delegate_placards_ceremony', placards.delegate_placards_ceremony, name="delegate placards ceremony"),
    path('custom_placard', placards.custom_placard, name="custom placard"),
    path('executive_placards', placards.executive_placards, name="executive placard"),
    path('student_officer_placards', placards.student_officer_placards, name="student officer placard"),

    path('advisor_badges', badges.advisor_badges, name="advisor badges"),
    path('executive_badges', badges.executive_badges, name="executive badges"),
    path('delegate_badges', badges.delegate_badges, name="delegate badges"),
    path('staff_badges', badges.staff_badges, name="staff badges"),
    path('student_officer_badges', badges.student_officer_badges, name="student officer badges"),
    path('mun_director_badges', badges.mun_director_badges, name="mun_director badges"),
    path('custom_badge', badges.custom_badge, name="custom badge"),

    path('delegate_certificate', certificates.delegate_certificate, name="delegate certificate"),
    path('student_officer_certificate', certificates.student_officer_certificate, name="student officer certificate"),
    path('executive_certificate', certificates.executives_certificate, name="executive certificate"),
    path('staff_certificate', certificates.staff_certificate, name="staff certificate"),
    path('mundirector_certificate', certificates.mundirector_certificate, name="mundirector certificate"),

    path('forum_roll_call_list', roll_call_lists.forum_roll_call_list, name="forum roll call list"),

    path('sign', signs.sign, name="sign"),
]
