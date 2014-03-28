from django.core.exceptions import ValidationError

from ...utils.tests import BaseTestCase
from ...users.models import User
from ...invitations.models import InvitedUser
from ..models import Board, BoardCollaborator, BoardCollaboratorRequest


class BoardTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(Board._meta.fields), 12)

    def test_is_user_collaborator_should_return_true_if_exists(self):
        """
        Tests that `.is_user_collaborator` returns `True` if
        a BoardCollaborator for given user exists.
        """
        is_user_collaborator = self.board.is_user_collaborator(self.user)

        self.assertTrue(is_user_collaborator)

    def test_is_user_collaborator_should_return_false(self):
        """
        Tests that `.is_user_collaborator` returns `False` if
        a BoardCollaborator for given user does not exists.
        """
        user = User.objects.create_user(
            username='jbennett',
            email='jbennett@example.com',
            password=self.password,
            first_name='John',
            last_name='Bennet'
        )

        is_user_collaborator = self.board.is_user_collaborator(user)

        self.assertFalse(is_user_collaborator)

    def test_is_user_collaborator_should_optianlly_check_perm(self):
        """
        Tests that `is_user_collaborator` checks if a BoardCollaborator
        exists for a given user and permission.
        """
        is_user_collaborator = self.board.is_user_collaborator(
            self.user, permission='write')

        self.assertTrue(is_user_collaborator)

    def test_creating_board_creates_owner_collaborator(self):
        """
        Tests that a post_save signal creates a BoardCollaborator
        for account owner.
        """
        collaborators = BoardCollaborator.objects.filter(
            board=self.board, user=self.user, permission='write')

        self.assertEqual(collaborators.count(), 1)


class BoardCollaboratorTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(BoardCollaborator._meta.fields), 7)

    def test_user_or_invited_user_must_be_set_before_creating(self):
        """
        Tests that ValidationError is raised when no
        user or invited_user is set.
        """
        with self.assertRaises(ValidationError):
            BoardCollaborator.objects.create(
                board=self.board
            )

    def test_setting_user_and_invited_user_should_raise_error(self):
        """
        Tests that ValidationError is raised when a
        user and invited_user are set together.
        """
        invited_user = InvitedUser.objects.create(
            email='invited@example.com',
            account=self.account,
            created_by=self.user
        )

        user = User.objects.create_user(
            username='jbennett',
            email='jbennett@example.com',
            password=self.password,
            first_name='John',
            last_name='Bennet'
        )

        with self.assertRaises(ValidationError):
            BoardCollaborator.objects.create(
                board=self.board,
                user=user,
                invited_user=invited_user
            )


class BoardCollaboratorRequestTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(BoardCollaboratorRequest._meta.fields), 9)

    def test_create_request_for_user_not_signed_up(self):
        """
        Tests that creating a request for an email address
        of a user that hasn't signed up yet returns None
        when accessing the user field.
        """
        request = BoardCollaboratorRequest.objects.create(
            first_name='Juan',
            last_name='Pueblo',
            email='jpueblocollaborator@example.com',
            board=self.board,
            message='Let me in!'
        )

        self.assertEqual(request.user, None)

    def test_create_request_for_user_not_signed_in(self):
        """
        Tests that creating a request for an email address
        of a user that has signed up returns the expected user
        when accessing the user field.
        """
        request = BoardCollaboratorRequest.objects.create(
            first_name='Juan',
            last_name='Pueblo',
            email=self.email,
            board=self.board,
            message='Let me in!'
        )

        self.assertEqual(request.user, self.user)

    def test_create_request_for_user_signed_in(self):
        """
        Tests that creating a request using a user object
        sets the first_name, last_name, and email fields.
        """
        request = BoardCollaboratorRequest.objects.create(
            user=self.user,
            board=self.board,
            message='Let me in!'
        )

        self.assertEqual(request.email, self.email)

    def test_user_or_email_must_be_set_before_creating(self):
        """
        Tests that ValidationError is raised when no
        user or email is set.
        """
        with self.assertRaises(ValidationError):
            BoardCollaboratorRequest.objects.create(
                board=self.board,
                message='Let me in!'
            )

    def test_accept_should_create_invited_user(self):
        """
        Tests that accept() creates an InvitedUser.
        """
        request = BoardCollaboratorRequest.objects.create(
            first_name='Juan',
            last_name='Pueblo',
            email='jpueblocollaborator@example.com',
            board=self.board,
            message='Let me in!'
        )

        request.accept()

        invited_users = InvitedUser.objects.filter(
            email=request.email, account=self.account)

        self.assertEqual(invited_users.count(), 1)

    def test_accept_should_create_board_collaborator(self):
        """
        Tests that accept() creates BoardCollaborator for
        the invited user.
        """
        request = BoardCollaboratorRequest.objects.create(
            first_name='Juan',
            last_name='Pueblo',
            email='jpueblocollaborator@example.com',
            board=self.board,
            message='Let me in!'
        )

        request.accept()

        invited_user = InvitedUser.objects.get(
            email=request.email, account=self.account)

        board_collaborators = BoardCollaborator.objects.filter(
            invited_user=invited_user, board=self.board)

        self.assertEqual(board_collaborators.count(), 1)

    def test_accept_should_add_board_collaborator_to_invited_user(self):
        """
        Tests that accept() adds created board collaborator
        to invited user.
        """
        request = BoardCollaboratorRequest.objects.create(
            first_name='Juan',
            last_name='Pueblo',
            email='jpueblocollaborator@example.com',
            board=self.board,
            message='Let me in!'
        )

        request.accept()

        invited_user = InvitedUser.objects.get(
            email=request.email, account=self.account)

        board_collaborators = invited_user.board_collaborators.all()

        self.assertEqual(board_collaborators.count(), 1)

    def test_accept_should_delete_request(self):
        """
        Tests that accept() deletes the BoardCollaboratorRequest.
        """
        request = BoardCollaboratorRequest.objects.create(
            first_name='Juan',
            last_name='Pueblo',
            email='jpueblocollaborator@example.com',
            board=self.board,
            message='Let me in!'
        )

        request.accept()

        requests = BoardCollaboratorRequest.objects.all()

        self.assertEqual(requests.count(), 0)

    def test_reject_should_delete_request(self):
        """
        Tests that reject() deletes the BoardCollaboratorRequest.
        """
        request = BoardCollaboratorRequest.objects.create(
            first_name='Juan',
            last_name='Pueblo',
            email='jpueblocollaborator@example.com',
            board=self.board,
            message='Let me in!'
        )

        request.reject()

        requests = BoardCollaboratorRequest.objects.all()

        self.assertEqual(requests.count(), 0)
