import jwt

from django.conf import settings
from django.contrib.auth.models import UserManager as SimpleUserManager
from django.utils import timezone


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

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class ActiveUserManager(UserManager):
    def get_queryset(self):
        queryset = super(ActiveUserManager, self).get_queryset()
        return queryset.filter(is_active=True)