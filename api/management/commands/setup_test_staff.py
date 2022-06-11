from django.core.management.base import BaseCommand
from testdata.generate_testdata import generate_staffs

class Command(BaseCommand):
    help = 'Add test staff to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of staff to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_staffs(n)
        else:
            generate_staffs()
        self.stdout.write("Staff created successfully")