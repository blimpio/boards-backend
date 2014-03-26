import jwt
import requests

from django.conf import settings
from django.utils.log import getLogger


logger = getLogger(__name__)


def queue_previews(url, sizes, metadata):
    payload = {
        'accountId': settings.BLIMP_PREVIEWS_ACCOUNT_ID,
        'url': url,
        'sizes': sizes,
        'metadata': metadata
    }

    token = jwt.encode(payload, settings.BLIMP_PREVIEWS_SECRET_KEY)

    headers = {
        'content-type': 'text/plain'
    }

    try:
        logger.info('Requesting previews for {}'.format(url))

        if settings.ENVIRONMENT == 'DEVELOPMENT':
            verify = False
        else:
            verify = '{}/certs/blimp-previews.crt'.format(settings.BASE_DIR)

        request = requests.post(
            settings.BLIMP_PREVIEWS_URL, data=token,
            headers=headers, verify=verify)

        logger.info(request.json())
    except Exception as e:
        logger.exception(e)


def decode_previews_payload(token):
    try:
        payload = jwt.decode(token, settings.BLIMP_PREVIEWS_SECRET_KEY)
    except:
        payload = None

    return payload
