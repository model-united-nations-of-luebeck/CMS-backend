from django.core.management.base import BaseCommand
from test_data.generate_test_data import generate_schools

class Command(BaseCommand):
    help = 'Add test schools to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of schools to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_schools(n)
        else:
            generate_schools()
        self.stdout.write("School(s) created successfully")
