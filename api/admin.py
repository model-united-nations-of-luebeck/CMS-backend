from django.contrib import admin
from .models import Conference, Participant, Delegate, StudentOfficer, MUNDirector, Executive, Staff, Advisor, MemberOrganization, School, Forum, Plenary, Location, Room, Event, Lunch, Issue, Document, ResearchReport, PositionPaper
from django.utils.safestring import mark_safe

@admin.register(Advisor, Delegate, Executive, MUNDirector, Participant, Staff, StudentOfficer)
class ParticipantAdmin(admin.ModelAdmin):
    readonly_fields = ('rendered_badge_photo',)
    
    # Display the rendered badge photo in the admin site
    @admin.display(
        description='Rendered Badge Photo'
    )
    def rendered_badge_photo(self, obj):
        if obj.picture:
            if obj.picture and hasattr(obj.picture, 'url'):
                return mark_safe(f'<img src="{obj.picture.url}" alt="Badge Photo" width="350" height="450" />')
            else:
                return 'Photo Invalid'
        else:
            return 'No Photo Available'
    


# Register your models here for the admin site.

admin.site.register(Conference)
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
