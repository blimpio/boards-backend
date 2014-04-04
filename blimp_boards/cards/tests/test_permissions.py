from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

from ...utils.tests import BaseTestCase
from ..permissions import CardPermission


class MockView(APIView):
    pass

mock_view = MockView.as_view()


class CardPermissionTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()
        self.create_card()

        self.factory = APIRequestFactory()
        self.perm_class = CardPermission()

    def test_should_return_true_for_authenticated_user(self):
        """
        Tests that `.has_permission` returns `True` for an
        authenticated user.
        """
        request = Request(self.factory.get('/', format='json'))
        request.parsers = (JSONParser(), )
        request.user = self.user

        view = mock_view(request)
        view.action = 'list'

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_should_return_false_for_anonymous_user(self):
        """
        Tests that `.has_permission` returns `False` for an
        unauthenticated user.
        """
        request = Request(self.factory.post('/', format='json'))
        request.parsers = (JSONParser(), )
        request.user = AnonymousUser()

        view = mock_view(request)
        view.action = 'create'

        has_perm = self.perm_class.has_permission(request, view)

        self.assertFalse(has_perm)

    def test_should_return_true_for_anonymous_user_listing_with_board(self):
        """
        Tests that `.has_permission` returns `True` for an
        unauthenticated user listing cards for a specific board.
        """
        params = {'board': self.board.id}
        request = Request(self.factory.get('/', params, format='json'))
        request.parsers = (JSONParser(), )
        request.user = AnonymousUser()

        view = mock_view(request)
        view.action = 'list'

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
            request, view, self.card)

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
            request, view, self.card)

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
            request, view, self.card)

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
            request, view, self.card)

        self.assertTrue(has_perm)
