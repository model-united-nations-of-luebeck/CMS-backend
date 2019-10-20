"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('api.urls', namespace='api'))
    
]

'''url(r'^api/schools/', include('api.urls', namespace='api-schools')),
    url(r'^api/member-organizations/', include('api.urls', namespace='api-member-organizations')),
    url(r'^api/locations/', include('api.urls', namespace='api-locations')),
    url(r'^api/rooms/', include('api.urls', namespace='api-rooms')),
    url(r'^api/events/', include('api.urls', namespace='api-events')),
    url(r'^api/lunches/', include('api.urls', namespace='api-lunches')),
    url(r'^api/plenaries/', include('api.urls', namespace='api-plenaries')),
    url(r'^api/forums/', include('api.urls', namespace='api-forums')),
    url(r'^api/participants/', include('api.urls', namespace='api-participants')),
    url(r'^api/delegates/', include('api.urls', namespace='api-delegates')),
    url(r'^api/student-officers/', include('api.urls', namespace='api-student-officers')),
    url(r'^api/mun-directors/', include('api.urls', namespace='api-mun-directors')),
    url(r'^api/executives/', include('api.urls', namespace='api-executives')),
    url(r'^api/staffs/', include('api.urls', namespace='api-staffs')),
    url(r'^api/advisors/', include('api.urls', namespace='api-advisors')),
    url(r'^api/issues/', include('api.urls', namespace='api-issues')),
    url(r'^api/documents/', include('api.urls', namespace='api-documents')),
    url(r'^api/research-reports/', include('api.urls', namespace='api-research-reports')),
    url(r'^api/position-papers/', include('api.urls', namespace='api-position-papers')),
    '''