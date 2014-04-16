from rest_framework import status
from rest_framework.test import APIClient

from ...utils.tests import BaseTestCase, AuthenticatedAPITestCase
from ...accounts.models import Account
from ...invitations.models import SignupRequest, InvitedUser
from ..models import User
from ..serializers import UserSerializer


class ValidateUsernameAPIViewTestCase(BaseTestCase):
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
                'username': ['Username already exists.']
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


class SignupAPIViewTestCase(BaseTestCase):
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
            'account_logo_color': 'red',
            'allow_signup': True,
            'signup_domains': ['example.com', 'example2.com'],
            'invite_emails': ['pedro@example.com', 'sara@example2.com'],
            'signup_request_token': self.signup_request.token
        }

        response = self.client.post(
            '/api/auth/signup/', data, format='json')

        user = User.objects.get(username='juan')

        expected_response = UserSerializer(user).data

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
            'account_logo_color': 'red',
            'allow_signup': False,
            'signup_request_token': self.signup_request.token
        }

        response = self.client.post(
            '/api/auth/signup/', data, format='json')

        user = User.objects.get(username='juan')

        expected_response = UserSerializer(user).data

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
                'account_logo_color': ['This field is required.'],
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
            'account_logo_color': 'red',
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
        user = User.objects.create_user(
            username='jpueblo',
            email='jpueblo@example.com',
            password='abc123',
            first_name='Juan',
            last_name='Pueblo'
        )

        account = Account.personals.create(name='Acme', created_by=user)

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
            'account_logo_color': 'red',
            'invited_user_token': invited_user.token
        }

        response = self.client.post('/api/auth/signup/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)


class SigninAPIEndpoint(BaseTestCase):
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
            'username': 'myusername',
            'password': 'mypassword'
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
        account = Account.personals.create(name='Acme', created_by=self.user)

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


class SignupValidateTokenHTMLViewTestCase(BaseTestCase):
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


class SigninValidateTokenHTMLViewTestCase(BaseTestCase):
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


class ForgotPasswordAPIViewTestCase(BaseTestCase):
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


class ResetPasswordAPIViewTestCase(BaseTestCase):
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


class ResetPasswordHTMLView(BaseTestCase):
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


class UserSettingsAPIViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(UserSettingsAPIViewTestCase, self).setUp()

        self.url = '/api/users/me/'

    def test_get_for_loggedin_user(self):
        """
        Tests that endpoint returns expected response for logged in user.
        """
        response = self.client.get(self.url)
        expected_response = {
            'id': self.user.id,
            'username': self.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.email,
            'avatar_path': '',
            'gravatar_url': self.user.gravatar_url,
            'timezone': 'UTC',
            'date_created': self.user.date_created,
            'date_modified': self.user.date_modified,
            'token': self.user.token
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_get_for_loggedout_user(self):
        """
        Tests that endpoint only works for logged in users.
        """
        self.client = APIClient()
        response = self.client.get(self.url)
        expected_response = {}

        expected_response = {
            'error': 'Authentication credentials were not provided.',
            'status_code': 401
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected_response)

    def test_update_should_update_logged_in_user(self):
        """
        Tests that endpoint can be used to update logged in user's data.
        """
        data = {
            'email': 'anotheremail@example.com'
        }

        response = self.client.patch(self.url, data)

        self.user = User.objects.get(username=self.username)

        expected_response = {
            'id': self.user.id,
            'username': self.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': 'anotheremail@example.com',
            'avatar_path': '',
            'gravatar_url': self.user.gravatar_url,
            'timezone': 'UTC',
            'date_created': self.user.date_created,
            'date_modified': self.user.date_modified,
            'token': self.user.token
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)


class ChangePasswordAPIViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(ChangePasswordAPIViewTestCase, self).setUp()

        self.url = '/api/users/me/change_password/'

    def test_post_for_loggedin_user_invalid_current_password(self):
        """
        Tests that endpoint checks for user's current password.
        """
        data = {
            'current_password': 'notmypassword',
            'password1': 'abc123',
            'password2': 'abc123'
        }

        response = self.client.post(self.url, data)

        expected_response = {
            'error': {
                'current_password': ['Current password is invalid.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_for_loggedin_user_valid_current_password(self):
        """
        Tests that endpoint changes user's password.
        """
        data = {
            'current_password': self.password,
            'password1': 'mynewpassword',
            'password2': 'mynewpassword'
        }

        response = self.client.post(self.url, data)

        self.user = User.objects.get(username=self.username)

        expected_response = {
            'id': self.user.id,
            'username': self.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'avatar_path': '',
            'gravatar_url': self.user.gravatar_url,
            'timezone': 'UTC',
            'date_created': self.user.date_created,
            'date_modified': self.user.date_modified,
            'token': self.user.token
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
        self.assertTrue(self.user.check_password('mynewpassword'))
