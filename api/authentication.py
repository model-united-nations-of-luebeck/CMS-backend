import jwt
from jwt import PyJWKClient
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class AzureADJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None

        token = auth.split(" ")[1]
        try:
            # Get signing keys
            jwks_client = PyJWKClient(settings.AZURE_JWKS_URL)
            signing_key = jwks_client.get_signing_key_from_jwt(token).key

            decoded = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience=settings.AZURE_AUDIENCE,
                issuer=settings.AZURE_ISSUER,
            )

            username = decoded.get("preferred_username") or decoded.get("email")
            if not username:
                raise AuthenticationFailed("No username in token")

            user, created = User.objects.get_or_create(username=username, defaults={
                "email": username,
                "is_staff": True,  # Grant staff access for organizers
            })

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f"Invalid token: {e}")
