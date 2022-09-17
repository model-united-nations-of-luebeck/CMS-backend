'''
This file provides methods to fill the Conference Management System with realistic data that might be in use during a conference. In particular is models randomly generated participants information with different localizations.
'''

from api.models import Conference, Delegate, Executive, Forum, MUNDirector, MemberOrganization, Participant, School, Advisor, Person, Staff, StudentOfficer
import random

from phonenumber_field.validators import validate_international_phonenumber
from django.core.exceptions import ValidationError
LOCALES = ['DE', 'IT', 'TR', 'en_US'] # only phone numbers for these regions are generated

# initialization # 
from faker import Faker
fake = Faker(['de_DE'])
Faker.seed(25) # seed generator so that the same random data can be regenerated

# define methods for generating data # 

def select_randomly_from_choices(choices: list)-> str:
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

def generate_conference():
    '''
    Generates an artificial conference
    '''

    conference = Conference.objects.create(year=2022, startdate='2022-05-30', enddate='2022-06-04', annual_session=25, theme='Responsible Consumption and Production', pre_registration_deadline='2022-12-18T22:55:00Z', chairhuman='Leonard Roemer', vice_chairhuman='Robin Schaub', treasurer='Lasse Rother', vice_treasurer='Nina Mellmann')
    


def generate_schools(n:int=30):
    '''
    Generates artificial entries for schools
    '''
    
    for _ in range(n):
        
        school = School.objects.get_or_create(name=fake.name() + "-School", street=fake.street_name(), city=fake.city(), zipcode=fake.postcode(), country=fake.country(), requested=random.randint(1,30), housing=select_randomly_from_choices(School.HOUSING_OPTIONS), registration_status=select_randomly_from_choices(School.STATUS_CHOICES), fee=random.choice([True, False]), arrival=fake.text(), departure=fake.text(), comment=fake.text())


def generate_advisors(n:int=20):
    '''
    Generates artificial entries for advisors
    '''
    
    for _ in range(n):
        advisor = Advisor.objects.get_or_create(first_name=fake.first_name(), last_name=fake.first_name(), gender=select_randomly_from_choices(Person.GENDER_CHOICES), email=fake.email(), mobile=generate_valid_phone_number(), diet=select_randomly_from_choices(Participant.DIET_CHOICES), birthday=fake.date(), extras=fake.text(), car=random.choice([True, False]), availability=fake.text(), experience=fake.text())
        
def generate_staffs(n:int=40):
    '''
    Generates artificial entries for staff
    '''

    position_names=["IT Staff", "Ad Staff", "Allrounder", "Photo Staff", "Press Member", "Kitchen Staff"]

    for _ in range(n):

        staff = Staff.objects.get_or_create(first_name=fake.first_name(), last_name=fake.first_name(), gender=select_randomly_from_choices(Person.GENDER_CHOICES), email=fake.email(), mobile=generate_valid_phone_number(), diet=select_randomly_from_choices(Participant.DIET_CHOICES), birthday=fake.date(), extras=fake.text(),position_name=random.choice(position_names), school_name=fake.name()+ "-School")
        
def generate_executives(n:int=30):
    '''
    Generates artificial entries for executives
    '''

    position_names = ["Head of Secretariat", "Assistant Head of School Management", "Assistant Student Supervisor", "Student Supervisor", "Head of Kitchen", "Assistant Head of Kiosk", "Head of Press", "Assistant Head of Photo", "Head of IT", "Public Information Officer", "Financial Management", "Conference Management","Secretary-General"]
    department_names = ["Secretariat", "School Management", "Student Supervisors", "Kitchen", "Kiosk", "Press", "Photo", "IT", "Public Information Office", "Financial Management", "Conference Management","General Secretariat"]

    for _ in range(n):

        executive = Executive.objects.get_or_create(first_name=fake.first_name(), last_name=fake.first_name(), gender=select_randomly_from_choices(Person.GENDER_CHOICES), email=fake.email(), mobile=generate_valid_phone_number(), diet=select_randomly_from_choices(Participant.DIET_CHOICES), birthday=fake.date(), extras=fake.text(),position_name=random.choice(position_names), school_name=fake.name()+ "-School", position_level=random.choice([True, False]),department_name=random.choice(department_names))
        
def generate_mun_directors(n:int=50):
    '''
    Generates artificial entries for MUN directors
    '''
    
    for _ in range(n):

        mun_director = MUNDirector.objects.get_or_create(first_name=fake.first_name(), last_name=fake.first_name(), gender=select_randomly_from_choices(Person.GENDER_CHOICES), email=fake.email(), mobile=generate_valid_phone_number(), diet=select_randomly_from_choices(Participant.DIET_CHOICES), birthday=fake.date(), extras=fake.text(), mobile=generate_valid_phone_number(), english_teacher=random.choice([True, False]), school=random.choice(School.objects.all()), housing=select_randomly_from_choices(MUNDirector.HOUSING_OPTIONS))

def generate_student_officers(n:int=30):
    '''
    Generates artificial entries for Student Officers
    '''
    
    position_names = ["Chairman of the Sixth Committee of the General Assembly", "President of the Security Council", "President of the General Assembly", "Vice-Chairwoman of First Committee", "Vice-President of the Human Rights Council", "Vice-Chairwoman of the Special Conference on Science and Technology for Development"]

    for _ in range(n):

        student_officer = StudentOfficer.objects.get_or_create(first_name=fake.first_name(), last_name=fake.first_name(), gender=select_randomly_from_choices(Person.GENDER_CHOICES), email=fake.email(), mobile=generate_valid_phone_number(), diet=select_randomly_from_choices(Participant.DIET_CHOICES), birthday=fake.date(), extras=fake.text(), position_name=random.choice(position_names), position_level=random.choice([True, False]), school_name=fake.name()+"-School", forum=random.choice(Forum.objects.all()))

def generate_delegates(n:int=250):
    '''
    Generates artificial entries for Delegates
    '''
    
    for _ in range(n):

        delegate = Delegate.objects.get_or_create(first_name=fake.first_name(), last_name=fake.first_name(), gender=select_randomly_from_choices(Person.GENDER_CHOICES), email=fake.email(), mobile=generate_valid_phone_number(), diet=select_randomly_from_choices(Participant.DIET_CHOICES), birthday=fake.date(), extras=fake.text(), ambassador=random.choice([True, False]), represents=random.choice(MemberOrganization.objects.all()), school=random.choice(School.objects.all()), forum=random.choice(Forum.objects.all()))