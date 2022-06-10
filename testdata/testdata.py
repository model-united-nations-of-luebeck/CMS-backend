'''
This script creates test data to fill the Conference Management System with realistic data that might be in use during a conference. In particular is models all conference information with hard-coded values and randomly generated participants information with different localizations.
'''

# initialization # 
from faker import Faker
fake = Faker(['de_DE','tr_TR'])
Faker.seed(25) # seed generator so that the same random data can be regenerated

print(fake.name())
print(fake.address())

# define methods for generating data # 

def generate_forums():
    '''
    Will populate the forums based on a file
    '''

def generate_member_organizations():
    '''
    Will populate the member organizations based on a file
    '''

def generate_schools(n=10):
    '''
    Generates artificial entries for schools
    '''

def generate_delegates(n=200):
    '''
    Generates artificial entries for delegates
    '''

# run generation for test data #

generate_forums()
generate_member_organizations()