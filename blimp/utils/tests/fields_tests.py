from django.test import TestCase

from ..fields import CharacterSeparatedField


class FieldsTestCase(TestCase):
    def test_field_default_separator_is_comma(self):
        field = CharacterSeparatedField()
        self.assertEquals(field.separator, ',')

    def test_field_should_accept_custom_separator(self):
        field = CharacterSeparatedField(separator='.')
        self.assertEquals(field.separator, '.')

    def test_field_to_native_should_return_str_for_given_list(self):
        field = CharacterSeparatedField()
        self.assertEquals(field.to_native(['a', 'b', 'c']), 'a,b,c')

    def test_field_from_native_should_return_list_for_given_str(self):
        field = CharacterSeparatedField()
        self.assertEquals(field.from_native('a,b,c'), ['a', 'b', 'c'])
