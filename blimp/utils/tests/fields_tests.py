from django.test import TestCase

from ..fields import CharacterSeparatedField, PasswordField


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
        field = PasswordField()
        self.assertEqual(field.min_length, 6)
        self.assertEqual(field.max_length, None)
