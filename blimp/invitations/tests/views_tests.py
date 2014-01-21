from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import InviteRequest


class InviteRequestCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.email = 'jpueblo@example.com'

        self.invite_request = InviteRequest.objects.create(email=self.email)

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'email': 'ppueblo@example.com'
        }

        response = self.client.post(
            '/api/auth/invite_request/', data, format='json')

        invite_request = InviteRequest.objects.get(email=data['email'])

        expected_response = {
            'id': invite_request.id,
            'email': invite_request.email
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/invite_request/')

        expected_response = {
            'error': {
                'email': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class ValidateInviteRequestAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.email = 'jpueblo@example.com'

        self.invite_request = InviteRequest.objects.create(email=self.email)

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'token': self.invite_request.token
        }

        response = self.client.post(
            '/api/auth/invite_request/validate/', data, format='json')

        expected_response = {
            'email': self.invite_request.email
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/invite_request/validate/')

        expected_response = {
            'error': {
                'token': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_no_invite_request_found(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        data = {
            'token': 'abc'
        }

        response = self.client.post(
            '/api/auth/invite_request/validate/', data, format='json')

        expected_response = {
            'error': {
                'token': ['No Invite Request found.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)
