from rest_framework import exceptions
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

try:
    from django.contrib.auth import get_user_model
except ImportError:  # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class JWTAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        try:
            user = User.objects.get(
                pk=payload['user_id'],
                email=payload['email'],
                token_version=payload['token_version'],
                is_active=True
            )
        except User.DoesNotExist:
            msg = 'Invalid signature'
            raise exceptions.AuthenticationFailed(msg)

        return user
