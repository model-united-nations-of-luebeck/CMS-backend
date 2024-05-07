from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField

# Models (sometimes also called entities or data templates) are stored here. These models describe what kind of objects we deal with in our app. However, the objects themselves are stored in a database.


class Conference(models.Model):
    ''' A conference object represents one session of the MUN conference with the corresponding details'''
    year = models.PositiveSmallIntegerField(
        "year of the conference", help_text="Use format YYYY for years so 2019 instead of just 19")
    startdate = models.DateField(
        "first day", help_text="Use the first day of the conference as start date, at MUNOL it's usually Monday")
    enddate = models.DateField(
        "last day", help_text="Last day of the conference, at MUNOL usually Saturday")
    annual_session = models.PositiveSmallIntegerField(
        "annual session", help_text="First session was in 1998, i.e. MUNOL 2020 will be the 23rd session")
    theme = models.CharField("conference theme", blank=True, null=True,
                             max_length=100, help_text="Overarching topic of the conference")
    pre_registration_deadline = models.DateTimeField(
        "pre-registration deadline")
    final_registration_deadline = models.DateTimeField(
        "final registration deadline", blank=True, null=True)
    position_paper_deadline = models.DateTimeField(
        "position paper deadline", blank=True, null=True)
    chairhuman = models.CharField("Chair:wo:man", max_length=50,
                                  help_text="Full name of the Chairman/woman of the MUNOL Association")
    vice_chairhuman = models.CharField("Vice-Chair:wo:man", max_length=50,
                                       help_text="Full name of the Vice-Chairman/woman of the MUNOL Association")
    treasurer = models.CharField(
        "Treasurer", max_length=50, help_text="Full name of the Treasurer of the MUNOL Association")
    vice_treasurer = models.CharField(
        "Vice-Treasurer", max_length=50, help_text="Full name of the Vice-Treasurer of the MUNOL Association")

    def __str__(self):
        return "MUNOL {}".format(self.year)


class School(models.Model):
    ''' School that is planning to attend the conference '''
    name = models.CharField("School Name", max_length=50,
                            help_text="Name will be used like this for badges and certificates.")
    street = models.CharField(
        "Street Name", max_length=50, blank=True, null=True)
    city = models.CharField("City", max_length=50, blank=True, null=True)
    zipcode = models.CharField(
        "ZIP Code", max_length=10, blank=True, null=True)
    country = models.CharField(
        "Country of origin", max_length=50, blank=True, null=True)
    requested = models.PositiveSmallIntegerField(
        "Number of requested students", help_text="Note, that this is the <b>requested</b> number, <u>not</u> the confirmed one which might be lower.", blank=True, null=True)
    HOSTEL = 'hostel'
    GUEST_FAMILY = 'guest family'
    OTHER = 'other'
    HOUSING_OPTIONS = [
        (HOSTEL, 'hostel'),
        (GUEST_FAMILY, 'guest family'),
        (OTHER, 'other self-organized accommodation')
    ]
    housing_delegates = models.CharField("Housing option for delegates", max_length=50, choices=HOUSING_OPTIONS, default=OTHER,
                                         help_text="Please note, that housing in guest families is not available for all delegations and we will prefer international delegations in our housing who travel the longest distances.")
    housing_mun_directors = models.CharField("Housing option for MUN-Directors", max_length=50, choices=HOUSING_OPTIONS, default=OTHER,
                                             help_text="Please note, that housing in guest families is not available for all delegations and we will prefer international delegations in our housing who travels the longest distances.")
    WAITING_FOR_PRE_REGISTRATION = 'WAITING_FOR_PRE_REGISTRATION'
    PRE_REGISTRATION_DONE = 'PRE_REGISTRATION_DONE'
    WAITING_FOR_DATA_PROTECTION = 'WAITING_FOR_DATA_PROTECTION'
    WAITING_FOR_FINAL_REGISTRATION = 'WAITING_FOR_FINAL_REGISTRATION'
    FINAL_REGISTRATION_DONE = 'FINAL_REGISTRATION_DONE'
    CANCELED = 'CANCELED'
    STATUS_CHOICES = [
        (WAITING_FOR_PRE_REGISTRATION, 'waiting for pre-registration'),
        (PRE_REGISTRATION_DONE, 'pre-registration done'),
        (WAITING_FOR_DATA_PROTECTION, 'waiting for data protection'),
        (WAITING_FOR_FINAL_REGISTRATION, 'waiting for final registration'),
        (FINAL_REGISTRATION_DONE, 'final registration done'),
        (CANCELED, 'canceled')
    ]
    registration_status = models.CharField("Registration status", max_length=50, choices=STATUS_CHOICES,
                                           default=WAITING_FOR_PRE_REGISTRATION, help_text="This status indicates at what stage of registration the school is.")
    fee = models.BooleanField("Pre-registration fee", default=False,
                              help_text="Was the pre-registration fee paid?")
    arrival = models.TextField("Arrival Information", blank=True, null=True,
                               help_text="Please provide date, time and location (e.g. school, conference venue, train station, airport, ...) of arrival here so that we can plan the registration process and housing respectively.")
    departure = models.TextField("Departure Information", blank=True, null=True,
                                 help_text="Please provide date, time and location (e.g. conference venue, train station, airport, ...) of departure here so that we can plan in advance.")
    comment = models.TextField("Internal Comment", blank=True, null=True,
                               help_text="Write down notes and comments regarding this school here, e.g. outstanding fees, contact persons names, etc.")

    def __str__(self):
        return "{}, {}".format(self.name, self.country)


