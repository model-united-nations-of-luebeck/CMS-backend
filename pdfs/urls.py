from django.urls import path

from .lists import lists, executives_list, student_officer_list, advisors_list, staffs_list, mun_directors_list, roll_call_list_forums, roll_call_list_plenaries, registration_list, participants_list, allergy_list
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
    path('issues_list', lists.issues_list, name="issues list"),
    path('schools_list', lists.schools_list, name="schools list"),
    path('executives_list', executives_list.executives_list, name="executives list"),
    path('student_officers_list', student_officer_list.student_officers_list, name="student officer list"),
    path('advisors_list', advisors_list.advisors_list, name="advisors list"),
    path('staffs_list', staffs_list.staffs_list, name="staffs list"),
    path('mun_directors_list', mun_directors_list.mun_directors_list, name="mun directors list"),
    path('roll_call_list_forums', roll_call_list_forums.roll_call_list_forums, name="roll call list forums"),
    path('roll_call_list_plenaries', roll_call_list_plenaries.roll_call_list_plenaries, name="roll call list plenaries"),
    path('registration_list', registration_list.registration_list, name="registration list"),
    path('participants_list', participants_list.participants_list, name="participants list"),
    path('allergy_list', allergy_list.allergy_list, name="allergy list"),

    path('sign', signs.sign, name="sign"),
]
