from django.test import TestCase

from ..models import SignupRequest
from ..serializers import ValidateSignupRequestSerializer


class ValidateSignupRequestSerializerTestCase(TestCase):
    def setUp(self):
        self.email = 'jpueblo@example.com'

        self.signup_request = SignupRequest.objects.create(email=self.email)

        self.data = {
            'token': self.signup_request.token
        }

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = ValidateSignupRequestSerializer()
        self.assertEqual(serializer.data, {})

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = ValidateSignupRequestSerializer(data={})
        serializer.is_valid()
        expected_errors = {
            'token': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_no_signup_request_found(self):
        """
        Tests serializer's No Invite Request validation errors.
        """
        self.data['token'] = 'abc'
        serializer = ValidateSignupRequestSerializer(data=self.data)
        serializer.is_valid()
        expected_errors = {
            'token': ['No Invite Request found.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_return_signup_request(self):
        """
        Tests that serializer should return expected data when valid.
        """
        serializer = ValidateSignupRequestSerializer(data=self.data)
        serializer.is_valid()

        expected_data = {
            'email': self.email
        }

        self.assertEqual(serializer.data, expected_data)
