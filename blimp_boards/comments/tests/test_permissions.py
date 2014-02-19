from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

from ...utils.tests import BaseTestCase
from ...users.models import User
from ..models import Comment
from ..permissions import CommentPermission


class MockView(APIView):
    pass

mock_view = MockView.as_view()


class BoardPermissionTestCase(BaseTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.perm_class = CommentPermission()

    def test_should_return_true_for_authenticated_user(self):
        """
        Tests that `.has_permission` returns `True` for an
        authenticated user.
        """
        self.create_user()

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

    def test_returns_true_for_user_that_created_comment(self):
        """
        Tests that `.has_object_permission` returns `True` for
        the user that created the comment.
        """
        self.create_user()

        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=self.user)

        request = self.factory.post('/')
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, comment)

        self.assertTrue(has_perm)

    def test_returns_false_for_user_that_didnt_create_comment(self):
        """
        Tests that `.has_object_permission` returns `False` for
        a user other than the one that created the comment.
        """
        self.create_user()
        user = self.create_another_user(username='pedro')

        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=user)

        request = self.factory.post('/')
        request.user = self.user

        view = mock_view(request)

        has_perm = self.perm_class.has_object_permission(
            request, view, comment)

        self.assertFalse(has_perm)
