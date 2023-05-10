import json
import secrets
from typing import Any

import jwt

from datetime import date, timedelta
from smtplib import SMTPException

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone
from requests import get, HTTPError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mobile_app.serializers import *
from api.models import Participant, Conference

# Make sure to create a secret.py in the same folder as this file and specify:
# - MIGRATE_TOKEN for the old CMS
# - EMAIL_PASSWORD for the smtp auth used in the verification code emails
# - RSA_PASSPHRASE for the digital badge signature
# - RSA_PRIVATE_KEY for the digital badge signature
# Use secret.example.py as a template.
from api.mobile_app.secret import MIGRATE_TOKEN, RSA_PASSPHRASE, EMAIL_PASSWORD, RSA_PRIVATE_KEY

pgp_key = serialization.load_pem_private_key(RSA_PRIVATE_KEY, password=RSA_PASSPHRASE, backend=default_backend())

SENDER_EMAIL = "app@munol.org"


def generate_login_code():
    characters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # Does not contain 0, O, 1, I as to not be ambiguous
    return ''.join(secrets.choice(characters) for _ in range(6))


class RequestLoginCodeView(APIView):
    def post(self, request):
        serializer = RequestLoginCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid request body."})
        email = serializer.validated_data["email"]
        try:
            participant = Participant.objects.get(email__exact=email)
        except Participant.DoesNotExist:
            # Migrate participant from old CMS
            try:
                migrated_data = get("https://app.munol.org/migrate_participants.php?email",
                                    headers={"X-Authorization": MIGRATE_TOKEN}, params={"email": email})
                if migrated_data.status_code != 200 and migrated_data.status_code != 403:
                    migrated_data.raise_for_status()
            except HTTPError:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                data={"detail": "Something went wrong while fetching participant data."})

            if migrated_data.status_code == 403:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"detail": "An account with the specified email "
                                                "address does not exist."})

            serializer = MigratedParticipantSerializer(data=migrated_data.json())
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                data={"detail": "Something went wrong while fetching participant data."})
            participant = serializer.save()

        participant.app_code = generate_login_code()
        participant.app_code_expires_by = timezone.now() + timedelta(minutes=15)
        participant.save()

        txt_template = loader.get_template("api/mobile_app/code_email.txt")
        html_template = loader.get_template("api/mobile_app/code_email.html")
        context = {"code": participant.app_code}
        email_txt = txt_template.render(context)
        email_html = html_template.render(context)

        for _ in range(0, 5):
            try:
                send_mail("MUNOL App verification code", email_txt, f'MUNOL App <{SENDER_EMAIL}>', [email],
                          html_message=email_html, auth_user=SENDER_EMAIL, auth_password=EMAIL_PASSWORD)
                return Response({"detail": "A login code was sent to your email address."})
            except SMTPException:
                pass
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"detail": "Failed to send email."})


class LoginView(APIView):
    def post(self, request):
        serializer = LoginCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid request body."})
        email = serializer.validated_data["email"].lower()
        code = serializer.validated_data["code"].upper()
        try:
            next_conference = Conference.objects.filter(enddate__gte=date.today()).order_by("enddate")[0]
        except Conference.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"detail": "There is no planned upcoming conference."})
        try:
            participant = Participant.objects.get(email__exact=email)
        except Participant.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"detail": "An account with the specified email address does not exist. "
                                            "If you are sure that this is a correct email address, contact app@munol.org."})
        if not participant.app_code or participant.app_code != code:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"detail": "The submitted code was not correct."})
        if participant.app_code_expires_by < timezone.now():
            return Response(status=status.HTTP_410_GONE,
                            data={"detail": "The login code expired."})

        participant.app_code = ""
        participant.app_code_expires_by = None
        participant.save()

        serializer = DigitalBadgeSerializer(participant)
        badge_data = serializer.data
        badge_data['exp'] = next_conference.enddate + timedelta(days=1)
        token = jwt.encode(badge_data, pgp_key, algorithm="RS256", json_encoder=DigitalBadgeEncoder)

        return Response({"digital_badge": token})


class DigitalBadgeEncoder(json.JSONEncoder):
    def encode(self, participant: Any) -> str:
        return str(JSONRenderer().render(participant))
