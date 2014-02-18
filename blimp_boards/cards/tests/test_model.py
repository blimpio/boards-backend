from django.core.exceptions import ValidationError

from ...utils.tests import BaseTestCase
from ..models import Card


class CardTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(Card._meta.fields), 16)

    def test_model_should_validate_card_content(self):
        """
        Tests that card should have content if not a stack.
        """
        with self.assertRaises(ValidationError):
            Card.objects.create(
                name='The Card', type='note',
                board=self.board, created_by=self.user)

    def test_model_should_validate_card_stack(self):
        """
        Tests that model validates disallowed_fields when
        card type is stack.
        """
        with self.assertRaises(ValidationError):
            Card.objects.create(
                name='The Card', type='stack', board=self.board,
                created_by=self.user, content='Err!', file_extension='exe')
