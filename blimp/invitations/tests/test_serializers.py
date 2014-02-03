from django.test import TestCase

from ..serializers import SignupRequestSerializer


class SignupRequestSerializerTestCase(TestCase):
    def setUp(self):
        self.email = 'jpueblo@example.com'

        self.data = {
            'email': self.email
        }

    def test_serializer_empty_data(self):
        """
        Tests that serializer.object returns None if no data given.
        """
        serializer = SignupRequestSerializer()
        self.assertEqual(serializer.object, None)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = SignupRequestSerializer(data={})
        serializer.is_valid()
        expected_errors = {
            'email': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_valid_data(self):
        """
        Tests serializer expected data if valid.
        """
        serializer = SignupRequestSerializer(data=self.data)
        serializer.is_valid()

        self.assertEqual(serializer.data, self.data)
