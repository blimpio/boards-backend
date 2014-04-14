import jwt

from django.conf import settings

from ...utils.tests import BaseTestCase
from ...users.models import User
from ...accounts.models import Account, AccountCollaborator
from ...boards.models import Board, BoardCollaborator
from ..models import SignupRequest, InvitedUser


class SignupRequestTestCase(BaseTestCase):
    def setUp(self):
        self.signup_request = SignupRequest.objects.create(
            email='jpueblo@example.com')

    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(SignupRequest._meta.fields), 4)

    def test_token_property(self):
        """
        Tests that the token property returns the expected JWT token.
        """
        payload = jwt.decode(self.signup_request.token, settings.SECRET_KEY)
        expected_payload = {
            'type': 'SignupRequest',
            'id': 1
        }

        self.assertTrue(payload, expected_payload)

    def test_get_from_token(self):
        """
        Tests that the manager's get_from_token() returns an SignupRequest
        for a given token.
        """
        signup_request = SignupRequest.objects.get_from_token(
            self.signup_request.token)

        self.assertEqual(signup_request, self.signup_request)


class InvitedUserTestCase(BaseTestCase):
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

        self.account = Account.personals.create(name='Acme')
        self.account_collaborator = AccountCollaborator.objects.create(
            account=self.account, user=self.user, is_owner=True)

        self.user2 = User.objects.create_user(
            username='bburke',
            email='bburke@example.com',
            password=self.password,
            first_name='Bruce',
            last_name='Burke'
        )

        self.invited_user = InvitedUser.objects.create(
            user=self.user2, account=self.account, created_by=self.user)

    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(InvitedUser._meta.fields), 10)

    def test_save_should_set_additional_user_data_if_available(self):
        """
        Tests that save() adds any user data in other fields.
        """
        self.assertEqual(self.invited_user.first_name, self.user2.first_name)

    def test_should_find_existing_user_with_given_email(self):
        """
        Tests that save() finds an existing user with a given email address
        sets the user field and adds any user data in other fields.
        """

        invited_user = InvitedUser.objects.create(
            email=self.user.email, account=self.account, created_by=self.user)

        self.assertEqual(invited_user.first_name, self.user.first_name)

    def test_get_email_should_return_email(self):
        """
        Tests that get_email() returns the user's email.
        """
        self.assertEqual(self.invited_user.get_email(), self.user2.email)

    def test_get_full_name_should_concatenate_names(self):
        """
        Tests that get_full_name returns the user's first name
        plus the last name, with a space in between.
        """
        full_name = u'{} {}'.format(self.user2.first_name, self.user2.last_name)

        self.assertEqual(self.invited_user.get_full_name(), full_name)

    def test_token_property(self):
        """
        Tests that the token property returns the expected JWT token.
        """

        payload = jwt.decode(self.invited_user.token, settings.SECRET_KEY)
        expected_payload = {
            'type': 'InvitedUser',
            'id': 1
        }

        self.assertTrue(payload, expected_payload)

    def test_get_gravatar_url_should_return_user_gravatar_url(self):
        """
        Tests that gravatar_url returns the user's gravatar URL.
        """
        expected_url = ('https://secure.gravatar.com/'
                        'avatar/be7fb46dbd6620092dcc039fef94da52')

        self.assertEqual(self.invited_user.gravatar_url, expected_url)

    def test_accept_invitation_should_create_account_collaborator(self):
        """
        Tests that accepting invitation creates AccountCollaborator.
        """
        self.invited_user.accept(self.user2)

        collaborator = AccountCollaborator.objects.filter(user=self.user2)

        self.assertEqual(collaborator.count(), 1)

    def test_accept_invitation_should_delete_invited_user(self):
        """
        Tests that accepting invitation deletes invited user.
        """
        self.invited_user.accept(self.user2)

        invited_users = InvitedUser.objects.all()

        self.assertEqual(invited_users.count(), 0)

    def test_accept_invitation_should_set_board_collaborators_user(self):
        board = Board.objects.create(
            name='Example Board',
            created_by=self.user,
            account=self.account
        )

        board_collaborator = BoardCollaborator.objects.create(
            invited_user=self.invited_user,
            board=board,
            permission='read'
        )

        self.invited_user.board_collaborator = board_collaborator

        self.invited_user.accept(self.user2)

        board_collaborator = BoardCollaborator.objects.filter(user=self.user)

        self.assertTrue(board_collaborator.exists())
