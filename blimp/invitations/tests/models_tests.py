from django.test import TestCase

from blimp.users.models import User
from blimp.accounts.models import Account
from ..models import SignupRequest, InvitedUser


class SignupRequestTestCase(TestCase):
    def setUp(self):
        self.signup_request = SignupRequest.objects.create(
            email='jpueblo@example.com')

        self.token = ('eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.'
                      'eyJ0eXBlIjogIlNpZ251cFJlcXVlc3QiLCAiaWQiOiAxfQ.'
                      'IeyWuyJBKOK93iGSybajLMU3PyYAya9q_UCCZCS_rDI')

    def test_token_property(self):
        """
        Tests that the token property returns the expected JWT token.
        """
        self.assertTrue(self.signup_request.token, self.token)

    def test_get_from_token(self):
        """
        Tests that the manager's get_from_token() returns an SignupRequest
        for a given token.
        """
        signup_request = SignupRequest.objects.get_from_token(self.token)
        self.assertEqual(signup_request, self.signup_request)


class InvitedUserTestCase(TestCase):
    def setUp(self):
        self.username = 'jpueblo'
        self.password = 'abc123'

        self.user = User.objects.create_user(
            username=self.username,
            email='jpueblo@example.com',
            password=self.password,
            first_name='Juan',
            last_name='Pueblo'
        )

        self.account = Account.objects.create(name='Acme')

        self.invited_user = InvitedUser.objects.create(
            user=self.user, account=self.account, created_by=self.user)

        self.token = ('eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.'
                      'eyJ0eXBlIjogIkludml0ZWRVc2VyIiwgImlkIjogMX0._VT6-'
                      'fWVseLemG99pbcftEr4uVNxv7iivOO_FLvYFcg')

    def test_save_should_set_additional_user_data_if_available(self):
        """
        Tests that save() adds any user data in other fields.
        """
        self.assertEqual(self.invited_user.first_name, self.user.first_name)

    def test_get_email_should_return_email(self):
        """
        Tests that get_email() returns the user's email.
        """
        self.assertEqual(self.invited_user.get_email(), self.user.email)

    def test_get_full_name_should_concatenate_names(self):
        """
        Tests that get_full_name returns the user's first name
        plus the last name, with a space in between.
        """
        full_name = u'{} {}'.format(self.user.first_name, self.user.last_name)

        self.assertEqual(self.invited_user.get_full_name(), full_name)

    def test_token_property(self):
        """
        Tests that the token property returns the expected JWT token.
        """
        self.assertEqual(self.invited_user.token, self.token)

    def test_get_gravatar_url_should_return_user_gravatar_url(self):
        """
        Tests that get_gravatar_url() returns the user's gravatar URL.
        """
        expected_url = ('https://secure.gravatar.com/'
                        'avatar/8964266c2b9182617beb65e50fc00031?d=retro')

        self.assertEqual(self.invited_user.get_gravatar_url(), expected_url)

    def test_get_invite_url_should_returl_absolute_invite_url(self):
        """
        TODO: Write test when method is implemented.
        """
        pass

    def test_accept_should_accept_invitation(self):
        """
        TODO: Write test when method is implemented.
        """
        pass

    def test_notify_pending_invitations_class_method(self):
        """
        TODO: Write test when method is implemented.
        """
        pass