class MemberOrganization(models.Model):
    ''' A represented state, former state, observer state, NGO, IGO, UN sub-body or other member of the UN '''
    name = models.CharField("Member state's or Organization's name", max_length=50,
                            help_text="Use common (short) version of the name, e.g. 'Russia' instead of 'Russian Federation' or 'EU' instead of 'European Union', so use abbreviations. This name is only used internally and thus allows to create Countries twice, e.g. China 1 and China 2 if the delegation is split between two schools.")
    official_name = models.CharField(
        "Official Name", max_length=150, help_text="Official name as stated on resolutions of the UN, e.g. 'Russian Federation' instead of Russia. No abbreviations allowed here.")
    placard_name = models.CharField(
        "Placards Name", max_length=50, help_text="The best readable compromise between no abbreviation but also not the full official name")
    MEMBER_STATE = 'member state'
    OBSERVER_STATE = 'observer state'
    FORMER_MEMBER = 'former member state'
    NON_GOVERNMENTAL_ORGANIZATION = 'non-governmental organization'
    INTER_GOVERNMENTAL_ORGANIZATION = 'inter-governmental organization'
    UN_SUB_BODY = 'UN sub-body'
    STATUS_CHOICES = [
        (MEMBER_STATE, 'member state'),
        (OBSERVER_STATE, 'observer state'),
        (FORMER_MEMBER, 'former member state'),
        (NON_GOVERNMENTAL_ORGANIZATION, 'non-governmental organization'),
        (INTER_GOVERNMENTAL_ORGANIZATION, 'inter-governmental organization'),
        (UN_SUB_BODY, 'UN sub-body'),
    ]
    status = models.CharField(
        "Status in the UN", max_length=50, choices=STATUS_CHOICES, default=MEMBER_STATE)
    active = models.BooleanField("Represented at this conference?", default=False,
                                 help_text="This allows to store all countries but only select the ones to be simulated and quickly change the selection.")
    flag = models.URLField("Flag URL", max_length=250, blank=True, null=True,
                           help_text="URL to SVG Flag file of the Member Organization if it has one")

    class Meta:
        verbose_name = "Member Organization"

    def __str__(self):
        return self.name


