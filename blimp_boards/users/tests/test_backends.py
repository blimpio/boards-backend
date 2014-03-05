from ...utils.tests import BaseTestCase
from ..models import User
from ..backends import EmailBackend


class EmailBackendTestCase(BaseTestCase):
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

        self.authenticate_kwargs = {
            'username': self.username,
            'password': self.password
        }

        self.backend = EmailBackend()

    def test_authenticate_should_return_user_if_valid(self):
        """
        Tests that authenticate() should return user if valid data.
        """
        authenticate = self.backend.authenticate(**self.authenticate_kwargs)

        self.assertEqual(authenticate, self.user)

    def test_authenticate_should_return_none_if_invalid(self):
        """
        Tests that authenticate() should return None if invalid data.
        """
        self.authenticate_kwargs['username'] = 'wrongusername'
        authenticate = self.backend.authenticate(**self.authenticate_kwargs)

        self.assertEqual(authenticate, None)

    def test_authenticate_should_return_user_when_using_email(self):
        """
        Tests that authenticate() should return user with email for username.
        """
        self.authenticate_kwargs['username'] = self.email
        authenticate = self.backend.authenticate(**self.authenticate_kwargs)

        self.assertEqual(authenticate, self.user)

    def test_authenticate_should_return_none_for_incorrect_password(self):
        """
        Tests that authenticate() returns None for invalid password.
        """
        self.authenticate_kwargs['password'] = 'wrongpassword'
        authenticate = self.backend.authenticate(**self.authenticate_kwargs)

        self.assertEqual(authenticate, None)

    def test_get_user_returns_user_for_valid_user_id(self):
        """
        Tests that get_user() returns user for valid user id.
        """
        user = self.backend.get_user(self.user.pk)

        self.assertEqual(user, self.user)

    def test_get_user_returns_none_for_invalid_user_id(self):
        """
        Tests that get_user() returns None for invalid user id.
        """
        user = self.backend.get_user(1000)

        self.assertEqual(user, None)
