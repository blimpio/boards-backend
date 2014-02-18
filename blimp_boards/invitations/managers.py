import jwt

from django.db import models
from django.conf import settings


class SignupRequestManager(models.Manager):
    def get_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            return None

        payload_type = payload.get('type')
        payload_email = payload.get('email')

        if payload_type == 'SignupRequest' and payload_email:
            try:
                return self.get(email=payload_email)
            except self.model.DoesNotExist:
                pass

        return None


class InvitedUserManager(models.Manager):
    def get_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            return None

        payload_type = payload.get('type')
        payload_pk = payload.get('pk')

        if payload_type == 'InvitedUser' and payload_pk:
            try:
                return self.get(pk=payload_pk)
            except self.model.DoesNotExist:
                pass

        return None
