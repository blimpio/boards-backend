from ...utils.tests import BaseTestCase
from ..models import Comment


class CommentTestCase(BaseTestCase):
    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(Comment._meta.fields), 8)
