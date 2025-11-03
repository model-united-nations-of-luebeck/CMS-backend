'''
This file provides methods to fill the Conference Management System with realistic data that might be in use during a conference. In particular it models randomly generated participants' information with different localizations.
'''

from api.models import Delegate, Executive, Forum, Plenary, MUNDirector, MemberOrganization, School, Advisor, Person, Staff, StudentOfficer, Issue
import random
from typing import List, Tuple
import datetime
from django.contrib.auth.models import User

from phonenumber_field.validators import validate_international_phonenumber
from django.core.exceptions import ValidationError
LOCALES = ['DE', 'IT', 'TR', 'en_US'] # only phone numbers for these regions are generated

# initialization # 
from faker import Faker
fake = Faker(['de_DE'])
Faker.seed(25) # seed generator so that the same random data can be regenerated

TEST_PRONOUNS = ['he/him', 'she/her', 'they/them', 'ze/hir', 'xe/xem', 'ey/em', 'it/its']

# define methods for generating data # 

def select_randomly_from_choices(choices: List[Tuple[str, str]]) -> str:
    '''
    Randomly selects an option from a list of choices. 

    :param: choices (list): is a list of tuples with the first entry being the string representation 
    in the database and the second being the displayed string

    returns a string for the database
    '''
    return random.choice([choice[0] for choice in choices])

def generate_valid_phone_number() -> str:
    '''
    Randomly generates phone numbers that are valid, at least according to the PhoneNumberField Validator.
    '''
    while True:  # generate numbers until a valid one is found
        try:
            locale = random.choice(LOCALES) # switch locales
            fake = Faker(locale)
            number = fake.phone_number()
            validate_international_phonenumber(number)
            return number
        except ValidationError:
            pass # ignore invalid phone numbers


def generate_schools(n:int=30):
    '''
    Generates artificial entries for schools
    '''
    
    for _ in range(n):

        user = User.objects.create_user(
            username=fake.user_name(),
            password=fake.password(),
        )
        
        School.objects.get_or_create(
            user=user,
            name=fake.name() + "-School",
            street=fake.street_name(),
            city=fake.city(),
            zipcode=fake.postcode(),
            country=fake.country(),
            requested=random.randint(1,30),
            housing_delegates=select_randomly_from_choices(School.HOUSING_OPTIONS),
            housing_mun_directors=select_randomly_from_choices(School.HOUSING_OPTIONS),  
            registration_status=select_randomly_from_choices(School.STATUS_CHOICES), 
            fee_paid=random.choice([True, False]), 
            arrival=fake.text(), 
            departure=fake.text(), 
            comment=fake.text()
        )


def generate_advisors(n:int=20):
    '''
    Generates artificial entries for advisors
    '''
    Faker.seed(hash("Advisor"))
    
    for _ in range(n):
        Advisor.objects.get_or_create(
            first_name=fake.first_name(), 
            last_name=fake.last_name(), 
            gender=select_randomly_from_choices(Person.GENDER_CHOICES), 
            email=fake.unique.email(), 
            mobile=generate_valid_phone_number(), 
            birthday=None, 
            pronouns=random.choice(TEST_PRONOUNS),
            extras=fake.text(), 
            data_consent_time=fake.date_time_this_decade(tzinfo=datetime.timezone.utc),
            data_consent_ip=fake.ipv4_private(),
            media_consent_time=random.choice([fake.date_time_this_decade(tzinfo=datetime.timezone.utc), None]),
            media_consent_ip=random.choice([fake.ipv4_private(), None]),
            car=random.choice([True, False]), 
            availability=fake.text(), 
            experience=fake.text(),
            help=", ".join(fake.words(nb=random.randint(1, 4))),
        )

def generate_staffs(n:int=40):
    '''
    Generates artificial entries for staffs
    '''
    Faker.seed(hash("Staff"))

    position_names=["IT Staff", "Ad Staff", "Allrounder", "Photo Staff", "Press Member", "Kitchen Staff"]

    for _ in range(n):

        Staff.objects.get_or_create(
            first_name=fake.first_name(), 
            last_name=fake.last_name(), 
            gender=select_randomly_from_choices(Person.GENDER_CHOICES), 
            email=fake.unique.email(), 
            mobile=generate_valid_phone_number(), 
            birthday=fake.date(), 
            pronouns=random.choice(TEST_PRONOUNS),
            extras=fake.text(), 
            data_consent_time=fake.date_time_this_decade(tzinfo=datetime.timezone.utc),
            data_consent_ip=fake.ipv4_private(),
            media_consent_time=random.choice([fake.date_time_this_decade(tzinfo=datetime.timezone.utc), None]),
            media_consent_ip=random.choice([fake.ipv4_private(), None]),
            position_name=random.choice(position_names), 
            school_name=fake.name()+ "-School")
        
