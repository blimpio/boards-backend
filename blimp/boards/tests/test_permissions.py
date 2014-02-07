from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from ...utils.tests import BaseTestCase
from ..models import BoardCollaboratorRequest
from ..permissions import BoardPermission, BoardCollaboratorRequestPermission


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
        request = self.factory.post('/')
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_should_return_false_for_anonymous_user(self):
        request = self.factory.post('/')
        request.user = AnonymousUser()

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertFalse(has_perm)

    def test_returns_true_for_user_with_write_perm(self):
        request = self.factory.post('/')
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertTrue(has_perm)

    def test_returns_false_for_user_without_write_perm(self):
        request = self.factory.post('/')
        request.user = self.user

        self.board_collaborator.permission = 'read'
        self.board_collaborator.save()

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertFalse(has_perm)

    def test_returns_true_for_user_with_read_perm(self):
        request = self.factory.get('/')
        request.user = self.user

        self.board_collaborator.permission = 'read'
        self.board_collaborator.save()

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertTrue(has_perm)

    def test_returns_true_for_user_with_write_perm_get_method(self):
        request = self.factory.get('/')
        request.user = self.user

        self.board_collaborator.permission = 'write'
        self.board_collaborator.save()

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, self.board)

        self.assertTrue(has_perm)


class BoardCollaboratorRequestPermissionTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

        self.factory = APIRequestFactory()
        self.perm_class = BoardCollaboratorRequestPermission()

    def test_should_return_true_for_authenticated_user(self):
        request = self.factory.post('/')
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertTrue(has_perm)

    def test_should_return_false_for_anonymous_user(self):
        request = self.factory.post('/')
        request.user = AnonymousUser()

        view = mock_view(request)

        has_perm = self.perm_class.has_permission(request, view)

        self.assertFalse(has_perm)

    def test_should_return_true_for_owner(self):
        request = self.factory.get('/')
        request.user = self.user

        collaborator_request = BoardCollaboratorRequest.objects.create(
            user=self.user, board=self.board)

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, collaborator_request)

        self.assertTrue(has_perm)

    def test_should_return_false_for_user_that_is_not_owner(self):
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
