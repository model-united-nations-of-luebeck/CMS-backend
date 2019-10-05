from django.contrib import admin
from .models import Conference, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, MemberOrganization, School

# Register your models here for the admin site.

admin.site.register(Conference)
admin.site.register(Participant)
admin.site.register(Delegate)
admin.site.register(StudentOfficer)
admin.site.register(MUNDirector)
admin.site.register(Executive)
admin.site.register(Staff)
admin.site.register(MemberOrganization)
admin.site.register(School)



