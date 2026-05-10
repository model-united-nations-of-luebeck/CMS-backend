from django.core.management.base import BaseCommand
from test_data.generate_test_data import generate_issues

class Command(BaseCommand):
    help = 'Add test issues to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of issues to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_issues(n)
        else:
            generate_issues()
        self.stdout.write("Issues created successfully")
