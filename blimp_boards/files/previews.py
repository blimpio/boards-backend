import jwt
import requests

from django.conf import settings


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

    request = requests.post(
        settings.BLIMP_PREVIEWS_URL, data=token, headers=headers)

    print(request.json())


def decode_previews_payload(token):
    try:
        payload = jwt.decode(token, settings.BLIMP_PREVIEWS_SECRET_KEY)
    except:
        payload = None

    return payload
