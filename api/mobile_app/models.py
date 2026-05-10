from django.db import models

from api.models import Participant


class ParticipantLoginData(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)
    app_code = models.CharField("app login code", blank=True, editable=False, max_length=8, help_text="auto-generated one time login code")
    app_code_expires_by = models.DateTimeField("app code expires by", blank=True, editable=False, null=True, help_text="expiration date for the app code")
