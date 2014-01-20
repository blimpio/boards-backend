from django.test import TestCase

from ..validators import email_re, is_valid_email


class ValidatorsTestCase(TestCase):
    def setUp(self):
        self.valid_email = 'jpueblo@example.com'
        self.invalid_email = '.@example.com'

    def test_email_regex_valid(self):
        """
        Tests that email regex from Django's core validators by
        searching on a valid value returns True.
        """
        self.assertTrue(email_re.search(self.valid_email))

    def test_email_regex_invalid(self):
        """
        Tests that email regex from Django's core validators by
        searching on a invalid value returns False.
        """
        self.assertFalse(email_re.search(self.invalid_email))

    def test_is_valid_email_should_return_true_with_valid_email(self):
        """
        Tests that is_valid_email returns True for a valid email.
        """
        self.assertTrue(is_valid_email(self.valid_email))

    def test_is_valid_email_should_return_false_with_invalid_email(self):
        """
        Tests that is_valid_email returns False for an invalid email.
        """
        self.assertFalse(is_valid_email(self.invalid_email))
