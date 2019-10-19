from django.conf.urls import url

from api.views import ConferenceRUDView, ConferenceLCView

app_name = 'api'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ConferenceRUDView.as_view(), name='conference-rud'),
    url(r'^$', ConferenceLCView.as_view(), name='conference-lc')
]