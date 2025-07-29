from django.core.management.base import BaseCommand
from test_data.generate_test_data import generate_student_officers

class Command(BaseCommand):
    help = 'Add test student officers to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of student officers to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_student_officers(n)
        else:
            generate_student_officers()
        self.stdout.write("Student Officer(s) created successfully")