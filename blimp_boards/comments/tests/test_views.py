from rest_framework import status
from rest_framework.test import APIClient

from ...utils.tests import AuthenticatedAPITestCase
from ..models import Comment


class CommentViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(CommentViewSetTestCase, self).setUp()

        self.base_url = '/api/comments/'

        self.data = {
            'content': 'My content'
        }

    def test_viewset_should_require_authentication(self):
        """
        Tests that viewset requires authentication.
        """
        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=self.user)

        self.client = APIClient()
        response = self.client.get('{}{}/'.format(self.base_url, comment.id))

        expected_response = {
            'error': 'Authentication credentials were not provided.',
            'status_code': 401
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_check_permissions(self):
        """
        Tests that viewset checks for permissions.
        """
        user = self.create_another_user(username='pedro')

        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=user)

        response = self.client.get('{}{}/'.format(self.base_url, comment.id))

        expected_response = {
            'status_code': 403,
            'error': 'You do not have permission to perform this action.'
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_allow_creator_to_retrieve(self):
        """
        Tests that viewset allows creator to retrieve comment.
        """
        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=self.user)

        response = self.client.get('{}{}/'.format(self.base_url, comment.id))

        expected_response = {
            'id': comment.id,
            'content': 'A comment',
            'created_by': self.user.id,
            'date_created': comment.date_created,
            'date_modified': comment.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_allow_creator_to_update(self):
        """
        Tests that viewset allows creator to update comment.
        """
        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=self.user)

        data = {
            'content': 'Updated the comment.'
        }

        response = self.client.put(
            '{}{}/'.format(self.base_url, comment.id), data)

        comment = Comment.objects.get(pk=comment.id)

        expected_response = {
            'id': comment.id,
            'content': 'Updated the comment.',
            'created_by': self.user.id,
            'date_created': comment.date_created,
            'date_modified': comment.date_modified
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_viewset_should_allow_creator_to_destroy(self):
        """
        Tests that viewset allows creator to destroy comment.
        """
        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=self.user)

        data = {
            'content': 'Updated the comment.'
        }

        response = self.client.delete(
            '{}{}/'.format(self.base_url, comment.id), data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
