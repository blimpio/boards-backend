import jwt

from django.contrib.auth.models import UserManager as SimpleUserManager
from django.conf import settings


class UserManager(SimpleUserManager):
    def get_from_password_reset_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            return None

        payload_type = payload.get('type')
        user_id = payload.get('id')
        user_token_version = payload.get('token_version')

        if payload_type == 'PasswordReset' and user_id and user_token_version:
            try:
                return self.get(pk=user_id, token_version=user_token_version)
            except self.model.DoesNotExist:
                pass

        return None
