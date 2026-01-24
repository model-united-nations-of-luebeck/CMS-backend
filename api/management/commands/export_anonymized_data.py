import json
from datetime import date, datetime
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict

from api.models import (
    Conference,
    School,
    MemberOrganization,
    Location,
    Room,
    Forum,
    Issue,
    Event,
    Plenary,
    Delegate,
    StudentOfficer,
    Staff,
    Advisor,
    Executive,
    MUNDirector,
)

"""
These fields will be removed from all person/participant records to anonymize them.
"""
PERSON_FIELDS_TO_REMOVE = {
    "first_name",
    "last_name",
    "email",
    "mobile",
    "pronouns",
}

PARTICIPANT_FIELDS_TO_REMOVE = {
    "extras",
    "picture",
    "data_consent_time",
    "data_consent_ip",
    "media_consent_time",
    "media_consent_ip",
}


class Command(BaseCommand):
    help = "Export data as anonymized JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default=f"anonymized_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            help="Output JSON file path",
        )

    def handle(self, *args, **options):
        data = {
            "conference": self.export_queryset(Conference),
            "participants": self.export_participants(),
            "schools": self.export_queryset(School),
            "forums": self.export_queryset(Forum),
            "issues": self.export_queryset(Issue),
            "plenaries": self.export_queryset(Plenary),
            "events": self.export_queryset(Event),
            "member_organizations": self.export_queryset(MemberOrganization),
            "locations": self.export_queryset(Location),
            "rooms": self.export_queryset(Room),
        }

        
        with open(options["output"], "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        self.stdout.write(
            self.style.SUCCESS(f"Anonymized export written to {options['output']}")
        )

    def export_queryset(self, model):
        return [
            model_to_dict(obj)
            for obj in model.objects.all().order_by("pk")
        ]

    def export_participants(self):
        return {
            "delegates": self.export_people(Delegate),
            "student_officers": self.export_people(StudentOfficer),
            "staffs": self.export_people(Staff),
            "advisors": self.export_people(Advisor),
            "executives": self.export_people(Executive),
            "mun_directors": self.export_people(MUNDirector),
        }

    def export_people(self, model):
        output = []

        for obj in model.objects.all().order_by("pk"):
            record = model_to_dict(obj)

            # Remove person-identifying fields
            for field in PERSON_FIELDS_TO_REMOVE:
                record.pop(field, None)

            # Remove participant-sensitive fields
            for field in PARTICIPANT_FIELDS_TO_REMOVE:
                record.pop(field, None)

            # Normalize birthday
            if "birthday" in record and record["birthday"]:
                bday = record["birthday"]
                record["birthday"] = date(bday.year, bday.month, 15).isoformat()

            # Remove user and participant_ptr fields
            record.pop("user", None)
            record.pop("participant_ptr", None)

            output.append(record)

        return output