def generate_executives(n:int=30):
    '''
    Generates artificial entries for executives
    '''
    Faker.seed(hash("Executive"))

    position_names = ["Head of Secretariat", "Assistant Head of School Management", "Assistant Student Supervisor", "Student Supervisor", "Head of Kitchen", "Assistant Head of Kiosk", "Head of Press", "Assistant Head of Photo", "Head of IT", "Public Information Officer", "Financial Management", "Conference Management","Secretary-General"]
    department_names = ["Secretariat", "School Management", "Student Supervisors", "Kitchen", "Kiosk", "Press", "Photo", "IT", "Public Information Office", "Financial Management", "Conference Management","General Secretariat"]

    for _ in range(n):

        Executive.objects.get_or_create(
            first_name=fake.first_name(), 
            last_name=fake.last_name(), 
            gender=select_randomly_from_choices(Person.GENDER_CHOICES), 
            email=fake.unique.email(), 
            mobile=generate_valid_phone_number(), 
            birthday=fake.date(), 
            pronouns=random.choice(TEST_PRONOUNS),
            extras=fake.text(), 
            data_consent_time=fake.date_time_this_decade( tzinfo=datetime.timezone.utc),
            data_consent_ip=fake.ipv4_private(),
            media_consent_time=random.choice([fake.date_time_this_decade(tzinfo=datetime.timezone.utc), None]),
            media_consent_ip=random.choice([fake.ipv4_private(), None]),
            position_name=random.choice(position_names), school_name=fake.name()+ "-School")
        
def generate_mun_directors(n:int=50):
    '''
    Generates artificial entries for MUN directors
    '''
    Faker.seed(hash("MUNDirector"))

    for _ in range(n):

        MUNDirector.objects.get_or_create(
            first_name=fake.first_name(), 
            last_name=fake.last_name(), 
            gender=select_randomly_from_choices(Person.GENDER_CHOICES), 
            email=fake.unique.email(), 
            mobile=generate_valid_phone_number(), 
            birthday=fake.date(), 
            pronouns=random.choice(TEST_PRONOUNS),
            extras=fake.text(), 
            data_consent_time=fake.date_time_this_decade(tzinfo=datetime.timezone.utc),
            data_consent_ip=fake.ipv4_private(),
            media_consent_time=random.choice([fake.date_time_this_decade(tzinfo=datetime.timezone.utc), None]),
            media_consent_ip=random.choice([fake.ipv4_private(), None]),
            english_teacher=random.choice([True, False]), school=random.choice(School.objects.all()))

def generate_student_officers(n:int=30):
    '''
    Generates artificial entries for Student Officers
    '''
    Faker.seed(hash("StudentOfficer"))

    position_names = ["Chairman of the Sixth Committee of the General Assembly", "President of the Security Council", "President of the General Assembly", "Vice-Chairwoman of First Committee", "Vice-President of the Human Rights Council", "Vice-Chairwoman of the Special Conference on Science and Technology for Development"]

    for _ in range(n):

        StudentOfficer.objects.get_or_create(
            first_name=fake.first_name(), 
            last_name=fake.last_name(), 
            gender=select_randomly_from_choices(Person.GENDER_CHOICES), 
            email=fake.unique.email(), 
            mobile=generate_valid_phone_number(), 
            birthday=fake.date(), 
            pronouns=random.choice(TEST_PRONOUNS),
            extras=fake.text(), 
            data_consent_time=fake.date_time_this_decade(tzinfo=datetime.timezone.utc),
            data_consent_ip=fake.ipv4_private(),
            media_consent_time=random.choice([fake.date_time_this_decade(tzinfo=datetime.timezone.utc), None]),
            media_consent_ip=random.choice([fake.ipv4_private(), None]),
            position_name=random.choice(position_names), school_name=fake.name()+"-School", forum=random.choice(Forum.objects.all()),
            plenary=random.choice(Plenary.objects.all()))

def generate_valid_forum_member_organization_combo() -> Tuple[Forum, MemberOrganization]:
    '''
    Generates a valid combination of Forum and MemberOrganization such that the MemberOrganization is not already represented in the Forum by a Delegate.
    '''
    while True:
        forum = random.choice(Forum.objects.all())
        member_organization = random.choice(MemberOrganization.objects.all())
        if not Delegate.objects.filter(forum=forum, represents=member_organization).exists():
            return forum, member_organization

def generate_delegates(n:int=250):
    '''
    Generates artificial entries for Delegates.  
    '''
    Faker.seed(hash("Delegate"))

    for _ in range(n):

        # Ensure that one member organization is only represented by one delegate per forum.
        forum, member_organization = generate_valid_forum_member_organization_combo()

        # Furthermore ensure that each member organization has exactly one ambassador by setting the first one as the ambassador.
        ambassador = not Delegate.objects.filter(represents=member_organization).exists()

        Delegate.objects.get_or_create(
            first_name=fake.first_name(), 
            last_name=fake.last_name(), 
            gender=select_randomly_from_choices(Person.GENDER_CHOICES), 
            email=fake.unique.email(), 
            mobile=generate_valid_phone_number(), 
            birthday=fake.date(), 
            pronouns=random.choice(TEST_PRONOUNS),
            extras=fake.text(), 
            data_consent_time=fake.date_time_this_decade( tzinfo=datetime.timezone.utc),
            data_consent_ip=fake.ipv4_private(),
            media_consent_time=random.choice([fake.date_time_this_decade(tzinfo=datetime.timezone.utc), None]),
            media_consent_ip=random.choice([fake.ipv4_private(), None]),
            school=random.choice(School.objects.all()), 
            represents=member_organization,
            forum=forum,
            ambassador=ambassador)
        
def generate_issues(n:int=50):
    '''
    Generates artificial issues for the test data.
    '''
    
    for _ in range(n):
        Issue.objects.get_or_create(
            name=fake.sentence(nb_words=random.randint(6, 12)),
            forum=random.choice(Forum.objects.all())
        )
