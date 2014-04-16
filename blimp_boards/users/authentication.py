from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class JWTAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        try:
            user = User.objects.get(
                pk=payload['user_id'],
                token_version=payload['token_version'],
                is_active=True
            )
        except User.DoesNotExist:
            msg = 'Invalid signature'
            raise exceptions.AuthenticationFailed(msg)

        return user


class SessionAuthentication(SessionAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def enforce_csrf(self, request):
        """
        Remove CSRF enforcement.
        """
        pass
