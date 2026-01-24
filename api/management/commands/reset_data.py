import datetime
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connection



# Ordered deletion respecting dependencies (from leaves to roots)
# Derived from your dependency description
DEPENDENCY_ORDER = [
    "ResearchReport",
    "PositionPaper",
    "Document",
    "Issue",
    "Event",
    "StudentOfficer",
    "Delegate",
    "MUNDirector",
    "Executive",
    "Advisor",
    "Participant",
    "Conference",
    "School",
]

# User deletion happens separately: only normal users
User = get_user_model()


class Command(BaseCommand):
    help = ("Dumps database and deletes all conference-related data while preserving staff/superusers and users with first_name='API' and last_name='Token'.")

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Actually perform the reset (required).",
        )
        parser.add_argument(
            "--dump-dir",
            default="db_dumps",
            help="Directory to store database dump.",
        )

    def handle(self, *args, **options):
        if not options["force"]:
            raise CommandError("This command will DELETE DATA. Use --force to proceed.")

        if not settings.DEBUG:
            raise CommandError("Refusing to reset database when DEBUG=False.")

        # Dump database first
        dump_path = self._dump_database(options["dump_dir"])
        self.stdout.write(f"Database dumped to: {dump_path}")

        # Delete data in dependency order
        self._delete_data()

        # Reset sequences
        self._reset_sequences()

        self.stdout.write(self.style.SUCCESS("Database successfully reset."))

    def _dump_database(self, dump_dir):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_dir = Path(dump_dir)
        dump_dir.mkdir(parents=True, exist_ok=True)
        dump_file = dump_dir / f"db_dump_{timestamp}.json"

        with dump_file.open("w") as f:
            call_command(
                "dumpdata",
                "--natural-foreign",
                "--natural-primary",
                "--indent",
                "2",
                stdout=f,
            )

        return dump_file

    @transaction.atomic
    def _delete_data(self):
        
        self.stdout.write("Deleting dependent models in order...")
        for model_name in DEPENDENCY_ORDER:
            model = self._get_model_by_name(model_name)
            if model:
                count, _ = model.objects.all().delete()
                self.stdout.write(f"Deleted {count} rows from {model_name}")

        self.stdout.write("Deleting normal users...")
        User.objects.filter(is_staff=False, is_superuser=False).exclude(first_name="API", last_name="Token").delete()

    def _get_model_by_name(self, name):
        for model in apps.get_models():
            if model.__name__ == name:
                return model
        self.stdout.write(f"Warning: model {name} not found.")
        return None

    def _reset_sequences(self):
        """Reset primary key sequences for all non-excluded models"""
        from django.core.management.color import no_style

        self.stdout.write("Resetting primary key sequences...")
        models_to_reset = [
            m for m in apps.get_models() if m.__name__ in DEPENDENCY_ORDER
        ]
        sql_statements = connection.ops.sequence_reset_sql(no_style(), models_to_reset)
        with connection.cursor() as cursor:
            for sql in sql_statements:
                cursor.execute(sql)
