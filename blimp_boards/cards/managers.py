import jwt

from django.db import models
from django.conf import settings


class CardManager(models.Manager):
    def get_from_download_token(self, token, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            raise self.model.DoesNotExist

        payload_type = payload.get('type')
        payload_id = payload.get('id')

        if payload_type == 'CardDownload' and payload_id:
            return self.get(id=payload_id, **kwargs)

        raise self.model.DoesNotExist
