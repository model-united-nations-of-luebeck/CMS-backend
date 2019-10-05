from django.db import models

# Models (sometimes also calles entities or data templates) are stored here. These models describe what kind of objects we deal with in our app. However, the objects themselves are stored in a database.

class Conference(models.Model):
    ''' A conference object represents one session of the MUN conference with the corresponding details'''
    year = models.PositiveSmallIntegerField(help_text="Use format YYYY for years so 2019 instead of just 19")
    startdate = models.DateField(help_text="Use the first day of the conference as start date, at MUNOL it's usually Monday")
    enddate = models.DateField(help_text="Last day of the conference, at MUNOL usually Saturday")
    annual_session = models.PositiveSmallIntegerField(help_text="First session was in 1998, i.e. MUNOL 2020 will be the 23rd session")
    theme = models.CharField(blank=True, max_length="100", help_text="Overarching topic of the conference")
    pre_registration_deadline = models.DateTimeField()
    final_registration_deadline = models.DateTimeField(blank=True)
    position_paper_deadline = models.DateTimeField(blank=True)
    chairhuman = models.CharField(max_length="50", help_text="Full name of the Chairman/woman of the MUNOL Association")
    vice_chairhuman = models.CharField(max_length="50", help_text="Full name of the Vice-Chairman/woman of the MUNOL Association")
    treasurer = models.CharField(max_length="50", help_text="Full name of the Treasurer of the MUNOL Association")
    vice_treasurer = models.CharField(max_length="50", help_text="Full name of the Vice-Treasurer of the MUNOL Association")
