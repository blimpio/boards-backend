from rest_framework import status
from rest_framework.test import APIClient

from ...utils.tests import AuthenticatedAPITestCase
from ...boards.models import Board
from ...comments.models import Comment
from ..serializers import CardUserSerializer
from ..models import Card


class CardViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(CardViewSetTestCase, self).setUp()

        self.create_account()
        self.create_board()
        self.create_card()

        self.base_url = '/api/v1/cards/'

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

        created_by = CardUserSerializer.to_native(self.card.created_by)
        modified_by = CardUserSerializer.to_native(self.card.modified_by)

        expected_response = [{
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.card.id,
            'position': self.card.position,
            'date_created': self.card.date_created,
            'date_modified': self.card.date_modified,
            'name': self.card.name,
            'type': self.card.type,
            'slug': self.card.slug,
            'board': self.card.board_id,
            'cards': [],
            'stack': None,
            'featured': False,
            'origin_url': self.card.origin_url,
            'content': self.card.content,
            'is_shared': False,
            'thumbnail_xs_path': self.card.thumbnail_xs_path,
            'thumbnail_sm_path': self.card.thumbnail_sm_path,
            'thumbnail_md_path': self.card.thumbnail_md_path,
            'thumbnail_lg_path': self.card.thumbnail_lg_path,
            'file_size': None,
            'mime_type': self.card.mime_type,
            'html_url': self.card.html_url,
            'download_html_url': self.card.download_html_url,
            'original_html_url': self.card.original_html_url,
            'metadata': self.card.metadata,
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
        self.account_owner.delete()
        self.board_collaborator.permission = 'read'
        self.board_collaborator.save()

        data = {
            'name': 'New Board Name',
            'account': self.account.id,
            'board': self.board.id,
            'type': 'note',
            'content': 'abc123'
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

        created_by = CardUserSerializer.to_native(self.card.created_by)
        modified_by = CardUserSerializer.to_native(self.card.modified_by)

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.card.id,
            'position': self.card.position,
            'date_created': self.card.date_created,
            'date_modified': self.card.date_modified,
            'name': self.card.name,
            'slug': self.card.slug,
            'type': self.card.type,
            'board': self.card.board_id,
            'cards': [],
            'stack': None,
            'featured': False,
            'origin_url': self.card.origin_url,
            'content': self.card.content,
            'is_shared': False,
            'thumbnail_xs_path': self.card.thumbnail_xs_path,
            'thumbnail_sm_path': self.card.thumbnail_sm_path,
            'thumbnail_md_path': self.card.thumbnail_md_path,
            'thumbnail_lg_path': self.card.thumbnail_lg_path,
            'file_size': None,
            'mime_type': self.card.mime_type,
            'html_url': self.card.html_url,
            'download_html_url': self.card.download_html_url,
            'original_html_url': self.card.original_html_url,
            'metadata': self.card.metadata,
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
        self.data['metadata'] = {
            'pattern': {
                'shape': '01',
                'color': '#000'
            }
        }

        response = self.client.post(self.base_url, self.data, format='json')

        card = Card.objects.get(pk=response.data['id'])
        created_by = CardUserSerializer.to_native(card.created_by)
        modified_by = CardUserSerializer.to_native(card.modified_by)

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': card.id,
            'position': card.position,
            'date_created': card.date_created,
            'date_modified': card.date_modified,
            'name': card.name,
            'slug': 'my-card',
            'type': card.type,
            'board': card.board_id,
            'cards': [],
            'stack': None,
            'featured': False,
            'origin_url': card.origin_url,
            'content': card.content,
            'is_shared': False,
            'thumbnail_xs_path': card.thumbnail_xs_path,
            'thumbnail_sm_path': card.thumbnail_sm_path,
            'thumbnail_md_path': card.thumbnail_md_path,
            'thumbnail_lg_path': card.thumbnail_lg_path,
            'file_size': None,
            'mime_type': card.mime_type,
            'html_url': card.html_url,
            'download_html_url': card.download_html_url,
            'original_html_url': card.original_html_url,
            'metadata': self.data['metadata'],
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
        created_by = CardUserSerializer.to_native(card.created_by)
        modified_by = CardUserSerializer.to_native(card.modified_by)

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': card.id,
            'date_created': card.date_created,
            'date_modified': card.date_modified,
            'name': self.data['name'],
            'position': card.position,
            'slug': card.slug,
            'type': card.type,
            'board': card.board_id,
            'cards': [],
            'stack': None,
            'featured': False,
            'origin_url': card.origin_url,
            'content': card.content,
            'is_shared': False,
            'thumbnail_xs_path': card.thumbnail_xs_path,
            'thumbnail_sm_path': card.thumbnail_sm_path,
            'thumbnail_md_path': card.thumbnail_md_path,
            'thumbnail_lg_path': card.thumbnail_lg_path,
            'file_size': None,
            'mime_type': card.mime_type,
            'html_url': card.html_url,
            'download_html_url': card.download_html_url,
            'original_html_url': card.original_html_url,
            'metadata': card.metadata,
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
        created_by = CardUserSerializer.to_native(card.created_by)
        modified_by = CardUserSerializer.to_native(card.modified_by)

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': card.id,
            'date_created': card.date_created,
            'date_modified': card.date_modified,
            'name': self.data['name'],
            'position': card.position,
            'slug': card.slug,
            'type': card.type,
            'board': card.board_id,
            'cards': [],
            'stack': None,
            'featured': False,
            'origin_url': card.origin_url,
            'content': self.data['content'],
            'is_shared': False,
            'thumbnail_xs_path': card.thumbnail_xs_path,
            'thumbnail_sm_path': card.thumbnail_sm_path,
            'thumbnail_md_path': card.thumbnail_md_path,
            'thumbnail_lg_path': card.thumbnail_lg_path,
            'file_size': None,
            'mime_type': card.mime_type,
            'html_url': card.html_url,
            'download_html_url': card.download_html_url,
            'original_html_url': card.original_html_url,
            'metadata': card.metadata,
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

        response = self.client.get(self.base_url, {'board': self.board.id})

        created_by = CardUserSerializer.to_native(self.card.created_by)
        modified_by = CardUserSerializer.to_native(self.card.modified_by)

        expected_response = [{
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.card.id,
            'position': self.card.position,
            'date_created': self.card.date_created,
            'date_modified': self.card.date_modified,
            'name': self.card.name,
            'slug': self.card.slug,
            'type': self.card.type,
            'board': self.card.board_id,
            'cards': [],
            'stack': None,
            'featured': False,
            'origin_url': self.card.origin_url,
            'content': self.card.content,
            'is_shared': False,
            'thumbnail_xs_path': self.card.thumbnail_xs_path,
            'thumbnail_sm_path': self.card.thumbnail_sm_path,
            'thumbnail_md_path': self.card.thumbnail_md_path,
            'thumbnail_lg_path': self.card.thumbnail_lg_path,
            'file_size': None,
            'mime_type': self.card.mime_type,
            'html_url': self.card.html_url,
            'download_html_url': self.card.download_html_url,
            'original_html_url': self.card.original_html_url,
            'metadata': self.card.metadata,
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_comments_action_get(self):
        """
        Tests that viewset allows retrieving comments for specific card.
        """
        comment = Comment.objects.create(
            content='A comment',
            content_object=self.card,
            created_by=self.user
        )

        response = self.client.get(
            '{}{}/comments/'.format(self.base_url, self.card.id))

        expected_response = [{
            'id': comment.id,
            'content': 'A comment',
            'created_by': self.user.id,
            'modified_by': self.user.id,
            'date_created': comment.date_created,
            'date_modified': comment.date_modified
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_comments_action_post(self):
        data = {
            'content': 'This is my comment.'
        }

        response = self.client.post(
            '{}{}/comments/'.format(self.base_url, self.card.id), data)

        comment = Comment.objects.get(pk=response.data['id'])

        expected_response = {
            'id': comment.id,
            'content': 'This is my comment.',
            'created_by': self.user.id,
            'modified_by': self.user.id,
            'date_created': comment.date_created,
            'date_modified': comment.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_viewset_comments_action_post_read_permission(self):
        data = {
            'content': 'This is my comment.'
        }

        self.board_collaborator.permission = 'read'
        self.board_collaborator.save()

        response = self.client.post(
            '{}{}/comments/'.format(self.base_url, self.card.id), data)

        comment = Comment.objects.get(pk=response.data['id'])

        expected_response = {
            'id': comment.id,
            'content': 'This is my comment.',
            'created_by': self.user.id,
            'modified_by': self.user.id,
            'date_created': comment.date_created,
            'date_modified': comment.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_allow_anonymous_user_to_list_cards(self):
        """
        Tests that viewset should allow anonymous users to list cards
        with board query parameter, and board is shared.
        """
        self.board.is_shared = True
        self.board.save()

        self.client = APIClient()
        response = self.client.get(self.base_url, {'board': self.board.id})

        created_by = CardUserSerializer.to_native(self.card.created_by)
        modified_by = CardUserSerializer.to_native(self.card.modified_by)

        expected_response = [{
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.card.id,
            'position': self.card.position,
            'date_created': self.card.date_created,
            'date_modified': self.card.date_modified,
            'name': self.card.name,
            'slug': self.card.slug,
            'type': self.card.type,
            'board': self.card.board_id,
            'cards': [],
            'stack': None,
            'featured': False,
            'origin_url': self.card.origin_url,
            'content': self.card.content,
            'is_shared': False,
            'thumbnail_xs_path': self.card.thumbnail_xs_path,
            'thumbnail_sm_path': self.card.thumbnail_sm_path,
            'thumbnail_md_path': self.card.thumbnail_md_path,
            'thumbnail_lg_path': self.card.thumbnail_lg_path,
            'file_size': None,
            'mime_type': self.card.mime_type,
            'html_url': self.card.html_url,
            'download_html_url': self.card.download_html_url,
            'original_html_url': self.card.original_html_url,
            'metadata': self.card.metadata,
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_create_stack(self):
        """
        Tests that POST to viewset creates a stack.
        """
        self.data = {
            'name': 'My Stack',
            'type': 'stack',
            'board': self.board.id,
            'content': 'My content',
            'cards': [self.card.id]
        }

        response = self.client.post(self.base_url, self.data, format='json')

        card = Card.objects.get(pk=response.data['id'])

        created_by = CardUserSerializer.to_native(self.card.created_by)
        modified_by = CardUserSerializer.to_native(self.card.modified_by)

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': card.id,
            'position': card.position,
            'date_created': card.date_created,
            'date_modified': card.date_modified,
            'name': card.name,
            'slug': card.slug,
            'type': card.type,
            'board': card.board_id,
            'cards': [self.card.id],
            'featured': False,
            'is_shared': False,
            'html_url': card.html_url
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_viewset_unstack(self):
        """
        Tests that PUT to unstack, removes stack card
        and updates cards.
        """
        self.data = {
            'name': 'My Stack',
            'type': 'stack',
            'board': self.board,
            'created_by': self.user
        }

        stack = Card.objects.create(**self.data)

        stack.cards.add(self.card)

        response = self.client.put(
            '{}{}/unstack/'.format(self.base_url, stack.id))

        card = Card.objects.get(pk=self.card.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

        self.assertEqual(list(stack.cards.all()), [])
        self.assertEqual(card.stack, None)

    def test_viewset_unstack_card_should_return_error(self):
        """
        Tests that PUT to unstack should only work on stack cards.
        """
        response = self.client.put(
            '{}{}/unstack/'.format(self.base_url, self.card.id))

        expected_response = {'error': 'Malformed request.', 'status_code': 400}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)
