from django.test import TestCase
from django.conf import settings

from rest_framework.test import APIClient

from ...users.models import User
from ...accounts.models import Account, AccountCollaborator
from ...boards.models import Board, BoardCollaborator
from ...cards.models import Card
from ...comments.models import Comment


class BaseTestCase(TestCase):
    users = {}

    def create_user(self):
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

        self.users[self.username] = self.user

    def create_another_user(self, username='jsmith'):
        password = 'abc123'
        email = '{}@example.com'.format(username)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=username[:1].upper(),
            last_name=username[1:].upper()
        )

        self.users[username] = user

        return user

    def create_account(self):
        self.account = Account.personals.create(
            name='Acme', created_by=self.user)

        self.account_owner = AccountCollaborator.objects.create_owner(
            account=self.account, user=self.user)

    def create_another_account(self, name='Example.com', user=None):
        if not user and self.user:
            user = self.user

        account = Account.personals.create(
            name=name, created_by=user)

        account_owner = AccountCollaborator.objects.create_owner(
            account=account, user=user)

        return account, account_owner

    def create_board(self):
        self.board = Board.objects.create(
            name='The Board', account=self.account, created_by=self.user)

        settings.BOARDS_DEMO_BOARD_ID = self.board.id

        self.board_collaborator = BoardCollaborator.objects.get(
            user=self.user, board=self.board)

    def create_card(self):
        self.card = Card.objects.create(
            name='The Card', type='note', content='abc123',
            board=self.board, created_by=self.user)

    def create_anoter_card(self, name, board=None, created_by=None):
        if not board and self.board:
            board = self.board

        if not created_by and self.user:
            created_by = self.user

        return Card.objects.create(
            name=name, type='note', content='abc123',
            board=board, created_by=created_by)

    def create_comment(self):
        self.comment = Comment.objects.create(
            content='A comment',
            content_object=self.card,
            created_by=self.user
        )

    def create_another_comment(self, content, obj=None, created_by=None):
        if not obj:
            obj = self.card

        if not created_by:
            created_by = self.user

        return Comment.objects.create(
            content=content,
            content_object=obj,
            created_by=created_by
        )


class AuthenticatedAPITestCase(BaseTestCase):
    """
    This test case class creates a basic user
    and does authentication for you using a JWT token
    """

    def setUp(self):
        self.create_user()

        self.token = self.user.token

        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
