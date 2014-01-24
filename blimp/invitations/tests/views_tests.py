from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import SignupRequest


class SignupRequestCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.email = 'jpueblo@example.com'

        self.signup_request = SignupRequest.objects.create(email=self.email)

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'email': 'ppueblo@example.com'
        }

        response = self.client.post(
            '/api/auth/signup_request/', data, format='json')

        signup_request = SignupRequest.objects.get(email=data['email'])

        expected_response = {
            'email': signup_request.email
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/signup_request/')

        expected_response = {
            'error': {
                'email': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)
