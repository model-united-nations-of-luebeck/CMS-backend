from django.http import HttpResponseBadRequest
from django.urls import path
from . import gender, age, first_time_delegates, origin, housing, stats

app_name = 'stats'

urlpatterns = [
    path('gender_participants', gender.gender_participants, name="gender_participants"),
    path('gender_delegates', gender.gender_delegates, name="gender_delegates"),
    path('gender_student_officers', gender.gender_student_officers, name="gender_student_officers"),
    path('gender_staff', gender.gender_staff, name="gender_staff"),
    path('gender_executives', gender.gender_executives, name="gender_executives"),
    path('gender_all', gender.gender_all, name="gender_all"),


    path('age_counts_participants', age.age_participants, name="age_counts_participants"),
    path('age_counts_delegates', age.age_delegates, name="age_counts_delegates"),
    path('age_counts_student_officers', age.age_student_officers, name="age_counts_student_officers"),
    path('age_counts_staff', age.age_staff, name="age_counts_staff"),
    path('age_counts_executives', age.age_executives, name="age_counts_executives"),
    path('age_counts_mundirectors', age.age_mundirectors, name="age_counts_mundirectors"),
    path('age_counts_advisors', age.age_advisors, name="age_counts_advisors"),
    path('age_counts_all', age.age_all, name="age_counts_all"),

    path('birthdays_during_conference', age.birthdays_during_conference, name="birthdays_during_conference"),

    path('origin_delegates', origin.origin_delegates, name="origin_delegates"),
    path('origin_mun_directors', origin.origin_mun_directors, name="origin_mun_directors"),
    path('origin_schools', origin.origin_schools, name="origin_schools"),
    path('origin_all', origin.origin_all, name="origin_all"),
    path('delegates_from_countries', origin.delegates_from_countries, name="delegates_from_countries"),

    path('housing_all', housing.housing_all, name="housing_all"),
    path('housing_delegates', housing.housing_delegates, name="housing_delegates"),
    path('housing_mun_directors', housing.housing_mun_directors, name="housing_mun_directors"),
    path('housing_schools', housing.housing_schools, name="housing_schools"),

    path('number_of_forums', stats.number_of_forums, name="number_of_forums"),
    path('number_of_issues', stats.number_of_issues, name="number_of_issues"),
    path('number_of_simulated_member_organizations', stats.number_of_simulated_member_organizations, name="number_of_simulated_member_organizations"),
    path('number_of_delegates', stats.number_of_delegates, name="number_of_delegates"),
    path('number_of_student_officers', stats.number_of_student_officers, name="number_of_student_officers"),
    path('number_of_mun_directors', stats.number_of_mun_directors, name="number_of_mun_directors"),
    path('number_of_executives', stats.number_of_executives, name="number_of_executives"),
    path('number_of_staff', stats.number_of_staff, name="number_of_staff"),
    path('number_of_advisors', stats.number_of_advisors, name="number_of_advisors"),
    path('number_of_participants', stats.number_of_participants, name="number_of_participants"),
    path('birthday_stats', stats.birthday_stats, name="birthday_stats"),
    path('all_stats', stats.all_stats, name="all_stats"),

    path('first_time_delegates_per_forum', first_time_delegates.first_time_delegates_per_forum, name="first_time_delegates_per_forum"),
]

