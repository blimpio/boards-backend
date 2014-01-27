from django.test import TestCase
from django.core.exceptions import ValidationError

from ..validators import validate_signup_domain


class ValidatorsTestCase(TestCase):
    def setUp(self):
        self.valid_domain = 'example.com'
        self.invalid_domain = 'examplecom'
        self.blacklisted_domain = 'gmail.com'

    def test_validate_signup_domain_validates_domain_name(self):
        """
        Tests that validate_signup_domain returns None for valid values.
        """
        self.assertEqual(validate_signup_domain(self.valid_domain), None)

    def test_validate_signup_domain_raises_error_invalid_domain(self):
        """
        Tests that validate_signup_domain raises ValidationError
        if validate_domain_name raises ValidationError.
        """
        with self.assertRaises(ValidationError):
            validate_signup_domain(self.invalid_domain)

    def test_validate_signup_domain_raises_error_blacklist_domain(self):
        """
        Tests that validate_signup_domain raises ValidationError
        for blacklisted signup domains.
        """
        with self.assertRaises(ValidationError):
            validate_signup_domain(self.blacklisted_domain)
