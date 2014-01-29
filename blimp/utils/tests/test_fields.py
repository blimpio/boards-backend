from django.test import TestCase
from django.core.exceptions import ValidationError

from ..fields import CharacterSeparatedField, PasswordField, ListField


class CharacterSeparatedFieldTestCase(TestCase):
    def test_field_default_separator_is_comma(self):
        """
        Tests that field should have a default comma separator specified.
        """
        field = CharacterSeparatedField()
        self.assertEqual(field.separator, ',')

    def test_field_should_accept_custom_separator(self):
        """
        Tests that field should accept a custom separator.
        """
        field = CharacterSeparatedField(separator='.')
        self.assertEqual(field.separator, '.')

    def test_field_to_native_should_return_str_for_given_list(self):
        """
        Tests that field's to_native method should return a string
        from a specified list.
        """
        field = CharacterSeparatedField()
        self.assertEqual(field.to_native(['a', 'b', 'c']), 'a,b,c')

    def test_field_from_native_should_return_list_for_given_str(self):
        """
        Tests that field's from_native method should return a list
        from a specified string.
        """
        field = CharacterSeparatedField()
        self.assertEqual(field.from_native('a,b,c'), ['a', 'b', 'c'])


class PasswordFieldTesetCase(TestCase):
    def test_field_should_have_default_length_options(self):
        """
        Tests that field should have default min_length and max_length set.
        """
        field = PasswordField()
        self.assertEqual(field.min_length, 6)
        self.assertEqual(field.max_length, None)


class ListFieldTestCase(TestCase):
    def setUp(self):
        self.field = ListField()

    def test_that_field_validates_value_as_list(self):
        """
        Tests that validate() validates value is a list first.
        """
        with self.assertRaises(ValidationError):
            self.field.validate('not a list')

    def test_that_field_validates_value(self):
        """
        Tests that validate() validates each value in the list.
        """
        with self.assertRaises(ValidationError):
            self.field.validate([None])

    def test_that_run_validators_runs_validator_for_list_values(self):
        """
        Tests that run_validators() runs validator for
        each value in the list.
        """
        def validate_not_none(value):
            if value is not None:
                raise ValidationError('err')

        field = ListField(validators=[validate_not_none])

        with self.assertRaises(ValidationError):
            field.run_validators(["jpadilla.com", None])