class Location(models.Model):
    ''' a conference venue which can be show on a map '''
    name = models.CharField("Location name", max_length=100,
                            help_text="e.g. 'Thomas-Mann-Schule'")
    latitude = models.DecimalField(
        "Latitude", decimal_places=6, max_digits=9, help_text="e.g. 53.860421")
    longitude = models.DecimalField(
        "Longitude", decimal_places=6, max_digits=9, help_text="e.g. 10.713462")
    zoom_level = models.PositiveSmallIntegerField(
        "Zoom level", help_text="a number between 1 and 20, like google maps zoom levels")
    address = models.CharField(
        "Address", max_length=100, help_text="e.g. 'Thomas-Mann-Straße 14', i.e. Street Name and House Number")

    def __str__(self):
        return self.name


class Room(Location):
    ''' Rooms within the School are also locations '''
    room_number = models.CharField(
        "Room Number", max_length=10, help_text="e.g. '0.23'")
    floor = models.PositiveSmallIntegerField(
        "Floor", help_text="Ground Floor is level 0, First Floor is 1, etc.")

    def __str__(self):
        return self.room_number


class Person(models.Model):
    ''' Person in general as a human being'''
    first_name = models.CharField(
        "first name", max_length=50, help_text="Including second names if wanted")
    last_name = models.CharField(
        "last name", max_length=50, help_text="Including prefixes like 'von', 'zu', 'de' etc.")
    MALE = 'm'
    FEMALE = 'f'
    OTHER = 'o'
    GENDER_CHOICES = [
        (MALE, 'male'),
        (FEMALE, 'female'),
        (OTHER, 'other')
    ]
    gender = models.CharField("gender", max_length=1, choices=GENDER_CHOICES, default=FEMALE,
                              help_text="the diversity of genders is reflected in the 'other' choice")
    email = models.EmailField("E-Mail", blank=True, null=True)
    mobile = PhoneNumberField("mobile phone", blank=True,  null=True,
                              help_text="remember to include the country code, e.g. for Germany +49 and then leave out the leading 0")

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


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
    diet = models.CharField("diet", max_length=10, choices=DIET_CHOICES, default=VEGETARIAN,
                            help_text="main diet, smaller variations like allergies shall be indicated in the extras field")
    ROLE_CHOICES = [("advisor", 'Conference Advisor'), ('student officer', 'Student Officer'), ('delegate', 'Delegate'),
                    ("mun_director", "MUN Director"), ('executive', 'Executive'), ("staff", 'Staff')]
    role = models.CharField("the role they are participating in the conference as",
                            choices=ROLE_CHOICES, max_length=15, blank=True, editable=False)
    picture = models.ImageField("badge photo", blank=True, null=True, upload_to="images/badge_photos",
                                help_text="please provide a passport-style photo for the badge")
    birthday = models.DateField("birthday", blank=True, null=True)
    extras = models.TextField("extra information", blank=True, null=True,
                              help_text="please include here all additional information about diet, allergies, preferences etc. so that we can try to provide a perfect conference")


