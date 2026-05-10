import json
import os
import secrets
from typing import Any

import jwt

from datetime import date, timedelta, datetime
from smtplib import SMTPException

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone
from jwt import ExpiredSignatureError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mobile_app.models import ParticipantLoginData
from api.mobile_app.serializers import *
from api.models import Participant, Conference

APP_EMAIL = os.getenv("APP_EMAIL", None)
APP_EMAIL_PASSWORD = os.getenv("APP_EMAIL_PASSWORD", None)
DIGITAL_BADGE_PRIVATE_KEY = os.getenv("DIGITAL_BADGE_PRIVATE_KEY", None)
DIGITAL_BADGE_PUBLIC_KEY = os.getenv("DIGITAL_BADGE_PUBLIC_KEY", None)
DIGITAL_BADGE_KEY_PASSPHRASE = os.getenv("DIGITAL_BADGE_KEY_PASSPHRASE", None)
if DIGITAL_BADGE_KEY_PASSPHRASE is not None:
    DIGITAL_BADGE_KEY_PASSPHRASE = DIGITAL_BADGE_KEY_PASSPHRASE.encode()

digital_badge_private_key = None
if DIGITAL_BADGE_PRIVATE_KEY is not None:
    with open(DIGITAL_BADGE_PRIVATE_KEY, "rb") as f:
        digital_badge_private_key = serialization.load_pem_private_key(f.read(), password=DIGITAL_BADGE_KEY_PASSPHRASE, backend=default_backend())

digital_badge_public_key = None
if DIGITAL_BADGE_PUBLIC_KEY is not None:
    with open(DIGITAL_BADGE_PUBLIC_KEY, "rb") as f:
        digital_badge_public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

def generate_login_code():
    # Does not contain 0, O, 1, I as to not be ambiguous
    characters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
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
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"detail": "An account with the specified email "
                                            "address does not exist."})            

        
        app_code = generate_login_code()
        login_data = ParticipantLoginData(
            participant=participant,
            app_code=app_code,
            app_code_expires_by = timezone.now() + timedelta(minutes=15),
        )
        login_data.save()

        if email == "apple.tester@munol.org":
            return Response({"detail": "A login code was sent to your email address."})
        txt_template = loader.get_template("api/mobile_app/code_email.txt")
        html_template = loader.get_template("api/mobile_app/code_email.html")
        context = {"code": app_code}
        email_txt = txt_template.render(context)
        email_html = html_template.render(context)

        for _ in range(0, 5):
            try:
                send_mail("MUNOL App verification code", email_txt, f'MUNOL App <{APP_EMAIL}>', [email],
                          html_message=email_html, auth_user=APP_EMAIL, auth_password=APP_EMAIL_PASSWORD)
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

        upcoming_conferences = Conference.objects.filter(end_date__gte=date.today()).order_by("end_date")
        if len(upcoming_conferences) == 0:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"detail": "There is no planned upcoming conference."})
        next_conference = upcoming_conferences[0]

        try:
            participant = Participant.objects.get(email__exact=email)
        except Participant.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"detail": "An account with the specified email address does not exist. "
                                            f"If you are sure that this is a correct email address, contact {APP_EMAIL}."})
        if not (email == "apple.tester@munol.org" and code == "ABCDEF"):
            try:
                login_data = participant.participantlogindata
            except ParticipantLoginData.DoesNotExist:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"detail": "The submitted code was not correct."})
            if not login_data.app_code or login_data.app_code != code:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"detail": "The submitted code was not correct."})
            if login_data.app_code_expires_by < timezone.now():
                return Response(status=status.HTTP_410_GONE,
                                data={"detail": "The login code expired."})
            
            login_data.delete()

        serializer = DigitalBadgeSerializer(participant)
        badge_data = serializer.data
        badge_data['exp'] = datetime.combine(
            next_conference.end_date + timedelta(days=1), datetime.min.time())
        token = jwt.encode(badge_data, digital_badge_private_key, algorithm="RS256",
                           json_encoder=DigitalBadgeEncoder)

        return Response({"digital_badge": token})


class VerifyView(APIView):
    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid request body."})
        token = serializer.validated_data['token']
        try:
            jwt.decode(token, digital_badge_public_key, algorithms=["RS256"])
        except ExpiredSignatureError:
            return Response({"expired": True, "invalid": True})
        except:
            return Response({"expired": False, "invalid": True})
        return Response({"expired": False, "invalid": False})


class LoginProblemView(APIView):
    def post(self, request):
        serializer = LoginProblemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid request body."})
        email = serializer.validated_data['email']
        print("[Login Problem] " + email)

        for _ in range(0, 5):
            try:
                send_mail("MUNOL App Login Issue", f"User with E-Mail \"{email}\" reported a login problem.", f'MUNOL App <{APP_EMAIL}>',
                    [APP_EMAIL], auth_user=APP_EMAIL, auth_password=EMAIL_PASSWORD)
                return Response({"detail": "Your problem was reported."})
            except SMTPException:
                pass
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"detail": "Something went wrong."})


class DigitalBadgeEncoder(json.JSONEncoder):
    def encode(self, participant: Any) -> str:
        return JSONRenderer().render(participant).decode('utf-8')
