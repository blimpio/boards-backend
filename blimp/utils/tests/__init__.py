from django.test import TestCase
from rest_framework.test import APIClient

from ...users.models import User
from ...utils.jwt_handlers import jwt_payload_handler, jwt_encode_handler


class AuthenticatedAPITestCase(TestCase):
    """
    This test case class creates a basic user
    and does authentication for you using a JWT token
    """
    def setUp(self):
        self.username = 'jpueblo'
        self.email = 'jpueblo@example.com'
        self.password = 'abc123'
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