class Event(models.Model):
    ''' An event during the conference '''
    name = models.CharField("Event name", max_length=100,
                            help_text="How is the event called")
    day = models.DateField("Day", help_text="On which day does it take place?")
    start_time = models.TimeField(
        "Start Time", help_text="Specify the beginning time")
    end_time = models.TimeField("End Time", blank=True, null=True,
                                help_text="Specify the end time, none if it's open ended")
    info = models.CharField("Additional information", blank=True, null=True, max_length=200,
                            help_text="Add additional information, e.g. dress code, speakers title")
    location = models.ForeignKey(Location, blank=True, null=True,
                                 help_text="Select where the event happens", on_delete=models.SET_NULL)
    relevance = MultiSelectField(
        choices=Participant.ROLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return "{}, {}, {}".format(self.name, self.day, self.start_time)


class Lunch(Event):
    ''' important event of the day '''


class Plenary(models.Model):
    ''' A plenary session of several forums '''
    name = models.CharField("Plenary Name", max_length=50,
                            help_text="e.g. 'General Assembly' or 'Economic and Social Council'")
    abbreviation = models.CharField("Abbreviated Plenary Name", max_length=10, blank=True, null=True, help_text="e.g. 'GA', 'ECOSOC'")
    location = models.ForeignKey(Location, blank=True, null=True,
                                 help_text="Select a conference venue where this plenary takes place", on_delete=models.SET_NULL)
    # might have to be limited to 3 or 5 lunch events per plenary
    lunches = models.ManyToManyField(Lunch, blank=True)

    def __str__(self):
        return self.name


class Forum(models.Model):
    ''' A body of the UN, usually committees, councils, commissions, special conferences etc. '''
    name = models.CharField("Forum Name", max_length=50,
                            help_text="e.g. 'First Committee', 'Economic and Social Council")
    abbreviation = models.CharField(
        "Abbreviated Forum Name", max_length=10, blank=True, null=True, help_text="e.g. 'GA1', 'ECOSOC'")
    subtitle = models.CharField("Explanatory Subtitle", max_length=75, blank=True,
                                null=True, help_text="e.g. 'Disarmament and International Security")
    email = models.EmailField(
        "E-Mail", blank=True, null=True, help_text="Email will be displayed on website")
    room = models.ForeignKey(Room, blank=True, null=True,
                             help_text="Select a Room within the conference venue", on_delete=models.SET_NULL)
    plenary = models.ForeignKey(Plenary, blank=True, null=True,
                                help_text="Select a Plenary if this forum is part of it, otherwise choose none.", on_delete=models.SET_NULL)
    # might have to be limited to 3 or 5 lunch events per forum
    lunches = models.ManyToManyField(Lunch, blank=True)

    def __str__(self):
        return self.name


class Delegate(Participant):
    ''' Delegates are the main participants of MUN :model:`api.Conference` and represent a delegation's position in their :model:`api.Forum`. '''
    ambassador = models.BooleanField("Is the delegate the delegation's ambassador?", default=False,
                                     help_text="one delegate per delegation has to be selected to be the ambassador of the delegation")  # Question: how do we ensure that there is one, but only one ambassador per delegation? Do we do it on database level or in front end software? Answer: Do it in front end and not in DB. If no ambassador is chosen, we simply select the first one of each delegation.
    first_timer = models.BooleanField("It the delegate participating in their first MUN conference?", default=True,
                                      help_text="There is a first MUN conference for everyone. Knowing this in advance, the team can prepare a smooth first conference for first timers.")
    represents = models.ForeignKey(
        MemberOrganization, help_text="select member organization which is represented by this delegate", on_delete=models.PROTECT)
    school = models.ForeignKey(
        School, help_text="select the school which is attended by this delegate", on_delete=models.PROTECT)
    forum = models.ForeignKey(
        Forum, help_text="Select which forum this Delegate is a member of", on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.role = 'delegate'
        return super().save(*args, **kwargs)


class StudentOfficer(Participant):
    ''' Student Officers are the participants that chair a forum '''
    position_name = models.CharField(
        "Position name", max_length=20, help_text="e.g. Chairman, Chairwoman, President, ... but <b>NOT</b> the entire title like 'Vice-Chairman of the First Committee' this will be generated automatically")
    position_level = models.BooleanField("Is this the main Student Officer of the forum?", default=False,
                                         help_text="Main Student Officers might have other duties and obligations than vice/deputy Student Officers")
    # Explanation: Chairs don't belong to schools' delegations but the name shall still be available. Also chairs can participate without their school participating.
    school_name = models.CharField(
        "School name", max_length=50, help_text="Name of the school/institution the student officer attends.")
    forum = models.ForeignKey(Forum, blank=True, null=True,
                              help_text="Select which forum this Student Officer is chairing", on_delete=models.SET_NULL)
    plenary = models.ForeignKey(Plenary, blank=True, null=True,
                                help_text="Select if this Student Officer is also chairing a Plenary.", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Student Officer"

    def save(self, *args, **kwargs):
        self.role = 'student officer'
        return super().save(*args, **kwargs)


class MUNDirector(Participant):
    ''' MUN-Directors are responsible for supervising their schools' delegates'''
    landline_phone = PhoneNumberField("landline phone", blank=True, null=True,
                                      help_text="in case that a call is quicker than an email, don't forget the country code")
    english_teacher = models.BooleanField("Is the MUN-Director an English teacher?", default=True,
                                          help_text="English teachers can help with correcting the language and grammar of resolutions.")
    school = models.ForeignKey(
        School, help_text="select the school at which this MUN Director teaches", on_delete=models.PROTECT)
    HOSTEL = 'hostel'
    GUEST_FAMILY = 'guest family'
    OTHER = 'other'
    help_text = "Please note, that housing in guest families is not available for all MUN-Directors."
    # Figure out how to set BIRTHDAY to >18 because this can be assumed.
    # Solved: We don't need to store a Birthday, it can also be blank and then we don't show it for MUN Directors, only for other participants and enforce setting a birthday there.

    class Meta:
        verbose_name = "MUN-Director"

    def save(self, *args, **kwargs):
        self.role = 'mun_director'
        return super().save(*args, **kwargs)


class Executive(Participant):
    ''' Executives are part of the organising team '''
    position_name = models.CharField(
        "Position name", max_length=50, help_text="e.g. 'Assistant Head of School Management'")
    position_level = models.BooleanField("Is this the Head of this position?", default=False,
                                         help_text="Main Head might have other duties and obligations than Assistant Heads")
    department_name = models.CharField(
        "Department name", max_length=50, help_text="e.g. 'School Management', note that this name is <b>not</b> the entire position title")
    school_name = models.CharField("School name", max_length=50, default="Thomas-Mann-Schule",
                                   help_text="Name of the school/institution the Executive attends.")

    def save(self, *args, **kwargs):
        self.role = 'executive'
        return super().save(*args, **kwargs)


class Staff(Participant):
    ''' Staffs help in some departments and forums to keep the conference running smoothly '''
    position_name = models.CharField(
        "Position name", max_length=50, help_text="e.g. 'Administration Staff' or 'IT Staff'")
    school_name = models.CharField("School name", max_length=50, default="Thomas-Mann-Schule",
                                   help_text="Name of the school/institution the Staff member attends.")

    def save(self, *args, **kwargs):
        self.role = 'staff'
        return super().save(*args, **kwargs)


class Advisor(Participant):
    ''' Advisors are former participants who now support the conference with their knowledge '''
    car = models.BooleanField("Car available", blank=True, default=False,
                              help_text="Do you have a car available during MUNOL and have a driving license so that you could help driving people and stuff around?")
    availability = models.CharField("Availability during week", blank=True, null=True, max_length=512,
                                    help_text="Please specify on which days and nighs you will attend the conference and give your advice")
    experience = models.CharField("MUN Experience", blank=True, null=True, max_length=512,
                                  help_text="Please specify which role you had in former MUNOL sessions and other conferences, e.g. 'School Management 2013'")
    help = models.CharField("Areas of help", max_length=512,
                            help_text="In which areas would you like to support the team?")

    def save(self, *args, **kwargs):
        self.role = 'advisor'
        return super().save(*args, **kwargs)


class Issue(models.Model):
    ''' An Issue on the Agenda of the conference '''
    name = models.CharField("Issue name", max_length=256,
                            help_text="Official Issue title as on the Agenda")
    forum = models.ForeignKey(
        Forum, help_text="Select the forum in which this issue is debated", on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Document(models.Model):
    ''' A PDF Document for the conference '''
    name = models.CharField("Name of the document",
                            max_length=100, help_text="Document's name")
    file = models.FileField("File", upload_to="documents",
                            help_text="Document file on server")
    # auto_now_add sets the current datetime when the object is first created
    created = models.DateTimeField(
        "Created at", auto_now_add=True, help_text="When was this document created")
    author = models.CharField("Author(s)", blank=True, null=True,
                              max_length=100, help_text="Who created this document?")

    def __str__(self):
        return self.name


class ResearchReport(Document):
    ''' A background research report for one issue '''
    issue = models.ForeignKey(
        Issue, help_text="Select the issue this research report belongs to", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Research Report"


class PositionPaper(Document):
    ''' A document stating the delegations position on issues debated in a forum '''
    delegate = models.ForeignKey(
        Delegate, help_text="Who has written this position paper?", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Position Paper"
