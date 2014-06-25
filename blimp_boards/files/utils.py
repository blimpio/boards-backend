import json
import base64
import datetime
import hmac
import hashlib
import uuid
import time

from django.conf import settings
from django.utils.timezone import now
from django.utils.six.moves import urllib
from django.utils.encoding import smart_bytes, smart_text
from django.utils.log import getLogger


logger = getLogger(__name__)


def sign_s3_url(url, expires_in=None, response_headers=None):
    if not expires_in:
        expires_in = settings.AWS_SIGNATURE_EXPIRES_IN

    signer = S3UrlSigner(settings.AWS_ACCESS_KEY_ID,
                         settings.AWS_SECRET_ACCESS_KEY)

    return signer.sign_url('GET', url, expires_in, response_headers)


def generate_policy(bucket, mime_type, file_size):
    """
    Returns a Base64-encoded policy document that applies rules
    to file uploads sent by the S3 POST form. It is used to
    authorize the form, and to impose conditions on the files
    that can be uploaded.
    """
    tomorrow = now() + datetime.timedelta(hours=24)
    expiration = tomorrow.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    policy_object = {
        "expiration": expiration,
        "conditions": [
            {"bucket": bucket},
            {"acl": "private"},
            {"content-type": mime_type},
            {"success_action_status": "200"},
            ["starts-with", "$key", "cards/"],
            ["content-length-range", 0, file_size],
        ]
    }

    json_policy = json.dumps(
        policy_object).replace('\n', '').replace('\r', '')

    return base64.b64encode(smart_bytes(json_policy))


def generate_signature(policy, secret_key):
    """
    Returns a Base64-encoded signature value that authorizes
    the form and proves that only you could have created it.
    This value is calculated by signing the Base64-encoded
    policy document with your AWS Secret Key.
    """
    hmac_signature = hmac.new(
        smart_bytes(secret_key), smart_bytes(policy), hashlib.sha1)

    return base64.b64encode(hmac_signature.digest())


def generate_file_key(name=None):
    """
    Returns a string name for the S3 object that will
    store the uploaded file's data.

    TODO: Generate correct key depending on what object the file belongs.
    """
    key = 'cards/{}'.format(uuid.uuid4())

    if name:
        key = '{}/'.format(key, name)

    return key


class S3UrlSigner(object):
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint = 'https://s3.amazonaws.com'

    def generate_url(self, verb, key, bucket, expires_in_seconds,
                     response_headers=None):
        """
        Returns a full signed URL from a given verb, key,
        bucket, and expires_in_seconds.
        """
        key = urllib.parse.quote(key)

        expires = int(time.time() + expires_in_seconds)

        str = '{}\n\n\n{}\n/{}'.format(verb, expires, bucket)

        url = '{}/{}'.format(self.endpoint, bucket)

        if not key.startswith('/'):
            str = '{}/'.format(str)
            url = '{}/'.format(url)

        url = '{}{}'.format(url, key)
        str = '{}{}'.format(str, key)

        if response_headers:
            str = '{}?{}'.format(str, urllib.parse.urlencode(response_headers))

        signature = smart_text(generate_signature(str, self.secret_key))

        params = {
            'Expires': expires,
            'AWSAccessKeyId': self.access_key,
            'Signature': signature
        }

        if response_headers:
            params.update(response_headers)

        return '{}?{}'.format(url, urllib.parse.urlencode(params))

    def sign_url(self, verb, url, expires_in, response_headers=None):
        """
        Returns a full signed URL from a given verb,
        url, and expires_in_seconds.
        """
        if not url.startswith(self.endpoint):
            return None

        url = urllib.parse.urlparse(url)
        url = '{}://{}{}'.format(url.scheme, url.netloc, url.path)
        url = url.replace(self.endpoint, '')
        parts = url.split('/')
        bucket = parts[1]

        parts.remove(bucket)

        key = urllib.parse.unquote('/'.join(parts))

        return self.generate_url(verb, key, bucket, expires_in,
                                 response_headers)
