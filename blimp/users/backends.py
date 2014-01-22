from django.contrib.auth.backends import ModelBackend

from blimp.utils.validators import is_valid_email
from .models import User


class EmailBackend(ModelBackend):
    """
    Overwrites the default backend to check for e-mail address
    """
    def authenticate(self, username=None, password=None):
        """
        If username is an email address, then try to find
        User via email. If username is not an email addres,
        then try to find User via username.
        """
        if is_valid_email(username):
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
