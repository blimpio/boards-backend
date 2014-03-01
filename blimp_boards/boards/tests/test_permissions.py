from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

from ...utils.tests import BaseTestCase
from ...users.models import User
from ..models import BoardCollaboratorRequest
from ..permissions import (BoardPermission, BoardCollaboratorPermission,
                           BoardCollaboratorRequestPermission)


class MockView(APIView):
    pass

mock_view = MockView.as_view()


class BoardPermissionTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

        self.factory = APIRequestFactory()
        self.perm_class = BoardPermission()

    def test_should_return_true_for_authenticated_user(self):
        """
        Tests that `.has_permission` returns `True` for an
        authenticated user.
        """
        request = self.factory.post('/')
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_should_return_false_for_anonymous_user_unsafe(self):
        """
        Tests that `.has_permission` returns `False` for an
        unauthenticated user and unsafe method.
        """
        request = self.factory.post('/')
        request.user = AnonymousUser()

        view = mock_view(request)
        view.action = 'create'

        has_perm = self.perm_class.has_permission(request, view)

        self.assertFalse(has_perm)

    def test_should_return_false_for_anonymous_user_safe(self):
        """
        Tests that `.has_permission` returns `True` for an
        unauthenticated user.
        """
        request = self.factory.get('/')
        request.user = AnonymousUser()

        view = mock_view(request)
        view.action = 'list'

        has_perm = self.perm_class.has_permission(request, view)

        self.assertFalse(has_perm)

    def test_should_return_true_for_anonymous_user_viewing_shared_board(self):
        """
        Tests that `.has_permission` returns `True` for an
        unauthenticated user retrieving a board.
        """
        request = self.factory.get('/')
        request.user = AnonymousUser()

        view = mock_view(request)
        view.action = 'retrieve'

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_returns_true_for_user_with_write_perm(self):
        """
        Tests that `.has_object_permission` returns `True` for
        a user with write permissions using an unsafe method.
        """
        request = self.factory.post('/')
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertTrue(has_perm)

    def test_returns_false_for_user_without_write_perm(self):
        """
        Tests that `.has_object_permission` returns `False` for
        a user with read permissions using an unsafe method.
        """
        request = self.factory.post('/')
        request.user = self.user

        self.board_collaborator.permission = 'read'
        self.board_collaborator.save()

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertFalse(has_perm)

    def test_returns_true_for_user_with_read_perm(self):
        """
        Tests that `.has_object_permission` returns `True` for
        a user with read permissions using a safe method.
        """
        request = self.factory.get('/')
        request.user = self.user

        self.board_collaborator.permission = 'read'
        self.board_collaborator.save()

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertTrue(has_perm)

    def test_returns_true_for_user_with_write_perm_get_method(self):
        """
        Tests that `.has_object_permission` returns `True` for
        a user with write permissions using a safe method.
        """
        request = self.factory.get('/')
        request.user = self.user

        self.board_collaborator.permission = 'write'
        self.board_collaborator.save()

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertTrue(has_perm)

    def test_returns_true_for_anonymous_and_shared_board(self):
        """
        Tests that `.has_object_permission` returns `True` for
        an anonymous user retrieving shared board.
        """
        self.board.is_shared = True
        self.board.save()

        request = self.factory.get('/')
        request.user = AnonymousUser()

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertTrue(has_perm)


class BoardCollaboratorPermissionTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

        self.factory = APIRequestFactory()
        self.perm_class = BoardCollaboratorPermission()

        self.data = {
            'board': self.board.id
        }

    def test_authentication_is_required(self):
        """
        Tests that `.has_permission` returns `False`
        if user is not authenticated.
        """
        request = Request(self.factory.post('/', self.data, format='json'))
        request.parsers = (JSONParser(), )

        view = mock_view(request)
        view.action = 'create'

        has_perm = self.perm_class.has_permission(request, view)

        self.assertFalse(has_perm)

    def test_board_does_not_exist_should_return_false(self):
        """
        Tests that `.has_permission` returns `False`
        if board does not exist.
        """
        self.data = {
            'board': 1333
        }

        request = Request(self.factory.post('/', self.data, format='json'))
        request.parsers = (JSONParser(), )
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertFalse(has_perm)

    def test_has_permission_should_return_true(self):
        """
        Tests that `.has_permission` returns `True`.
        """
        request = Request(self.factory.get('/'))
        request.parsers = (JSONParser(), )
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_collaborator_with_write_perms_can_create(self):
        """
        Tests that `.has_permission` returns `True`
        for collaborator with write permissions.
        """
        request = Request(self.factory.post('/', self.data, format='json'))
        request.parsers = (JSONParser(), )
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_collaborator_is_account_owner_can_create(self):
        """
        Tests that `.has_permission` returns `True`
        for collaborator that is account owner.
        """
        self.board_collaborator.delete()

        request = Request(self.factory.post('/', self.data, format='json'))
        request.parsers = (JSONParser(), )
        request.user = self.account_owner.user

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_collaborator_with_write_perms_can_update(self):
        """
        Tests that `.has_object_permission` returns `True`
        for collaborator with write permissions.
        """
        request = Request(self.factory.put('/', self.data, format='json'))
        request.parsers = (JSONParser(), )
        request.user = self.user

        view = mock_view(request)
        has_perm = self.perm_class.has_object_permission(
            request, view, self.board_collaborator)

        self.assertTrue(has_perm)

    def test_collaborator_with_read_perms_can_delete_self(self):
        """
        Tests that collaborator with read perms can only
        delete it's own object.
        """
        self.account_owner.is_owner = False
        self.account_owner.save()

        user = User.objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password=self.password,
            first_name='Other',
            last_name='User'
        )

        self.board_collaborator.permission = 'read'
        self.board_collaborator.user = user
        self.board_collaborator.save()

        request = Request(self.factory.delete('/', self.data, format='json'))
        request.parsers = (JSONParser(), )
        request.user = self.user

        view = mock_view(request)
        has_perm = self.perm_class.has_object_permission(
            request, view, self.board_collaborator)

        self.assertFalse(has_perm)

    def test_collaborator_is_account_owner_can_update(self):
        """
        Tests that collaborator account owner can update.
        """
        self.board_collaborator.delete()

        request = Request(self.factory.put('/', self.data, format='json'))
        request.parsers = (JSONParser(), )
        request.user = self.user

        view = mock_view(request)
        has_perm = self.perm_class.has_object_permission(
            request, view, self.board_collaborator)

        self.assertTrue(has_perm)


class BoardCollaboratorRequestPermissionTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

        self.factory = APIRequestFactory()
        self.perm_class = BoardCollaboratorRequestPermission()

    def test_should_return_true_for_authenticated_user(self):
        """
        Tests that `.has_permission` returns `True` for an
        authenticated user.
        """
        request = self.factory.post('/')
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_should_return_false_for_anonymous_user(self):
        """
        Tests that `.has_permission` returns `True` for an
        unauthenticated user.
        """
        request = self.factory.post('/')
        request.user = AnonymousUser()

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertFalse(has_perm)

    def test_should_return_true_for_owner(self):
        """
        Tests that `.has_object_permission` returns `True`
        for account owner.
        """
        request = self.factory.get('/')
        request.user = self.user

        collaborator_request = BoardCollaboratorRequest.objects.create(
            user=self.user, board=self.board)

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, collaborator_request)

        self.assertTrue(has_perm)

    def test_should_return_false_for_user_that_is_not_owner(self):
        """
        Tests that `.has_object_permission` returns `True`
        for a user that is not the account owner.
        """
        request = self.factory.get('/')
        request.user = self.user

        self.account_owner.is_owner = False
        self.account_owner.save()

        collaborator_request = BoardCollaboratorRequest.objects.create(
            user=self.user, board=self.board)

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, collaborator_request)

        self.assertFalse(has_perm)
