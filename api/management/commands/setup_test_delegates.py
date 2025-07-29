from django.core.management.base import BaseCommand
from test_data.generate_test_data import generate_delegates

class Command(BaseCommand):
    help = 'Add test delegates to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of delegates to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_delegates(n)
        else:
            generate_delegates()
        self.stdout.write("Delegate(s) created successfully")