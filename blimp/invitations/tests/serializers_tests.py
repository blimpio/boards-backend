from django.test import TestCase

from ..models import InviteRequest
from ..serializers import ValidateInviteRequestSerializer


class ValidateInviteRequestSerializerTestCase(TestCase):
    def setUp(self):
        self.email = 'jpueblo@example.com'

        self.invite_request = InviteRequest.objects.create(email=self.email)

        self.data = {
            'token': self.invite_request.token
        }

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = ValidateInviteRequestSerializer()
        self.assertEqual(serializer.data, {})

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = ValidateInviteRequestSerializer(data={})
        serializer.is_valid()
        expected_errors = {
            'token': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_no_invite_request_found(self):
        """
        Tests serializer's No Invite Request validation errors.
        """
        self.data['token'] = 'abc'
        serializer = ValidateInviteRequestSerializer(data=self.data)
        serializer.is_valid()
        expected_errors = {
            'token': ['No Invite Request found.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_return_invite_request(self):
        """
        Tests that serializer should return expected data when valid.
        """
        serializer = ValidateInviteRequestSerializer(data=self.data)
        serializer.is_valid()

        expected_data = {
            'email': self.email
        }

        self.assertEqual(serializer.data, expected_data)
