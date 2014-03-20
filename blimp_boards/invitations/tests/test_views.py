from rest_framework import status
from rest_framework.test import APIClient

from ...utils.tests import BaseTestCase
from ...accounts.models import EmailDomain
from ..models import SignupRequest


class SignupRequestCreateAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()

        self.email = 'jpueblo@example.com'

        self.signup_request = SignupRequest.objects.create(email=self.email)

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'email': 'ppueblo@example.com'
        }

        response = self.client.post(
            '/api/auth/signup_request/', data, format='json')

        signup_request = SignupRequest.objects.get(email=data['email'])

        expected_response = {
            'email': signup_request.email
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/signup_request/')

        expected_response = {
            'error': {
                'email': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class InvitedUserCreateAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/signup_request/invite/'

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        self.create_user()
        self.create_account()

        self.account.allow_signup = True
        self.account.save()

        email_domain = EmailDomain.objects.create(domain_name='example.com')
        self.account.email_domains.add(email_domain)

        self.data = {
            'account': self.account.id,
            'email': 'jackson.flores78@example.com'
        }

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post(self.url)

        expected_response = {
            'error': {
                'account': ['This field is required.'],
                'email': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data_account_error(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        self.create_user()
        self.create_account()

        self.data = {
            'account': self.account.id,
            'email': 'jackson.flores78@example.com'
        }

        response = self.client.post(self.url, self.data, format='json')

        expected_response = {
            'error': {
                'account': [
                    'Account does not allow signup with email address.'
                ]
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)
