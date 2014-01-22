from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import User


class ValidateUsernameAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'username': 'jpueblo'
        }

        response = self.client.post(
            '/api/auth/username/validate/', data, format='json')

        expected_response = {
            'exists': False
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/username/validate/')

        expected_response = {
            'error': {
                'username': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class SignupAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'full_name': 'Juan Pueblo',
            'email': 'juan@example.com',
            'username': 'juan',
            'password': 'abc123',
            'account_name': 'Pueblo Co.',
            'allow_signup': True,
            'signup_domains': 'example.com,example2.com',
            'invite_emails': 'pedro@example.com,sara@example2.com'
        }

        response = self.client.post(
            '/api/auth/signup/', data, format='json')

        expected_response = {
            'email': 'juan@example.com',
            'full_name': 'Juan Pueblo',
            'first_name': 'Juan',
            'last_name': 'Pueblo',
            'account_name': 'Pueblo Co.',
            'username': 'juan',
            'allow_signup': True,
            'signup_domains': 'example.com,example2.com',
            'invite_emails': 'pedro@example.com,sara@example2.com'
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/signup/')

        expected_response = {
            'error': {
                'username': ['This field is required.'],
                'password': ['This field is required.'],
                'email': ['This field is required.'],
                'full_name': ['This field is required.'],
                'account_name': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class SigninAPIEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.username = 'jpueblo'
        self.password = 'abc123'
        self.email = 'jpueblo@example.com'

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name='Juan',
            last_name='Pueblo'
        )

    def test_post_valid_data_with_username(self):
        """
        Tests that POST request with valid username and password
        to endpoint returns expected data.
        """
        data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(
            '/api/auth/signin/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_post_valid_data_with_email(self):
        """
        Tests that POST request with valid email and password
        to endpoint returns expected data.
        """
        data = {
            'username': self.email,
            'password': self.password
        }

        response = self.client.post(
            '/api/auth/signin/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/signin/')

        expected_response = {
            'password': [
                'This field is required.'
            ],
            'username': [
                'This field is required.'
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data_wrong_credentials(self):
        """
        Tests that POST request with wrong credentials to endpoint
        returns expected error.
        """
        data = {
            'username': 'a',
            'password': 'b'
        }

        response = self.client.post(
            '/api/auth/signin/', data, format='json')

        expected_response = {
            'non_field_errors': [
                'Unable to login with provided credentials.'
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)
