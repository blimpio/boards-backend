from django.test import TestCase

from ..models import Comment


class CommentTestCase(TestCase):
    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(Comment._meta.fields), 7)
