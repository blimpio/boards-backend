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
        self.assertEqual(len(Card._meta.fields), 23)

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
                created_by=self.user, content='Err!',
                mime_type='audio/mp4')

    def test_model_cards_set_stack(self):
        """
        Tests that adding cards on a stack, sets the stack
        ForeignKey field on cards added to cards ManyToManyField.
        """
        self.create_card()

        card = Card.objects.create(
            name='The Stack', type='stack',
            board=self.board, created_by=self.user)

        card.cards.add(self.card)

        self.card = Card.objects.get(pk=self.card.pk)

        self.assertEqual(self.card.stack, card)

    def test_model_remove_cards_unset_stack(self):
        """
        Tests that disolving cards on a stack, sets the stack
        ForeignKey field to None.
        """
        self.create_card()

        card = Card.objects.create(
            name='The Stack', type='stack',
            board=self.board, created_by=self.user)

        card.cards.add(self.card)

        card.cards.remove(self.card)

        self.card = Card.objects.get(pk=self.card.pk)

        self.assertEqual(self.card.stack, None)

    def test_model_clear_cards_unset_stack(self):
        """
        Tests that disolving cards on a stack, sets the stack
        ForeignKey field to None.
        """
        self.create_card()

        card = Card.objects.create(
            name='The Stack', type='stack',
            board=self.board, created_by=self.user)

        card.cards.add(self.card)

        card.cards.clear()

        self.card = Card.objects.get(pk=self.card.pk)

        self.assertEqual(self.card.stack, None)
