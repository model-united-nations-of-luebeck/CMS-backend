from django.urls import path

from api.mobile_app.views import *

urlpatterns = [
    path('request_code/', RequestLoginCodeView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify/', VerifyView.as_view()),
    path('login_problem/', LoginProblemView.as_view())
]
