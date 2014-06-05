import os
import mimetypes
import jwt
import requests

from django.conf import settings
from django.utils.log import getLogger
from django.utils.six.moves.urllib.parse import urlparse


logger = getLogger(__name__)


def guess_output_format(url):
    output_format = 'png'
    url_path = urlparse(url).path
    file_extension = os.path.splitext(url_path)[1].lower()
    file_mimetype, file_encoding = mimetypes.guess_type(url_path)

    if not file_mimetype:
        return output_format

    file_type = file_mimetype.split('/')[0]

    raw_image_extensions = [
        '.arw', '.crw', '.cr2', '.nef'
        '.3fr',
        '.ari', '.arw',
        '.bay',
        '.crw', '.cr2', '.cap',
        '.dcs', '.dcr', '.dng', '.drf',
        '.eip', '.erf',
        '.fff',
        '.iiq',
        '.k25', '.kdc',
        '.mdc', '.mef', '.mos', '.mrw',
        '.nef', '.nrw',
        '.obm', '.orf',
        '.pef', '.ptx', '.pxn',
        '.r3d', '.raf', '.raw', '.rwl', '.rw2', '.rwz',
        '.sr2', '.srf', '.srw',
        '.x3f'
    ]

    jpg_conditions = [
        file_type == 'video',
        file_extension in ['.jpg', '.jpeg', '.tiff', '.tif'],
        file_extension in raw_image_extensions
    ]

    if any(jpg_conditions):
        output_format = 'jpg'

    return output_format


def queue_previews(url, sizes, metadata):
    payload = {
        'account_key': settings.BLIMP_PREVIEWS_ACCOUNT_ID,
        'url': url,
        'sizes': sizes,
        'metadata': metadata,
        'extra_data': ['all'],
        'format': guess_output_format(url),
        'uploader': {
            'headers': {
                'Cache-Control': 'max-age=315360000, no-transform, private',
                'x-amz-acl': 'private'
            }
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
