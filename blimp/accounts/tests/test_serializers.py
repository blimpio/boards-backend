from django.test import TestCase

from blimp.accounts.models import EmailDomain
from ..serializers import ValidateSignupDomainsSerializer


class ValidateSignupDomainsSerializerTestCase(TestCase):
    def setUp(self):
        EmailDomain.objects.create(domain_name='example.com')

        self.data = {
            'signup_domains': ['example-domain.com']
        }

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data returns empty signup_domains.
        """
        serializer = ValidateSignupDomainsSerializer()

        self.assertEqual(serializer.data, {'signup_domains': ''})

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = ValidateSignupDomainsSerializer(data={})
        serializer.is_valid()
        expected_errors = {
            'signup_domains': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_object_should_have_signup_domains_key(self):
        """
        Tests that serializer.object should be a dictionary
        with a signup_domains key.
        """
        serializer = ValidateSignupDomainsSerializer(data=self.data)
        serializer.is_valid()

        self.assertTrue('signup_domains' in serializer.data)

    def test_serializer_should_return_error_if_domain_name_is_invalid(self):
        """
        Tests that serializer should return error if domain name is
        blacklisted or used.
        """
        self.data['signup_domains'] = ['gmail.com', 'example.com']

        serializer = ValidateSignupDomainsSerializer(data=self.data)
        serializer.is_valid()
        expected_errors = {
            'signup_domains': ["gmail.com is an invalid sign-up domain."]
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_return_list_of_valid_domains(self):
        """
        Tests that serializer should list of valid domains.
        """
        serializer = ValidateSignupDomainsSerializer(data=self.data)
        serializer.is_valid()
        expected_data = {
            'signup_domains': ['example-domain.com']
        }

        self.assertEqual(serializer.data, expected_data)
