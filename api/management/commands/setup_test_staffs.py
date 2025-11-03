from django.core.management.base import BaseCommand
from test_data.generate_test_data import generate_staffs

class Command(BaseCommand):
    help = 'Add test staffs to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of staffs to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_staffs(n)
        else:
            generate_staffs()
        self.stdout.write("Staff created successfully")
