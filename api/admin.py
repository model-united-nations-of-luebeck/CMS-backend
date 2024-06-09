from django.contrib import admin
from .models import Conference, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, Advisor, MemberOrganization, School, Forum, Plenary, Location, Room, Event, Lunch, Issue, Document, ResearchReport, PositionPaper
from django.utils.safestring import mark_safe

class ParticipantAdmin(admin.ModelAdmin):
    readonly_fields = ('rendered_badge_photo',)
    
    # Display the rendered badge photo in the admin site
    def rendered_badge_photo(self, obj):
        if obj.picture:
            if obj.picture.startswith('data:image/') and ';base64,' in obj.picture:
                return mark_safe(f'<img src="{obj.picture}" alt="Badge Photo" width="350" height="450" />')
            else:
                return 'Photo data is not base 64 encoded'
        else:
            return 'No Photo Available'
    
    rendered_badge_photo.short_description = 'Rendered Badge Photo'


# Register your models here for the admin site.

admin.site.register(Conference)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Delegate, ParticipantAdmin)
admin.site.register(StudentOfficer, ParticipantAdmin)
admin.site.register(MUNDirector, ParticipantAdmin)
admin.site.register(Executive, ParticipantAdmin)
admin.site.register(Staff, ParticipantAdmin)
admin.site.register(Advisor, ParticipantAdmin)
admin.site.register(MemberOrganization)
admin.site.register(School)
admin.site.register(Forum)
admin.site.register(Plenary)
admin.site.register(Location)
admin.site.register(Room)
admin.site.register(Event)
admin.site.register(Lunch)
admin.site.register(Issue)
admin.site.register(Document)
admin.site.register(ResearchReport)
admin.site.register(PositionPaper)