from django.core.management.base import BaseCommand
from testdata.generate_testdata import generate_student_officers

class Command(BaseCommand):
    help = 'Add test student officer to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of student officers to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_student_officers(n)
        else:
            generate_student_officers()