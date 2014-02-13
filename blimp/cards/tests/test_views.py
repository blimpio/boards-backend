from rest_framework import status
from rest_framework.test import APIClient

from ...utils.tests import AuthenticatedAPITestCase
from ...boards.models import Board
from ..models import Card


class CardViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(CardViewSetTestCase, self).setUp()

        self.create_account()
        self.create_board()
        self.create_card()

        self.base_url = '/api/cards/'

        self.data = {
            'name': 'My Card',
            'type': 'note',
            'board': self.board.id,
            'content': 'My content'
        }

    def test_viewset_should_require_authentication(self):
        """
        Tests that viewset requires authentication.
        """
        self.client = APIClient()
        response = self.client.get(self.base_url)

        expected_response = {
            'error': 'Authentication credentials were not provided.',
            'status_code': 401
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_return_cards_user_can_access(self):
        """
        Tests that viewset returns cards that the user can access.
        """
        response = self.client.get(self.base_url)
        expected_response = [{
            'created_by': self.card.created_by_id,
            'id': self.card.id,
            'date_created': self.card.date_created,
            'date_modified': self.card.date_modified,
            'name': self.card.name,
            'type': self.card.type,
            'board': self.card.board_id,
            'cards': [],
            'featured': False,
            'origin_url': '',
            'content': self.card.content,
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': '',
            'file_size': None,
            'file_extension': ''
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_shouldnt_return_cards_to_user_with_no_access(self):
        """
        Tests that viewset doesn't returns cards that the user can't access.
        """
        self.board_collaborator.delete()

        response = self.client.get(self.base_url)
        expected_response = []

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_check_permissions(self):
        """
        Tests that viewset checks for custom permissions.
        """
        self.board_collaborator.permission = 'read'
        self.board_collaborator.save()

        data = {
            'name': 'New Board Name',
            'account': self.account.id
        }

        response = self.client.put(
            '{}{}/'.format(self.base_url, self.board.id), data, format='json')

        expected_response = {
            'status_code': 403,
            'error': 'You do not have permission to perform this action.'
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_retrieve_card(self):
        """
        Tests that viewset allows retrieving specific card.
        """
        response = self.client.get(
            '{}{}/'.format(self.base_url, self.card.id))

        expected_response = {
            'created_by': self.card.created_by_id,
            'id': self.card.id,
            'date_created': self.card.date_created,
            'date_modified': self.card.date_modified,
            'name': self.card.name,
            'type': self.card.type,
            'board': self.card.board_id,
            'cards': [],
            'featured': False,
            'origin_url': '',
            'content': self.card.content,
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': '',
            'file_size': None,
            'file_extension': ''
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_shouldnt_retrieve_card_unallowed_board(self):
        """
        Tests that viewset doesn't return card that are unallowed to user.
        """
        self.board_collaborator.delete()

        response = self.client.get(
            '{}{}/'.format(self.base_url, self.card.id))

        expected_response = {
            'status_code': 404,
            'error': 'Not found'
        }

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_create_card(self):
        """
        Tests that POST to viewset creates a card.
        """
        response = self.client.post(self.base_url, self.data, format='json')

        card = Card.objects.get(pk=response.data['id'])

        expected_response = {
            'created_by': card.created_by_id,
            'id': card.id,
            'date_created': card.date_created,
            'date_modified': card.date_modified,
            'name': card.name,
            'type': card.type,
            'board': card.board_id,
            'cards': [],
            'featured': False,
            'origin_url': '',
            'content': card.content,
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': '',
            'file_size': None,
            'file_extension': ''
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_update_card(self):
        """
        Tests that PUT to viewset should update card.
        """

        self.data['name'] = 'New Card Name'

        response = self.client.put(
            '{}{}/'.format(self.base_url, self.card.id),
            self.data, format='json')

        card = Card.objects.get(pk=response.data['id'])

        expected_response = {
            'created_by': card.created_by_id,
            'id': card.id,
            'date_created': card.date_created,
            'date_modified': card.date_modified,
            'name': self.data['name'],
            'type': card.type,
            'board': card.board_id,
            'cards': [],
            'featured': False,
            'origin_url': '',
            'content': card.content,
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': '',
            'file_size': None,
            'file_extension': ''
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_delete_card(self):
        """
        Tests that DELETE to viewset deletes specified card.
        """
        response = self.client.delete(
            '{}{}/'.format(self.base_url, self.card.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_viewset_should_partially_update_board(self):
        """
        Tests that PATCH to viewset partially updates the card.
        """
        self.data['content'] = 'updated content...'

        response = self.client.patch(
            '{}{}/'.format(self.base_url, self.card.id),
            self.data, format='json')

        card = Card.objects.get(pk=response.data['id'])

        expected_response = {
            'created_by': card.created_by_id,
            'id': card.id,
            'date_created': card.date_created,
            'date_modified': card.date_modified,
            'name': self.data['name'],
            'type': card.type,
            'board': card.board_id,
            'cards': [],
            'featured': False,
            'origin_url': '',
            'content': self.data['content'],
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': '',
            'file_size': None,
            'file_extension': ''
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_allow_filtering_by_board(self):
        """
        Tests that viewset returns board collaborators of
        boards that the user can access.
        """
        board = Board.objects.create(
            name='Another Board', account=self.account, created_by=self.user)

        Card.objects.create(
            name='Another Card', type='note', content='abc123',
            board=board, created_by=self.user)

        response = self.client.get('{}?board=1'.format(self.base_url))

        expected_response = [{
            'created_by': self.card.created_by_id,
            'id': self.card.id,
            'date_created': self.card.date_created,
            'date_modified': self.card.date_modified,
            'name': self.card.name,
            'type': self.card.type,
            'board': self.card.board_id,
            'cards': [],
            'featured': False,
            'origin_url': '',
            'content': self.card.content,
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': '',
            'file_size': None,
            'file_extension': ''
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
