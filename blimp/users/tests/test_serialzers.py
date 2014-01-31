from django.test import TestCase

from blimp.accounts.models import Account, AccountCollaborator
from blimp.invitations.models import SignupRequest, InvitedUser
from blimp.utils.jwt_handlers import jwt_payload_handler, jwt_encode_handler
from ..models import User
from ..serializers import (ValidateUsernameSerializer, SignupSerializer,
                           ForgotPasswordSerializer, ResetPasswordSerializer)


class ValidateUsernameSerializerTestCase(TestCase):
    def setUp(self):
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
            'username': 'pedro'
        }

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = ValidateUsernameSerializer()
        self.assertEqual(serializer.data, {'username': ''})

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = ValidateUsernameSerializer(data={})
        serializer.is_valid()
        expected_errors = {
            'username': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_object_should_have_username_key(self):
        """
        Tests that serializer.object should be a dictionary
        with an username key.
        """
        serializer = ValidateUsernameSerializer(data=self.data)
        serializer.is_valid()

        self.assertTrue('username' in serializer.object)

    def test_serializer_should_return_error_if_user_exists(self):
        """
        Tests that serializer should return error if user exists.
        """
        self.data['username'] = self.username
        serializer = ValidateUsernameSerializer(data=self.data)
        serializer.is_valid()

        expected_errors = {
            'username': ['Username is already taken.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_return_data_if_valid(self):
        """
        Tests that serializer should return data if user doesn't exists.
        """
        serializer = ValidateUsernameSerializer(data=self.data)
        serializer.is_valid()

        self.assertEqual(serializer.object, self.data)


class SignupSerializerTestCase(TestCase):
    def setUp(self):
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

        self.signup_request = SignupRequest.objects.create(
            email='juan@example.com')

        self.data = {
            'full_name': 'Juan Pueblo',
            'email': 'juan@example.com',
            'username': 'juan',
            'password': 'abc123',
            'account_name': 'Pueblo Co.',
            'allow_signup': False,
            'signup_request_token': self.signup_request.token
        }

    def test_serializer_empty_object(self):
        """
        Tests that serializer.object returns expected data when empty.
        """
        serializer = SignupSerializer()
        self.assertEqual(serializer.object, None)

    def test_serializer_should_return_expected_data_if_valid(self):
        """
        Tests that serializer.object should return expected data when valid.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()

        user = User.objects.get(username='juan')
        payload = jwt_payload_handler(user)

        expected_data = {
            'token': jwt_encode_handler(payload)
        }

        self.assertEqual(serializer.object, expected_data)

    def test_serializer_should_validate_token_not_found(self):
        """
        Tests that serializer should return an error if a signup request
        is not found for a token.
        """
        self.data['signup_request_token'] = 'nonexistent'

        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'signup_request_token': ['No signup request found for token.']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_validate_token_email_no_match(self):
        """
        Tests that serializer should return an error if a signup request
        email does not match signup email.
        """
        self.data['signup_request_token'] = 'nonexistent'
        signup_request = SignupRequest.objects.create(email=self.email)
        self.data['signup_request_token'] = signup_request.token

        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'signup_request_token': [
                'Signup request email does not match email.'
            ]
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_return_error_email_exists(self):
        """
        Tests that serializer should return an error if an email exists.
        """
        self.data['email'] = 'jpueblo@example.com'
        signup_request = SignupRequest.objects.create(email=self.data['email'])
        self.data['signup_request_token'] = signup_request.token

        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'email': ['Email already exists.']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_return_error_invalid_username(self):
        """
        Tests that serializer should return error if username is invalid.
        """
        self.data['username'] = 'jpueblo@example.com'
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'username': ['Invalid username.']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_return_error_username_exists(self):
        """
        Tests that serializer should return error if username exists.
        """
        self.data['username'] = 'jpueblo'
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'username': ['Username already exists.']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_return_error_invalid_signup_domain(self):
        """
        Tests that serializer should return error if signup
        domain is invalid.
        """
        self.data.update({
            'allow_signup': True,
            'signup_domains': ['gmail.com']
        })

        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'signup_domains': ["gmail.com is an invalid sign-up domain."]
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_return_error_invalid_invite_email(self):
        """
        Tests that serializer should return error if invite
        email is invalid.
        """
        self.data.update({
            'allow_signup': True,
            'signup_domains': ['example.com'],
            'invite_emails': ['@example.com'],
        })

        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'invite_emails': ['@example.com is not a valid email address.']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_signup_should_return_created_user(self):
        """
        Tests that serializer.signup() should return the created user.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_user = User.objects.filter(username=self.data['username'])

        self.assertEqual(expected_user.count(), 1)

    def test_create_user_should_return_created_user(self):
        """
        Tests that serializer.create_user() should return the created user.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_user = User.objects.filter(username=self.data['username'])

        self.assertEqual(expected_user.count(), 1)

    def test_create_account_should_return_created_account(self):
        """
        Tests that serializer should create an account
        and owner when validated.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_account = Account.objects.filter(slug='pueblo-co')

        self.assertEqual(expected_account.count(), 1)

    def test_create_account_should_return_created_owner(self):
        """
        Tests that serializer should create an account
        and owner when validated.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        user = User.objects.get(username=self.data['username'])
        expected_account = Account.objects.get(slug='pueblo-co')
        expected_owner = AccountCollaborator.objects.filter(
            account=expected_account, user=user, is_owner=True)

        self.assertEqual(expected_owner.count(), 1)

    def test_invite_users_should_return_invited_users(self):
        """
        Tests that serializer.invite_users should return a list of
        the invited users.
        """
        self.data.update({
            'allow_signup': True,
            'signup_domains': ['example.com'],
            'invite_emails': ['ppueblo@example.com', 'qpueblo@example.com'],
        })

        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        invited_users = InvitedUser.objects.filter(
            email__in=['ppueblo@example.com', 'qpueblo@example.com'])

        self.assertEqual(invited_users.count(), 2)

    def test_serializer_should_validate_password_requirements(self):
        """
        Tests that serializer validates password field.
        """
        self.data['password'] = 'a.'
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'password': [
                'Ensure this value has at least 6 characters (it has 2).'
            ]
        }

        self.assertEqual(serializer.errors, expected_error)


class ForgotPasswordSerializerTestCase(TestCase):
    def setUp(self):
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

        self.data = {
            'email': self.email
        }

    def test_serializer_empty_object(self):
        """
        Tests that serializer.object returns expected data when empty.
        """
        serializer = ForgotPasswordSerializer()
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {'email': ''})

    def test_serializer_should_return_expected_data_if_valid(self):
        """
        Tests that serializer.object should return expected data when valid.
        """
        serializer = ForgotPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_data = {
            'email': self.email
        }

        self.assertEqual(serializer.object, expected_data)

    def test_serializer_should_return_expected_error_email_required(self):
        """
        Tests that serializer.errors should return expected
        error when invalid.
        """
        self.data['email'] = None
        serializer = ForgotPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'email': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_error)
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {'email': ''})

    def test_serializer_should_return_expected_error_no_user_found(self):
        """
        Tests that serializer.object should return expected
        error when no user found for given email.
        """
        self.data['email'] = 'nonexistent@example.com'
        serializer = ForgotPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'email': ['No user found.']
        }

        self.assertEqual(serializer.errors, expected_error)
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {'email': ''})


class ResetPasswordSerializerTestCase(TestCase):
    def setUp(self):
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

        self.data = {
            'token': self.user.password_reset_token,
            'password': 'newpassword'
        }

    def test_serializer_empty_object(self):
        """
        Tests that serializer.object returns expected data when empty.
        """
        serializer = ResetPasswordSerializer()

        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {})

    def test_serializer_should_return_expected_data_if_valid(self):
        """
        Tests that serializer.object should return expected data when valid.
        """
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_data = {
            'password_reset': True
        }

        self.assertEqual(serializer.object, expected_data)

    def test_serializer_should_return_expected_error_if_invalid(self):
        """
        Tests that serializer.errors should return expected
        error when invalid.
        """
        self.data['password'] = None
        self.data['token'] = None
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'password': ['This field is required.'],
            'token': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_error)
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {})

    def test_serializer_should_return_expected_error_invalid_token(self):
        """
        Tests that serializer.errors should return expected
        error for invalid token.
        """
        self.data['token'] = 'invalidtoken'
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'token': ['Invalid password reset token.']
        }

        self.assertEqual(serializer.errors, expected_error)
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {})

    def test_serializer_validate_should_set_user_password(self):
        """
        Tests that serializer.validate() should set new password.
        """
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        user = User.objects.get(username=self.username)

        self.assertTrue(user.check_password(self.data['password']))

    def test_serializer_should_validate_password_requirements(self):
        """
        Tests that serializer validates password field.
        """
        self.data['password'] = 'a.'
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'password': [
                'Ensure this value has at least 6 characters (it has 2).'
            ]
        }

        self.assertEqual(serializer.errors, expected_error)
