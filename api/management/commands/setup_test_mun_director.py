from django.core.management.base import BaseCommand
from testdata.generate_testdata import generate_mun_directors

class Command(BaseCommand):
    help = 'Add test MUN director to the database'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--number', type=int, help='Define the number of MUN directors to be created', )


    def handle(self, *args, **kwargs):
        n = kwargs.get('number')
        if n:
            generate_mun_directors(n)
        else:
            generate_mun_directors()