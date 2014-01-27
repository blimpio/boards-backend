# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError

from ..validators import (DomainNameValidator, validate_domain_name,
                          is_valid_email, is_valid_domain_name)


class ValidatorsTestCase(TestCase):
    def setUp(self):
        self.valid_email = 'jpueblo@example.com'
        self.invalid_email = '.@example.com'
        self.valid_domain = 'example.com'
        self.invalid_domain = 'examplecom'

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

    def test_is_valid_domainname_should_return_true_with_valid_domain(self):
        """
        Tests that is_valid_domain_name returns True for a valid domain.
        """
        self.assertTrue(is_valid_domain_name(self.valid_domain))

    def test_is_valid_domainname_should_return_false_with_invalid_domain(self):
        """
        Tests that is_valid_domain_name returns True for a valid domain.
        """
        self.assertFalse(is_valid_domain_name(self.invalid_domain))


class DomainNameValidatorTestCase(TestCase):
    def setUp(self):
        self.valid_domains = [
            'here.com', 'here.and.there.com', '[127.0.0.1]',
            'valid-----hyphens.com', 'valid-with-hyphens.com',
            'domain.with.idn.tld.उदाहरण.परीक्षा', 'localhost'
        ]

        self.invalid_domains = [
            None, '', 'abc', '.com', '127.0.0.1', 'invalid-.com',
            '-invalid.com', 'inv-.alid-.com', 'inv-.-alid.com',
            'example.com\n\n<script src="x.js">', 'shouldfail.com.'
        ]

        self.validator = DomainNameValidator()

    def test_valid_domains_should_return_none(self):
        """
        Tests that an expected valid domain name returns None.
        """
        for domain in self.valid_domains:
            self.assertEqual(self.validator(domain), None)

    def test_invalid_domains_should_raise_validation_error(self):
        """
        Tests that an expected invalid domain name raises ValidationError.
        """
        for domain in self.invalid_domains:
            with self.assertRaises(ValidationError):
                self.validator(domain)

    def test_whitelist_domain_should_return_none(self):
        """
        Tests that setting a custom whitelist domain list and
        checking a valid domain returns None.
        """
        validator = DomainNameValidator(whitelist=['localdomain'])
        self.assertEqual(validator('localdomain'), None)

    def test_validate_domain_name_should_be_a_shortcut(self):
        """
        Tests that an expected valid domain name returns None
        with validate_domain_name shortcut.
        """
        for domain in self.valid_domains:
            self.assertEqual(validate_domain_name(domain), None)
