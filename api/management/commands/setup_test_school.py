from django.core.management.base import BaseCommand
from testdata.generate_testdata import generate_schools

class Command(BaseCommand):
    help = 'Add test school to the database'

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