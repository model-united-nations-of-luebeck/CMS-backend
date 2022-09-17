from django.core.management.base import BaseCommand
from testdata.generate_testdata import generate_executives

class Command(BaseCommand):
    help = 'Add test executive to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of executives to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_executives(n)
        else:
            generate_executives()
        self.stdout.write("Executive(s) created successfully")