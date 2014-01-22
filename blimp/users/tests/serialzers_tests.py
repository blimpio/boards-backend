from django.test import TestCase

from blimp.accounts.models import Account, AccountMember
from blimp.invitations.models import SignupRequest
from ..models import User
from ..serializers import ValidateUsernameSerializer, SignupSerializer


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
            'username': self.username
        }

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = ValidateUsernameSerializer()
        self.assertEqual(serializer.data, {})

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

    def test_serializer_object_should_have_exists_key(self):
        """
        Tests that serializer.object should be a dictionary
        with an exists key.
        """
        serializer = ValidateUsernameSerializer(data=self.data)
        serializer.is_valid()

        self.assertTrue('exists' in serializer.object)

    def test_serializer_should_return_true_if_user_exists(self):
        """
        Tests that serializer should return True if user exists.
        """
        serializer = ValidateUsernameSerializer(data=self.data)
        serializer.is_valid()

        self.assertTrue(serializer.object['exists'])

    def test_serializer_should_return_false_if_user_doesnt_exists(self):
        """
        Tests that serializer should return False if user doesn't exists.
        """
        self.data['username'] = 'nonexistent'
        serializer = ValidateUsernameSerializer(data=self.data)
        serializer.is_valid()

        self.assertFalse(serializer.object['exists'])


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

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data returns expected data when empty.
        """
        serializer = SignupSerializer()
        expected_data = {
            'email': '',
            'full_name': '',
            'account_name': '',
            'username': '',
            'allow_signup': False,
            'signup_domains': '',
            'invite_emails': ''
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_should_return_expected_data_if_valid(self):
        """
        Tests that serializer.data should return expected data when valid.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_data = {
            'email': 'juan@example.com',
            'full_name': 'Juan Pueblo',
            'first_name': 'Juan',
            'last_name': 'Pueblo',
            'account_name': 'Pueblo Co.',
            'username': 'juan',
            'allow_signup': False,
            'signup_domains': None,
            'invite_emails': None
        }

        self.assertEqual(serializer.data, expected_data)

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
        self.data.update({'allow_signup': True, 'signup_domains': 'gmail.com'})
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'signup_domains': ["You can't have gmail.com as a sign-up domain."]
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_return_error_invalid_invite_email(self):
        """
        Tests that serializer should return error if invite
        email is invalid.
        """
        self.data.update({
            'allow_signup': True,
            'signup_domains': 'example.com',
            'invite_emails': '@example.com',
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
        user = serializer.signup()
        expected_user = User.objects.get(username=self.data['username'])

        self.assertEqual(user, expected_user)

    def test_create_user_should_return_created_user(self):
        """
        Tests that serializer.create_user() should return the created user.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        user = serializer.create_user()
        expected_user = User.objects.get(username=self.data['username'])

        self.assertEqual(user, expected_user)

    def test_create_account_should_return_created_account_and_owner(self):
        """
        Tests that serializer.create_account() should return a tuple of
        the created account and created owner.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        user = serializer.create_user()
        account_tuple = serializer.create_account(user)
        expected_account = Account.objects.get(slug='pueblo-co')
        expected_owner = AccountMember.objects.get(
            account=expected_account, user=user, role='owner')

        expected_tuple = expected_account, expected_owner

        self.assertEqual(account_tuple, expected_tuple)

    def test_invite_users_should_return_invited_users(self):
        """
        Tests that serializer.invite_users should return a list of
        the invited users.
        """
        self.data.update({
            'allow_signup': True,
            'signup_domains': 'example.com',
            'invite_emails': 'ppueblo@example.com,qpueblo@example.com',
        })

        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        user = serializer.create_user()
        account, owner = serializer.create_account(user)
        invited_users = serializer.invite_users(account, user)

        self.assertEqual(len(invited_users), 2)
