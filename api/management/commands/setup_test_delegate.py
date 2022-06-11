from django.core.management.base import BaseCommand
from testdata.generate_testdata import generate_delegates

class Command(BaseCommand):
    help = 'Add test delegate to the database'

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