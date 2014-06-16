import os
import mimetypes
import jwt
import requests

from django.conf import settings
from django.utils.log import getLogger
from django.utils.six.moves.urllib.parse import urlparse


logger = getLogger(__name__)


def is_raw_image(extension):
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

    return extension in raw_image_extensions


def get_parsed_file_from_url(url):
    """
    Returns a URL's file extension, mimetype, encoding, and type.
    """
    url_path = urlparse(url).path
    file_extension = os.path.splitext(url_path)[1].lower()
    file_mimetype, file_encoding = mimetypes.guess_type(url_path)

    return {
        'extension': file_extension,
        'mimetype': file_mimetype,
        'encoding': file_encoding,
        'type': file_mimetype.split('/')[0] if file_mimetype else None,
    }


def guess_output_format(url):
    """
    Returns the suggested FilePreviews.io thumbnail output format
    depending on the file.
    """
    output_format = 'png'
    parsed_file = get_parsed_file_from_url(url)

    if not parsed_file['mimetype']:
        return output_format

    jpg_conditions = [
        parsed_file['type'] == 'video',
        parsed_file['extension'] in ['.jpg', '.jpeg', '.tiff', '.tif'],
        is_raw_image(parsed_file['extension']),
    ]

    if any(jpg_conditions):
        output_format = 'jpg'

    return output_format


def guess_extra_data(url, output_format):
    """
    Returns unique list of suggested FilePreviews.io extra_data
    options for uploaded file.
    """
    extra_data = ['checksum']
    parsed_file = get_parsed_file_from_url(url)

    if parsed_file['type'] == 'image':
        extra_data.append('exif')

    if parsed_file['type'] in ['image', 'video']:
        extra_data.append('multimedia')

    psd_conditions = [
        parsed_file['mimetype'] == 'image/x-photoshop',
        parsed_file['mimetype'] == 'image/vnd.adobe.photoshop',
        parsed_file['extension'] == '.psd'
    ]

    if any(psd_conditions):
        extra_data.append('psd')

    if output_format != 'jpg':
        extra_data.append('ocr')

    if is_raw_image(parsed_file['extension']):
        extra_data.append('raw')

    return list(set(extra_data))


def queue_previews(url, sizes, metadata):
    """
    Requests preview from FilePreviews.io.
    extra_data: all, exif, psd, ocr, checksum, multimedia, raw
    """
    output_format = guess_output_format(url)
    extra_data = guess_extra_data(url, output_format)

    payload = {
        'api_key': settings.BLIMP_PREVIEWS_API_KEY,
        'url': url,
        'sizes': sizes,
        'metadata': metadata,
        'extra_data': extra_data,
        'format': output_format,
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
