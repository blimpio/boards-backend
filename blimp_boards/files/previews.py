import jwt
import requests

from django.conf import settings
from django.utils.log import getLogger


logger = getLogger(__name__)


def queue_previews(url, sizes, metadata):
    payload = {
        'account_key': settings.BLIMP_PREVIEWS_ACCOUNT_ID,
        'url': url,
        'sizes': sizes,
        'metadata': metadata,
        'extra_data': {
            'ocr': True,
            'exif': True,
            'psd_layers': True
        }
    }

    token = jwt.encode(payload, settings.BLIMP_PREVIEWS_SECRET_KEY)

    headers = {
        'content-type': 'text/plain'
    }

    try:
        logger.info('Requesting previews for {}'.format(url))

        request = requests.post(
            settings.BLIMP_PREVIEWS_URL, data=token, headers=headers)

        logger.info(request.text)
    except Exception as e:
        logger.exception(e)


def decode_previews_payload(token):
    try:
        payload = jwt.decode(token, settings.BLIMP_PREVIEWS_SECRET_KEY)
    except:
        payload = None

    return payload
