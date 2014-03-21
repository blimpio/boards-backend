import base64
import json
import datetime
import hmac
import hashlib
import uuid

from django.utils.encoding import smart_text, smart_bytes

from mock import Mock, patch

from ...utils.tests import BaseTestCase
from ..utils import generate_policy, generate_signature, generate_file_key


def mocked_now():
    return datetime.datetime(2014, 2, 25)


def mocked_uuid4():
    return uuid.UUID('16fd2706-8baf-433b-82eb-8c7fada847da')


class UtilsTestCase(BaseTestCase):
    @patch('blimp_boards.files.utils.now', mocked_now)
    def test_generate_policy_should_returns_base64_policy(self):
        """
        Tests that generate_policy returns a base64 encoded policy.
        """
        bucket = 'mybucket'
        mime_type = 'image/jpeg'
        file_size = 1000

        policy_base64 = generate_policy(bucket, mime_type, file_size)
        policy = json.loads(smart_text(base64.b64decode(policy_base64)))

        expected_policy = {
            'conditions': [
                {'bucket': 'mybucket'},
                {'acl': 'private'},
                {'content-type': 'image/jpeg'},
                {'success_action_status': '200'},
                ['starts-with', '$key', 'cards/'],
                ['content-length-range', 0, 1000]
            ],
            'expiration': '2014-02-26T00:00:00.000Z'
        }

        self.assertEqual(policy, expected_policy)

    def test_generate_signature_returns_base64_signed_policy(self):
        """
        Tests that generate_signature returns a base64 encoded signature.
        """
        bucket = 'mybucket'
        mime_type = 'image/jpeg'
        file_size = 1000
        secret = smart_bytes('mysecret')

        policy = generate_policy(bucket, mime_type, file_size)
        signature_base64 = generate_signature(policy, secret)
        signature_digest = base64.b64decode(signature_base64)
        hmac_signature = hmac.new(secret, policy, hashlib.sha1)

        self.assertEqual(signature_digest, hmac_signature.digest())

    @patch('blimp_boards.files.utils.uuid.uuid4', mocked_uuid4)
    def test_generate_file_key_should_return_key_path(self):
        """
        Tests that generate_file_key returns a correct path for file.
        """
        user = Mock()
        user.id = 1

        key = generate_file_key(name='photo.jpg', user=user)

        expected_key = ('cards/16fd2706-8baf-433b-82eb-8c7fada847da/photo.jpg')

        self.assertEqual(key, expected_key)
