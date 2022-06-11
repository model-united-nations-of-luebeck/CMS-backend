from django.core.management.base import BaseCommand
from testdata.generate_testdata import generate_advisors

class Command(BaseCommand):
    help = 'Add test advisor to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of advisors to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_advisors(n)
        else:
            generate_advisors()
        self.stdout.write("Advisor(s) created successfully")