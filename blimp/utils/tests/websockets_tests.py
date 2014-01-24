import json

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.test.client import RequestFactory
from rest_framework import permissions
from rest_framework.compat import patterns
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.test import APIClient
from wsrequest import WebSocketRequest

from blimp.users.models import User
from blimp.users.views import SigninAPIView
from blimp.users.authentication import JWTAuthentication


class MockAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, **kwargs):
        return Response({'foo': ['bar', 'baz']})

    def post(self, request, **kwargs):
        return Response({'foo': request.DATA})


class RestrictedAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, **kwargs):
        return Response({'user_id': request.user.id})

urlpatterns = patterns(
    '',
    (r'^api/mock/$', MockAPIView.as_view()),
    (r'^api/restricted/$', RestrictedAPIView.as_view()),
    (r'^api/auth/signin/$', SigninAPIView.as_view()),
)


class WebSocketRequestTestCase(TestCase):
    urls = 'blimp.utils.tests.websockets_tests'

    def test_authenticated_request_has_user(self):
        client = APIClient()

        data = {
            'username': 'jpueblo',
            'password': 'abc123'
        }

        user = User.objects.create_user(
            username=data['username'],
            email='jpueblo@example.com',
            password=data['password'],
            first_name='Juan',
            last_name='Pueblo'
        )

        response = client.post('/api/auth/signin/', data, format='json')

        data = {
            'url': '/api/restricted/',
            'token': 'abc',
            'method': 'post',
            'token': response.data['token']
        }

        message = json.dumps(data)
        wsrequest = WebSocketRequest(message)
        response = wsrequest.get_response()

        expected_response = {
            'user_id': user.id
        }

        self.assertEqual(response.data, expected_response)
