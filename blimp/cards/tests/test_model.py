from ...utils.tests import BaseTestCase
from ..models import Card


class CardTestCase(BaseTestCase):
    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(Card._meta.fields), 17)
