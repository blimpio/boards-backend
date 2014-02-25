import json
import base64
import datetime
import hmac
import hashlib
import uuid

from django.utils.encoding import smart_bytes
from django.utils.timezone import now


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
            {"acl": "public-read"},
            {"content-type": mime_type},
            {"success_action_status": "200"},
            ["starts-with", "$key", "uploads/"],
            ["content-length-range", 0, file_size],
        ]
    }

    json_policy = json.dumps(
        policy_object).replace('\n', '').replace('\r', '')

    return base64.b64encode(smart_bytes(json_policy))


def generate_signed_policy(policy, secret_key):
    """
    Returns a Base64-encoded signature value that authorizes
    the form and proves that only you could have created it.
    This value is calculated by signing the Base64-encoded
    policy document with your AWS Secret Key.
    """
    hmac_signature = hmac.new(
        smart_bytes(secret_key), policy, hashlib.sha1)

    return base64.b64encode(hmac_signature.digest())


def generate_file_key(name=None, user=None):
    """
    Returns a string name for the S3 object that will
    store the uploaded file's data.

    TODO: Generate correct key depending on what object the file belongs.
    """
    return 'uploads/cards/{}/{}/{}'.format(user.id, uuid.uuid4(), name)
