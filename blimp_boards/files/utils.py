import json
import base64
import datetime
import hmac
import hashlib
import uuid
import time
import Crypto.Hash.SHA
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5

from django.conf import settings
from django.utils.timezone import now
from django.utils.six.moves.urllib.parse import urlencode, quote, urlparse
from django.utils.encoding import smart_bytes, smart_text


def sign_s3_url(url, expires_in=None, response_headers=None):
    if not expires_in:
        expires_in = settings.AWS_SIGNATURE_EXPIRES_IN

    signer = S3UrlSigner(settings.AWS_ACCESS_KEY_ID,
                         settings.AWS_SECRET_ACCESS_KEY)

    return signer.sign_url('GET', url, expires_in, response_headers)


def sign_cloudfront_url(url, expires_in=None, response_headers=None):
    """
    If CLOUDFRONT_* settings are available return signed CloudFront URL,
    if not fallback to returning signed S3 URL.
    """
    if not expires_in:
        expires_in = settings.AWS_SIGNATURE_EXPIRES_IN

    try:
        signer = CloudFrontSigner(settings.CLOUDFRONT_SUBDOMAIN,
                                  settings.CLOUDFRONT_KEY_PAIR_ID,
                                  settings.CLOUDFRONT_PRIVATE_KEY)

        return signer.sign_url(url, expires_in)
    except:
        return sign_s3_url(url, expires_in)


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


def generate_file_key(name=None, user=None):
    """
    Returns a string name for the S3 object that will
    store the uploaded file's data.

    TODO: Generate correct key depending on what object the file belongs.
    """
    return 'cards/{}/{}'.format(uuid.uuid4(), name)


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
        key = quote(key)

        expires = int(time.time() + expires_in_seconds)

        str = '{}\n\n\n{}\n/{}'.format(verb, expires, bucket)

        url = '{}/{}'.format(self.endpoint, bucket)

        if not key.startswith('/'):
            str = '{}/'.format(str)
            url = '{}/'.format(url)

        url = '{}{}'.format(url, key)
        str = '{}{}'.format(str, key)

        if response_headers:
            str = '{}?{}'.format(str, urlencode(response_headers))

        signature = smart_text(generate_signature(str, self.secret_key))

        params = {
            'Expires': expires,
            'AWSAccessKeyId': self.access_key,
            'Signature': signature
        }

        if response_headers:
            params.update(response_headers)

        return '{}?{}'.format(url, urlencode(params))

    def sign_url(self, verb, url, expires_in, response_headers=None):
        """
        Returns a full signed URL from a given verb,
        url, and expires_in_seconds.
        """
        if not url.startswith(self.endpoint):
            return None

        url = urlparse(url)
        url = '{}://{}{}'.format(url.scheme, url.netloc, url.path)
        url = url.replace(self.endpoint, '')
        parts = url.split('/')
        bucket = parts[1]

        parts.remove(bucket)

        key = '/'.join(parts)

        return self.generate_url(verb, key, bucket, expires_in,
                                 response_headers)


class CloudFrontSigner(object):
    def __init__(self, subdomain, key_pair_id, private_key):
        self.s3_endpoint = 'https://s3.amazonaws.com'
        self.cf_endpoint = 'https://{}.cloudfront.net'.format(subdomain)
        self.key_pair_id = key_pair_id

        if private_key.startswith == '-----BEGIN RSA PRIVATE KEY-----':
            self.private_key = private_key
        elif private_key.endswith('.pem'):
            self.private_key = open(private_key, 'r').read()

    def _generate_signature(self, message):
        key = Crypto.PublicKey.RSA.importKey(self.private_key)
        signer = Crypto.Signature.PKCS1_v1_5.new(key)
        sha1_hash = Crypto.Hash.SHA.new()

        sha1_hash.update(smart_bytes(message))

        return signer.sign(sha1_hash)

    def _generate_encoded_signature(self, message):
        encoded = smart_text(base64.b64encode(smart_bytes(message)))

        return encoded.replace('+', '-').replace('=', '_').replace('/', '~')

    def _generate_url(self, url, expires_in, encoded_signature):
        params = urlencode({
            'Expires': expires_in,
            'Signature': encoded_signature,
            'Key-Pair-Id': self.key_pair_id
        })

        return url + '?' + params

    def _generate_canned_policy_url(self, url, expires_in):
        canned_policy = {
            'Statement': [{
                'Resource': url,
                'Condition': {
                    'DateLessThan': {
                        'AWS:EpochTime': expires_in
                    }
                }
            }]
        }

        json_canned_policy = json.dumps(canned_policy, separators=(',', ':'))
        signature = self._generate_signature(json_canned_policy)
        encoded_signature = self._generate_encoded_signature(signature)

        return self._generate_url(url, expires_in, encoded_signature)

    def sign_url(self, url, expires_in_seconds):
        """
        Returns a full signed URL from a given url, and expires_in_seconds.
        """
        expires = int(time.time() + expires_in_seconds)

        if url.startswith(self.s3_endpoint):
            return self.sign_s3_url(url, expires_in_seconds)

        return self._generate_canned_policy_url(url, expires)

    def sign_s3_url(self, url, expires_in_seconds):
        """
        Returns a signed CloudFront URL from a given
        S3 URL and expires_in_seconds.
        """
        url = urlparse(url)
        url = '{}://{}{}'.format(url.scheme, url.netloc, url.path)
        url = url.replace(self.s3_endpoint, '')
        parts = url.split('/')
        bucket = parts[1]

        parts.remove(bucket)

        key = quote('/'.join(parts))

        cloudfront_url = '{}{}'.format(self.cf_endpoint, key)

        return self.sign_url(cloudfront_url, expires_in_seconds)
