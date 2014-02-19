from ...utils.tests import BaseTestCase
from ..serializers import CommentSerializer
from ..models import Comment


class CommentSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.serializer_class = CommentSerializer

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = self.serializer_class()
        expected_data = {
            'content': ''
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = self.serializer_class(data={})
        serializer.is_valid()

        expected_errors = {
            'content': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_returns_expected_data_for_object(self):
        """
        Tests serializer returns expected data for a given object.
        """
        self.create_user()

        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=self.user)

        serializer = self.serializer_class(comment)
        serializer.is_valid()

        expected_data = {
            'id': comment.id,
            'content': 'A comment',
            'created_by': self.user.id,
            'date_created': comment.date_created,
            'date_modified': comment.date_modified
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_created_by_readonly_field(self):
        """
        Tests serializer created_by readonly field.
        """
        self.create_user()

        comment = Comment.objects.create(
            content='A comment',
            content_object=self.user,
            created_by=self.user)

        data = {
            'content': 'updated my comment.',
            'created_by': None
        }

        serializer = self.serializer_class(comment, data=data)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'id': comment.id,
            'content': 'updated my comment.',
            'created_by': self.user.id,
            'date_created': comment.date_created,
            'date_modified': comment.date_modified
        }

        self.assertEqual(serializer.data, expected_data)
