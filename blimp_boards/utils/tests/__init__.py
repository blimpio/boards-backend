from django.test import TestCase
from rest_framework.test import APIClient

from ...users.models import User
from ...accounts.models import Account, AccountCollaborator
from ...boards.models import Board, BoardCollaborator
from ...cards.models import Card
from ..jwt_handlers import jwt_payload_handler, jwt_encode_handler


class BaseTestCase(TestCase):
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

    def create_account(self):
        self.account = Account.objects.create(name='Acme')
        self.account_owner = AccountCollaborator.objects.create_owner(
            account=self.account, user=self.user)

    def create_board(self):
        self.board = Board.objects.create(
            name='The Board', account=self.account, created_by=self.user)

        self.board_collaborator = BoardCollaborator.objects.get(
            user=self.user, board=self.board)

    def create_card(self):
        self.card = Card.objects.create(
            name='The Card', type='note', content='abc123',
            board=self.board, created_by=self.user)


class AuthenticatedAPITestCase(BaseTestCase):
    """
    This test case class creates a basic user
    and does authentication for you using a JWT token
    """
    def setUp(self):
        self.create_user()

        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
