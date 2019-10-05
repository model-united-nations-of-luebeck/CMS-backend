from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Models (sometimes also calles entities or data templates) are stored here. These models describe what kind of objects we deal with in our app. However, the objects themselves are stored in a database.

class Conference(models.Model):
    ''' A conference object represents one session of the MUN conference with the corresponding details'''
    year = models.PositiveSmallIntegerField("year of the conference", help_text="Use format YYYY for years so 2019 instead of just 19")
    startdate = models.DateField("first day", help_text="Use the first day of the conference as start date, at MUNOL it's usually Monday")
    enddate = models.DateField("last day", help_text="Last day of the conference, at MUNOL usually Saturday")
    annual_session = models.PositiveSmallIntegerField("annual session", help_text="First session was in 1998, i.e. MUNOL 2020 will be the 23rd session")
    theme = models.CharField("conference theme", blank=True, max_length=100, help_text="Overarching topic of the conference")
    pre_registration_deadline = models.DateTimeField("pre-registration deadline")
    final_registration_deadline = models.DateTimeField("final registration deadline", blank=True)
    position_paper_deadline = models.DateTimeField("position paper deadline", blank=True)
    chairhuman = models.CharField("Chair:wo:man", max_length=50, help_text="Full name of the Chairman/woman of the MUNOL Association")
    vice_chairhuman = models.CharField("Vice-Chair:wo:man", max_length=50, help_text="Full name of the Vice-Chairman/woman of the MUNOL Association")
    treasurer = models.CharField("Treasurer", max_length=50, help_text="Full name of the Treasurer of the MUNOL Association")
    vice_treasurer = models.CharField("Vice-Treasurer", max_length=50, help_text="Full name of the Vice-Treasurer of the MUNOL Association")


class Person(models.Model):
    ''' Person in general as a human being'''
    first_name = models.CharField("first name", max_length=50, help_text="Including second names if wanted")
    last_name = models.CharField("last name", max_length=50, help_text="Including prefixes like 'von', 'zu', 'de' etc.")
    MALE = 'm'
    FEMALE = 'f'
    OTHER = 'o'
    GENDER_CHOICES = [
        (MALE, 'male'),
        (FEMALE, 'female'),
        (OTHER, 'other')
    ]
    gender = models.CharField("gender", max_length=1, choices=GENDER_CHOICES, default=FEMALE, help_text="the diversity of genders is reflected in the 'other' choice")
    email = models.EmailField("E-Mail", blank=True)
    mobile = PhoneNumberField("mobile phone", blank=True, help_text="remember to include the country code, e.g. for Germany +49 and then leave out the leading 0")

    class Meta:
        abstract = True


class Participant(Person):
    '''Participants are persons who take part in the conference and thus have additional attributes'''
    MEAT = 'meat'
    VEGETARIAN = 'vegetarian'
    VEGAN = 'vegan'
    DIET_CHOICES = [
        (MEAT, 'meat'),
        (VEGETARIAN, 'vegetarian'),
        (VEGAN, 'vegan')
    ]
    diet = models.CharField("diet", max_length=10, choices=DIET_CHOICES, default=VEGETARIAN, help_text="main diet, smaller variations like allergies shall be indicated in the extras field")
    #picture
    birthday = models.DateField("brithday")
    extras = models.TextField("extra information", blank=True, help_text="please include here all additional information about diet, allergies, preferences etc. so that we can try to provide a perfect conference")
