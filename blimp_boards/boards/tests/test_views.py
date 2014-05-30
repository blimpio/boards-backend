from rest_framework import status
from rest_framework.test import APIClient

from ...utils.tests import AuthenticatedAPITestCase
from ...invitations.models import InvitedUser
from ...users.serializers import NestedUserSerializer
from ..models import Board, BoardCollaborator, BoardCollaboratorRequest


class BoardViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(BoardViewSetTestCase, self).setUp()

        self.create_account()
        self.create_board()

        self.base_url = '/api/v1/boards/'

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

    def test_viewset_should_return_boards_user_can_access(self):
        """
        Tests that viewset returns boards that the user can access.
        """
        response = self.client.get(self.base_url)
        created_by = NestedUserSerializer(self.board.created_by).data
        modified_by = NestedUserSerializer(self.board.modified_by).data

        expected_response = [{
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.board.id,
            'date_created': self.board.date_created,
            'date_modified': self.board.date_modified,
            'name': 'The Board',
            'slug': 'the-board',
            'account': self.board.account_id,
            'is_shared': False,
            'thumbnail_xs_path': self.board.thumbnail_xs_path,
            'thumbnail_sm_path': self.board.thumbnail_sm_path,
            'thumbnail_md_path': self.board.thumbnail_md_path,
            'thumbnail_lg_path': self.board.thumbnail_lg_path,
            'html_url': self.board.html_url,
            'activity_html_url': self.board.activity_html_url,
            'color': '',
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_shouldnt_return_boards_to_user_with_no_access(self):
        """
        Tests that viewset doesn't returns boards that the user can't access.
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

    def test_viewset_should_retrieve_board(self):
        """
        Tests that viewset allows retrieving specific boards.
        """
        response = self.client.get(
            '{}{}/'.format(self.base_url, self.board.id))

        created_by = NestedUserSerializer(self.board.created_by).data
        modified_by = NestedUserSerializer(self.board.modified_by).data

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.board.id,
            'date_created': self.board.date_created,
            'date_modified': self.board.date_modified,
            'name': 'The Board',
            'slug': 'the-board',
            'account': self.board.account_id,
            'is_shared': False,
            'thumbnail_xs_path': self.board.thumbnail_xs_path,
            'thumbnail_sm_path': self.board.thumbnail_sm_path,
            'thumbnail_md_path': self.board.thumbnail_md_path,
            'thumbnail_lg_path': self.board.thumbnail_lg_path,
            'html_url': self.board.html_url,
            'activity_html_url': self.board.activity_html_url,
            'color': '',
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_shouldnt_retrieve_board_unallowed_board(self):
        """
        Tests that viewset doesn't return boards that are unallowed to user.
        """
        board = Board.objects.create(
            name='Another Board', account=self.account, created_by=self.user)

        BoardCollaborator.objects.get(board=board, user=self.user).delete()

        response = self.client.get(
            '{}{}/'.format(self.base_url, board.id))

        expected_response = {
            'status_code': 404,
            'error': 'Not found'
        }

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_create_board(self):
        """
        Tests that POST to viewset creates a board.
        """
        data = {
            'name': 'New Board Name',
            'account': self.account.id,
            'color': 'red'
        }

        response = self.client.post(self.base_url, data, format='json')

        board = Board.objects.get(pk=response.data['id'])
        created_by = NestedUserSerializer(board.created_by).data
        modified_by = NestedUserSerializer(board.modified_by).data

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': board.id,
            'date_created': board.date_created,
            'date_modified': board.date_modified,
            'name': 'New Board Name',
            'slug': 'new-board-name',
            'account': board.account_id,
            'is_shared': False,
            'thumbnail_xs_path': self.board.thumbnail_xs_path,
            'thumbnail_sm_path': self.board.thumbnail_sm_path,
            'thumbnail_md_path': self.board.thumbnail_md_path,
            'thumbnail_lg_path': self.board.thumbnail_lg_path,
            'html_url': board.html_url,
            'activity_html_url': board.activity_html_url,
            'color': 'red',
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_update_board(self):
        """
        Tests that PUT to viewset should update board.
        """
        data = {
            'name': 'New Board Name',
            'slug': 'the-board',
            'account': self.account.id,
            'color': 'red',
        }

        response = self.client.put(
            '{}{}/'.format(self.base_url, self.board.id), data, format='json')

        self.board = Board.objects.get(pk=self.board.id)

        created_by = NestedUserSerializer(self.board.created_by).data
        modified_by = NestedUserSerializer(self.board.modified_by).data

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.board.id,
            'date_created': self.board.date_created,
            'date_modified': self.board.date_modified,
            'name': 'New Board Name',
            'slug': 'the-board',
            'account': self.board.account_id,
            'is_shared': False,
            'thumbnail_xs_path': self.board.thumbnail_xs_path,
            'thumbnail_sm_path': self.board.thumbnail_sm_path,
            'thumbnail_md_path': self.board.thumbnail_md_path,
            'thumbnail_lg_path': self.board.thumbnail_lg_path,
            'html_url': self.board.html_url,
            'activity_html_url': self.board.activity_html_url,
            'color': 'red',
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_delete_board(self):
        """
        Tests that DELETE to viewset deletes specified board.
        """
        response = self.client.delete(
            '{}{}/'.format(self.base_url, self.board.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_viewset_should_partially_update_board(self):
        """
        Tests that PATCH to viewset partially updates the board.
        """
        data = {
            'name': 'New Board Name',
            'slug': 'the-board',
            'account': self.account.id,
            'color': 'red'
        }

        response = self.client.patch(
            '{}{}/'.format(self.base_url, self.board.id), data, format='json')

        self.board = Board.objects.get(pk=self.board.id)
        created_by = NestedUserSerializer(self.board.created_by).data
        modified_by = NestedUserSerializer(self.board.modified_by).data

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.board.id,
            'date_created': self.board.date_created,
            'date_modified': self.board.date_modified,
            'name': 'New Board Name',
            'slug': 'the-board',
            'account': self.board.account_id,
            'is_shared': False,
            'thumbnail_xs_path': self.board.thumbnail_xs_path,
            'thumbnail_sm_path': self.board.thumbnail_sm_path,
            'thumbnail_md_path': self.board.thumbnail_md_path,
            'thumbnail_lg_path': self.board.thumbnail_lg_path,
            'html_url': self.board.html_url,
            'activity_html_url': self.board.activity_html_url,
            'color': 'red',
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_anonymous_user_retrieve_shared_board(self):
        """
        Tests that viewset allows anonymous user to retrieve shared board.
        """
        self.board.is_shared = True
        self.board.save()

        self.client = APIClient()
        response = self.client.get(
            '{}{}/'.format(self.base_url, self.board.id))

        created_by = NestedUserSerializer(self.board.created_by).data
        modified_by = NestedUserSerializer(self.board.modified_by).data

        expected_response = {
            'created_by': created_by,
            'modified_by': modified_by,
            'id': self.board.id,
            'date_created': self.board.date_created,
            'date_modified': self.board.date_modified,
            'name': 'The Board',
            'slug': 'the-board',
            'account': self.board.account_id,
            'is_shared': True,
            'thumbnail_xs_path': self.board.thumbnail_xs_path,
            'thumbnail_sm_path': self.board.thumbnail_sm_path,
            'thumbnail_md_path': self.board.thumbnail_md_path,
            'thumbnail_lg_path': self.board.thumbnail_lg_path,
            'html_url': self.board.html_url,
            'activity_html_url': self.board.activity_html_url,
            'color': '',
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_requires_authentication_to_modify_shared_board(self):
        """
        Tests that viewset should only allow anonymous users
        to retrieve shared boards.
        """
        self.board.is_shared = True
        self.board.save()

        data = {
            'name': 'New Board Name',
            'slug': 'the-board',
            'account': self.account.id
        }

        self.client = APIClient()
        response = self.client.patch(
            '{}{}/'.format(self.base_url, self.board.id), data, format='json')

        self.board = Board.objects.get(pk=self.board.id)

        expected_response = {
            'error': 'Authentication credentials were not provided.',
            'status_code': 401
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_return_collaborators_user_can_access(self):
        """
        Tests that viewset returns board collaborators of
        boards that the user can access.
        """
        url = '{}{}/collaborators/'.format(self.base_url, self.board.id)
        response = self.client.get(url)

        expected_response = [{
            'id': self.board_collaborator.id,
            'date_created': self.board_collaborator.date_created,
            'date_modified': self.board_collaborator.date_modified,
            'board': self.board.id,
            'user': self.board_collaborator.user.id,
            'user_data': {
                'id': self.board_collaborator.user.id,
                'username': self.board_collaborator.user.username,
                'first_name': self.board_collaborator.user.first_name,
                'last_name': self.board_collaborator.user.last_name,
                'email': self.board_collaborator.user.email,
                'avatar_path': self.board_collaborator.user.avatar_path,
                'gravatar_url': self.board_collaborator.user.gravatar_url,
                'timezone': self.board_collaborator.user.timezone,
                'date_created': self.board_collaborator.user.date_created,
                'date_modified': self.board_collaborator.user.date_modified,
            },
            'invited_user': None,
            'permission': self.board_collaborator.permission
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_collaborators_should_use_public_serializer(self):
        """
        Test that viewset uses public serializer when needed.
        """
        self.board.is_shared = True
        self.board.save()

        self.client = APIClient()

        url = '{}{}/collaborators/'.format(self.base_url, self.board.id)
        response = self.client.get(url)

        created_by = NestedUserSerializer(self.board.created_by).data
        modified_by = NestedUserSerializer(self.board.modified_by).data

        expected_response = [{
            'id': self.board_collaborator.id,
            'date_created': self.board_collaborator.date_created,
            'date_modified': self.board_collaborator.date_modified,
            'board': self.board.id,
            'user': self.board_collaborator.user.id,
            'created_by': created_by,
            'modified_by': modified_by,
            'user_data': {
                'id': self.board_collaborator.user.id,
                'username': self.board_collaborator.user.username,
                'first_name': self.board_collaborator.user.first_name,
                'last_name': self.board_collaborator.user.last_name,
                'avatar_path': self.board_collaborator.user.avatar_path,
                'gravatar_url': self.board_collaborator.user.gravatar_url,
                'timezone': self.board_collaborator.user.timezone,
                'date_created': self.board_collaborator.user.date_created,
                'date_modified': self.board_collaborator.user.date_modified,
            },
            'invited_user': None,
            'permission': self.board_collaborator.permission
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_shouldnt_return_collabs_to_user_with_no_access(self):
        """
        Tests that viewset doesn't returns collaborator
        that the user can't access.
        """
        self.client = APIClient()

        url = '{}{}/collaborators/'.format(self.base_url, self.board.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_viewset_bulk_create(self):
        """
        Tests that viewset can accept an array to create.
        """
        data = [{
            'email': 'abc@example.com',
            'board': self.board.id,
            'permission': 'write'
        }]

        url = '{}{}/collaborators/'.format(self.base_url, self.board.id)
        response = self.client.post(url, data, format='json')

        invited_user = InvitedUser.objects.get(email='abc@example.com')
        board_collaborator = BoardCollaborator.objects.get(
            invited_user=invited_user, board=self.board)

        expected_response = [{
            'id': board_collaborator.id,
            'date_created': board_collaborator.date_created,
            'date_modified': board_collaborator.date_modified,
            'board': self.board.id,
            'user': None,
            'invited_user': board_collaborator.invited_user.id,
            'permission': self.board_collaborator.permission,
            'user_data': {
                'id': invited_user.id,
                'first_name': '',
                'last_name': '',
                'username': invited_user.username,
                'email': invited_user.email,
                'gravatar_url': invited_user.gravatar_url,
                'date_created': invited_user.date_created,
                'date_modified': invited_user.date_modified,
            }
        }]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)


class BoardCollaboratorViewSetViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(BoardCollaboratorViewSetViewSetTestCase, self).setUp()

        self.create_account()
        self.create_board()

        self.base_url = '/api/v1/boards/collaborators/'

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

    def test_viewset_should_check_permissions(self):
        """
        Tests that viewset checks for custom permissions.
        """
        self.account_owner.delete()
        self.board_collaborator.delete()

        data = {
            'board': self.board.id,
            'user': self.user.id,
            'permission': "write"
        }

        response = self.client.put(
            '{}{}/'.format(self.base_url, self.board.id), data, format='json')

        expected_response = {
            'status_code': 403,
            'error': 'You do not have permission to perform this action.'
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response)

    def test_viewset_serializer_update(self):
        """
        Test that viewset can update BoardCollaborator.
        """
        user = self.create_another_user()

        data = {
            'board': self.board.id,
            'user': user.id,
            'permission': "write"
        }

        url = '{}{}/'.format(self.base_url, self.board_collaborator.id)

        response = self.client.put(url, data, format='json')

        board_collaborator = BoardCollaborator.objects.get(
            pk=self.board_collaborator.id)

        expected_response = {
            'id': board_collaborator.id,
            'date_created': board_collaborator.date_created,
            'date_modified': board_collaborator.date_modified,
            'board': self.board.id,
            'user': board_collaborator.user.id,
            'invited_user': None,
            'permission': board_collaborator.permission,
            'user_data': {
                'id': board_collaborator.user.id,
                'username': board_collaborator.user.username,
                'first_name': board_collaborator.user.first_name,
                'last_name': board_collaborator.user.last_name,
                'email': board_collaborator.user.email,
                'avatar_path': board_collaborator.user.avatar_path,
                'gravatar_url': board_collaborator.user.gravatar_url,
                'timezone': board_collaborator.user.timezone,
                'date_created': board_collaborator.user.date_created,
                'date_modified': board_collaborator.user.date_modified,
            }
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)


class BoardCollaboratorRequestViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(BoardCollaboratorRequestViewSetTestCase, self).setUp()

        self.create_account()
        self.create_board()

        self.base_url = '/api/v1/boards/collaborators/requests/'

    def test_disallowed_methods(self):
        """
        Tests viewset's disallowed methods.
        """
        response = self.client.put(self.base_url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(self.base_url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.base_url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_action_requires_no_auth_or_permissions(self):
        """
        Tests that POST to create a request doesn't require auth or perms.
        """
        self.client = APIClient()
        data = {
            'email': self.user.email,
            'board': self.board.id
        }

        response = self.client.post(self.base_url, data, format='json')

        request = BoardCollaboratorRequest.objects.get(
            email=self.user.email, board=self.board)

        expected_response = {
            'id': request.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'board': self.board.id,
            'message': '',
            'user': self.user.id,
            'date_created': request.date_created,
            'date_modified': request.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_list_action_require_auth_and_perms(self):
        """
        Tests that list action requires auth and perms.
        """
        request = BoardCollaboratorRequest.objects.create(
            email=self.user.email, board=self.board)

        response = self.client.get(self.base_url)

        expected_response = [{
            'id': request.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'board': self.board.id,
            'message': '',
            'user': self.user.id,
            'date_created': request.date_created,
            'date_modified': request.date_modified
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_retrieve_action_require_auth_and_perms(self):
        """
        Tests that retrieve action requires auth and perms.
        """
        request = BoardCollaboratorRequest.objects.create(
            email=self.user.email, board=self.board)

        response = self.client.get('{}{}/'.format(self.base_url, request.id))

        expected_response = {
            'id': request.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'board': self.board.id,
            'message': '',
            'user': self.user.id,
            'date_created': request.date_created,
            'date_modified': request.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_shouldnt_return_for_user_without_access(self):
        """
        Tests that viewset only returns requests they can see.
        """
        BoardCollaboratorRequest.objects.create(
            email=self.user.email, board=self.board)

        self.account_owner.delete()

        response = self.client.get(self.base_url)
        expected_response = []

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_retrieve_should_return_request(self):
        """
        Tests that retrieve action should return a request.
        """
        request = BoardCollaboratorRequest.objects.create(
            email=self.user.email, board=self.board)

        response = self.client.get('{}{}/'.format(self.base_url, request.id))

        expected_response = {
            'id': request.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'board': self.board.id,
            'message': '',
            'user': self.user.id,
            'date_created': request.date_created,
            'date_modified': request.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_accept_action_should_require_auth_and_perms(self):
        """
        Tests that accept action requires auth and perms.
        """
        self.client = APIClient()

        request = BoardCollaboratorRequest.objects.create(
            email=self.user.email, board=self.board)

        response = self.client.put(
            '{}{}/accept/'.format(self.base_url, request.id))

        expected_response = {
            'status_code': 401,
            'error': 'Authentication credentials were not provided.'
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected_response)

    def test_reject_action_should_require_auth_and_perms(self):
        """
        Tests that reject action requires auth and perms.
        """
        self.client = APIClient()

        request = BoardCollaboratorRequest.objects.create(
            email=self.user.email, board=self.board)

        response = self.client.put(
            '{}{}/accept/'.format(self.base_url, request.id))

        expected_response = {
            'status_code': 401,
            'error': 'Authentication credentials were not provided.'
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected_response)

    def test_accept_action_should_return_request(self):
        """
        Tests that accept action returns request.
        """
        request = BoardCollaboratorRequest.objects.create(
            email=self.user.email, board=self.board)

        response = self.client.put(
            '{}{}/accept/'.format(self.base_url, request.id))

        expected_response = {
            'id': None,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'board': self.board.id,
            'message': '',
            'user': self.user.id,
            'date_created': request.date_created,
            'date_modified': request.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_reject_action_should_return_request(self):
        """
        Tests that accept action returns request.
        """
        request = BoardCollaboratorRequest.objects.create(
            email=self.user.email, board=self.board)

        response = self.client.put(
            '{}{}/reject/'.format(self.base_url, request.id))

        expected_response = {
            'id': None,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'board': self.board.id,
            'message': '',
            'user': self.user.id,
            'date_created': request.date_created,
            'date_modified': request.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)


class BoardHTMLViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(BoardHTMLViewTestCase, self).setUp()

        self.create_account()
        self.create_board()

        self.url = '/{}/{}/'.format(self.account.slug, self.board.slug)

    def test_view_should_render_html_template(self):
        """
        Tests that view renders our expected template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

    def test_view_should_raise_404_invalid_board(self):
        """
        Tests that view raises 404 for invalid tokens.
        """
        response = self.client.get('/account/board/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_should_include_javascript_object(self):
        """
        Tests that view contains the JS object window.App.PUBLIC_BOARD
        """
        self.board.is_shared = True
        self.board.save()

        response = self.client.get(self.url)

        self.assertContains(response, 'PUBLIC_BOARD:')
        self.assertContains(response, 'id: {}'.format(self.board.id))
        self.assertContains(response, 'collaborator_users: [{}]'.format(
                            self.board_collaborator.user_id))
