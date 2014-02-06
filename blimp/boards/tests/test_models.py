from django.core.exceptions import ValidationError

from ...utils.tests import BaseTestCase
from ...accounts.models import Account, AccountCollaborator
from ...invitations.models import InvitedUser
from ..models import Board, BoardCollaborator, BoardCollaboratorRequest


class BoardCollaboratorRequestTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()

        self.account = Account.objects.create(name='Acme')
        self.account_collaborator = AccountCollaborator.objects.create_owner(
            account=self.account, user=self.user)

        self.board = Board.objects.create(
            name='The Board', account=self.account, created_by=self.user)

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
