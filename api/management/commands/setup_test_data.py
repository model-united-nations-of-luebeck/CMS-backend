from django.core.management.base import BaseCommand
from test_data.generate_test_data import generate_advisors, generate_delegates, generate_executives, generate_mun_directors, generate_schools, generate_staffs, generate_student_officers, generate_issues

class Command(BaseCommand):
    help = 'Add test data to the database'

    def handle(self, *args, **kwargs):
        # assumes that at least one forum and one member organization exists
        generate_schools()
        generate_advisors()
        generate_staffs()
        generate_executives()
        generate_mun_directors()
        generate_student_officers()
        generate_delegates()
        generate_issues()
        self.stdout.write("Test data created successfully")
