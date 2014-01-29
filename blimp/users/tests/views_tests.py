from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from blimp.invitations.models import SignupRequest
from blimp.utils.jwt_handlers import jwt_payload_handler, jwt_encode_handler
from ..models import User


class ValidateUsernameAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.username = 'jpueblo'
        self.password = 'abc123'
        self.email = 'jpueblo@example.com'

        self.user = User.objects.create_user(
            username=self.username,
            email='jpueblo@example.com',
            password=self.password,
            first_name='Juan',
            last_name='Pueblo'
        )

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'username': 'pedro'
        }

        response = self.client.post(
            '/api/auth/username/validate/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_post_valid_data_taken_username(self):
        """
        Tests that POST request with taken username to endpoint
        returns expected error.
        """
        data = {
            'username': self.username
        }

        response = self.client.post(
            '/api/auth/username/validate/', data, format='json')

        expected_response = {
            'error': {
                'username': ['Username is already taken.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
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

        self.email = 'juan@example.com'

        self.signup_request = SignupRequest.objects.create(email=self.email)

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'full_name': 'Juan Pueblo',
            'email': self.email,
            'username': 'juan',
            'password': 'abc123',
            'account_name': 'Pueblo Co.',
            'allow_signup': True,
            'signup_domains': ['example.com', 'example2.com'],
            'invite_emails': 'pedro@example.com,sara@example2.com',
            'signup_request_token': self.signup_request.token
        }

        response = self.client.post(
            '/api/auth/signup/', data, format='json')

        user = User.objects.get(username='juan')
        payload = jwt_payload_handler(user)

        expected_response = {
            'token': jwt_encode_handler(payload)
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_valid_data_simple(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data. Skips signup domains and invites.
        """
        data = {
            'full_name': 'Juan Pueblo',
            'email': self.email,
            'username': 'juan',
            'password': 'abc123',
            'account_name': 'Pueblo Co.',
            'allow_signup': False,
            'signup_request_token': self.signup_request.token
        }

        response = self.client.post(
            '/api/auth/signup/', data, format='json')

        user = User.objects.get(username='juan')
        payload = jwt_payload_handler(user)

        expected_response = {
            'token': jwt_encode_handler(payload)
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
                'account_name': ['This field is required.'],
                'signup_request_token': ['This field is required.']
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
            'error': {
                'password': [
                    'This field is required.'
                ],
                'username': [
                    'This field is required.'
                ]
            }
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

        response = self.client.post('/api/auth/signin/', data, format='json')

        expected_response = {
            'error': {
                'non_field_errors': [
                    'Unable to login with provided credentials.'
                ]
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class SignupValidateTokenHTMLViewTestCase(TestCase):
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

    def test_view_should_not_allow_post_method(self):
        """
        Tests that view returns methods now allowed.
        """
        response = self.client.post('/signup/')
        self.assertEqual(response.status_code, 405)

    def test_view_should_allow_get_method(self):
        """
        Tests that view allows GET.
        """
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_should_render_html_template(self):
        """
        Tests that view renders our expected template.
        """
        response = self.client.get('/signup/')
        self.assertTemplateUsed(response, 'index.html')

    def test_view_should_raise_404_invalid_token(self):
        """
        Tests that view raises 404 for invalid tokens.
        """
        response = self.client.get('/signup/', {'token': 'abc'})
        self.assertEqual(response.status_code, 404)


class ForgotPasswordAPIViewTestCase(TestCase):
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

        self.url = '/api/auth/forgot_password/'

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'email': self.email,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post(self.url)

        expected_response = {
            'error': {
                'email': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class ResetPasswordAPIViewTestCase(TestCase):
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

        self.url = '/api/auth/reset_password/'

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'token': self.user.password_reset_token,
            'password': 'newpassword'
        }

        response = self.client.post(self.url, data, format='json')

        expected_response = {
            'password_reset': True
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post(self.url)

        expected_response = {
            'error': {
                'token': ['This field is required.'],
                'password': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class ResetPasswordHTMLView(TestCase):
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

        self.data = {
            'token': self.user.password_reset_token
        }

        self.url = '/reset_password/'

    def test_view_should_not_allow_post_method(self):
        """
        Tests that view returns methods now allowed.
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_view_should_allow_get_method(self):
        """
        Tests that view allows GET.
        """
        response = self.client.get(self.url, self.data)
        self.assertEqual(response.status_code, 200)

    def test_view_should_render_html_template(self):
        """
        Tests that view renders our expected template.
        """
        response = self.client.get(self.url, self.data)
        self.assertTemplateUsed(response, 'index.html')

    def test_view_should_raise_404_invalid_token(self):
        """
        Tests that view raises 404 for invalid tokens.
        """
        response = self.client.get(self.url, {'token': 'abc'})
        self.assertEqual(response.status_code, 404)
