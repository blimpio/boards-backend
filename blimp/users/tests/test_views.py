from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ...accounts.models import Account
from ...invitations.models import SignupRequest, InvitedUser
from ...utils.jwt_handlers import jwt_payload_handler, jwt_encode_handler
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
            'invite_emails': ['pedro@example.com', 'sara@example2.com'],
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

    def test_post_invalid_data_with_invited_user_token(self):
        """
        Tests that POST request with an invalid invited_user_token
        returns  the expected error.
        """
        data = {
            'full_name': 'Juan Pueblo',
            'email': self.email,
            'username': 'juan',
            'password': 'abc123',
            'account_name': 'Pueblo Co.',
            'allow_signup': False,
            'invited_user_token': 'invalidtoken'
        }

        response = self.client.post('/api/auth/signup/', data, format='json')

        expected_response = {
            'error': {
                'invited_user_token': ['No invited user found for token.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_valid_data_with_invited_user_token(self):
        """
        Tests that POST request with an valid invited_user_token
        returns a token.
        """
        account = Account.objects.create(name='Acme')

        user = User.objects.create_user(
            username='jpueblo',
            email='jpueblo@example.com',
            password='abc123',
            first_name='Juan',
            last_name='Pueblo'
        )

        invited_user = InvitedUser.objects.create(
            first_name='Roberto', last_name='Pueblo',
            email='rpueblo@example.com', account=account,
            created_by=user
        )

        data = {
            'full_name': 'Roberto Pueblo',
            'email': 'rpueblo@example.com',
            'username': 'roberto',
            'password': 'abc123',
            'invited_user_token': invited_user.token
        }

        response = self.client.post('/api/auth/signup/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)


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

    def test_post_invalid_data_with_invited_user_token(self):
        """
        Tests that POST request with an invalid invited_user_token
        returns  the expected error.
        """
        data = {
            'username': self.username,
            'password': self.password,
            'invited_user_token': 'invalidtoken'
        }

        response = self.client.post('/api/auth/signin/', data, format='json')

        expected_response = {
            'error': {
                'invited_user_token': ['No invited user found for token.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_valid_data_with_invited_user_token(self):
        """
        Tests that POST request with an valid invited_user_token
        returns a token.
        """
        account = Account.objects.create(name='Acme')

        invited_user = InvitedUser.objects.create(
            first_name='Juan', last_name='Pueblo',
            email='juanpueblo@example.com', account=account,
            created_by=self.user
        )

        data = {
            'username': self.username,
            'password': self.password,
            'invited_user_token': invited_user.token
        }

        response = self.client.post('/api/auth/signin/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)


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

        self.url = '/signup/'

    def test_view_should_not_allow_post_method(self):
        """
        Tests that view returns methods now allowed.
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_view_should_allow_get_method(self):
        """
        Tests that view allows GET.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_should_render_html_template(self):
        """
        Tests that view renders our expected template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

    def test_view_should_raise_404_invalid_token(self):
        """
        Tests that view raises 404 for invalid tokens.
        """
        response = self.client.get(self.url, {'token': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_should_raise_404_invalid_invited_user_token(self):
        """
        Tests that view raises 404 for invalid invite tokens.
        """
        response = self.client.get(self.url, {'invite': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_should_redirect_to_sigin_if_invited_user_has_user(self):
        """
        Tests that view redirects to signin if invited_user
        has a user associated to it.
        """
        account = Account.objects.create(name='Acme')

        invited_user = InvitedUser.objects.create(
            account=account, created_by=self.user, user=self.user
        )

        response = self.client.get(self.url, {'invite': invited_user.token})

        expected_url = '/signin/?invite={}'.format(invited_user.token)

        self.assertRedirects(response, expected_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class SigninValidateTokenHTMLViewTestCase(TestCase):
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

        self.url = '/signin/'

    def test_view_should_not_allow_post_method(self):
        """
        Tests that view returns methods now allowed.
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_view_should_allow_get_method(self):
        """
        Tests that view allows GET.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_should_render_html_template(self):
        """
        Tests that view renders our expected template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

    def test_view_should_raise_404_invalid_invited_user_token(self):
        """
        Tests that view raises 404 for invalid invite tokens.
        """
        response = self.client.get(self.url, {'invite': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_should_redirect_to_signup_if_invited_user_has_no_user(self):
        """
        Tests that view redirects to signup if invited_user has
        no user associated with it.
        """
        account = Account.objects.create(name='Acme')

        invited_user = InvitedUser.objects.create(
            first_name='Roberto', last_name='Pueblo',
            email='rpueblo@example.com', account=account,
            created_by=self.user
        )

        response = self.client.get(self.url, {'invite': invited_user.token})

        expected_url = '/signup/?invite={}'.format(invited_user.token)

        self.assertRedirects(response, expected_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


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
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_view_should_allow_get_method(self):
        """
        Tests that view allows GET.
        """
        response = self.client.get(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
