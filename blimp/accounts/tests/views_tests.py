from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ValidateSignupDomainsAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'signup_domains': 'example.com'
        }

        response = self.client.post(
            '/api/auth/signup_domains/validate/', data, format='json')

        expected_response = {
            'signup_domains': ['example.com']
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/signup_domains/validate/')

        expected_response = {
            'error': {
                'signup_domains': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_blacklisted_domain(self):
        """
        Tests that POST request with blacklisted domain to endpoint
        returns expected error.
        """
        data = {
            'signup_domains': 'gmail.com'
        }

        response = self.client.post(
            '/api/auth/signup_domains/validate/', data, format='json')

        expected_response = {
            'error': {
                'signup_domains': [
                    "You can't have gmail.com as a sign-up domain."
                ]
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)
