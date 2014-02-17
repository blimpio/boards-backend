from django.test import TestCase
from django.core.exceptions import ValidationError

from ..fields import PasswordField, ListField, DomainNameField


class PasswordFieldTestCase(TestCase):
    def test_field_should_have_default_length_options(self):
        """
        Tests that field should have default min_length and max_length set.
        """
        field = PasswordField()
        self.assertEqual(field.min_length, 6)
        self.assertEqual(field.max_length, None)


class DomainNameFieldTestCase(TestCase):
    def setUp(self):
        self.field = DomainNameField()

    def test_field_should_validate_domain(self):
        self.assertEqual(self.field.run_validators('example.com'), None)

    def test_field_should_raise_validation_error_if_value_not_a_domain(self):
        with self.assertRaises(ValidationError):
            self.field.run_validators('not a domain.')


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
