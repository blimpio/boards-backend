import json

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.test.client import RequestFactory
from rest_framework import permissions
from rest_framework.compat import patterns
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.test import APIClient

from blimp.users.models import User
from blimp.users.views import SigninAPIView
from blimp.users.authentication import JWTAuthentication
from ..websockets import WebSocketsRequest


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


class WebSocketsRequestTestCase(TestCase):
    urls = 'blimp.utils.tests.websockets_tests'

    def test_initilize_needs_message(self):
        with self.assertRaises(TypeError):
            WebSocketsRequest()

    def test_initilize_with_message(self):
        message = json.dumps({'url': '/api/mock/'})
        request = WebSocketsRequest(message)

        self.assertEqual(request.message, message)

    def test_get_url_should_return_url(self):
        message = json.dumps({'url': '/api/mock/'})
        request = WebSocketsRequest(message)
        request.is_valid_message()

        self.assertEqual(request.get_url(), '/api/mock/')

    def test_get_url_should_return_none(self):
        message = json.dumps({})
        request = WebSocketsRequest(message)
        request.is_valid_message()

        self.assertEqual(request.get_url(), None)

    def test_get_method_should_return_lower_method(self):
        message = json.dumps({'method': 'POST'})
        request = WebSocketsRequest(message)
        request.is_valid_message()

        self.assertEqual(request.get_method(), 'post')

    def test_get_method_should_return_default_lower_method(self):
        message = json.dumps({})
        request = WebSocketsRequest(message)
        request.is_valid_message()

        self.assertEqual(request.get_method(), 'get')

    def test_get_data_should_return_data(self):
        data = {
            'data': {
                'good': 1
            }
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)
        request.is_valid_message()

        self.assertEqual(request.get_data(), data['data'])

    def test_get_data_should_return_default_empty_dict(self):
        message = json.dumps({})
        request = WebSocketsRequest(message)
        request.is_valid_message()

        self.assertEqual(request.get_data(), {})

    def test_get_token_should_return_token(self):
        data = {
            'token': 'abc123'
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)
        request.is_valid_message()

        self.assertEqual(request.get_token(), data['token'])

    def test_get_token_should_return_none(self):
        message = json.dumps({})
        request = WebSocketsRequest(message)
        request.is_valid_message()

        self.assertEqual(request.get_token(), None)

    def test_set_error_should_set_error_message_and_code(self):
        message = json.dumps({})
        request = WebSocketsRequest(message)
        request.set_error('Error message', 123)

        expected_error = {
            'error': 'Error message',
            'status_code': 123
        }

        self.assertEqual(request.error, expected_error)

    def test_is_valid_should_return_true_for_valid_message(self):
        data = {
            'url': '/api/mock/',
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)

        self.assertTrue(request.is_valid())

    def test_is_valid_should_return_false_for_invalid_message(self):
        data = {
            'url': '/api/nonexistent/',
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)

        self.assertFalse(request.is_valid())

    def test_is_valid_message_should_return_true_for_valid_message(self):
        data = {
            'url': '/api/mock/',
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)

        self.assertTrue(request.is_valid_message())

    def test_is_valid_message_should_return_false_for_invalid_message(self):
        request = WebSocketsRequest('errormsg')

        self.assertFalse(request.is_valid_message())

    def test_is_valid_message_should_set_error_on_invalid_message(self):
        request = WebSocketsRequest('{')
        request.is_valid_message()

        expected_error = {
            'status_code': 400,
            'error': 'Invalid formatted message.'
        }

        self.assertEqual(request.error, expected_error)

    def test_get_url_resolver_match_should_return_resolver_match(self):
        data = {
            'url': '/api/mock/',
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)
        expected_match = resolve('/api/mock/')
        request.is_valid()
        resolver_match = request.get_url_resolver_match()

        self.assertEqual(resolver_match.url_name, expected_match.url_name)

    def test_get_url_resolver_match_should_set_error_when_no_match(self):
        data = {
            'url': '/api/nonexistent/',
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)
        request.is_valid()
        request.get_url_resolver_match()

        expected_error = {
            'error': 'Resource not found.',
            'status_code': 404
        }

        self.assertEqual(request.error, expected_error)

    def test_get_factory_should_return_request_factory(self):
        data = {
            'url': '/api/mock/',
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)
        request.is_valid()

        factory = request.get_factory()

        self.assertTrue(isinstance(factory, RequestFactory))

    def test_get_factory_should_includ_auth_header_if_token_is_set(self):
        data = {
            'url': '/api/mock/',
            'token': 'abc'
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)
        request.is_valid()

        factory = request.get_factory()

        expected_headers = {
            'HTTP_AUTHORIZATION': 'JWT abc'
        }

        self.assertEqual(factory.defaults, expected_headers)

    def test_get_request_should_return_request_factory_request(self):
        data = {
            'url': '/api/mock/',
            'token': 'abc'
        }

        message = json.dumps(data)
        request = WebSocketsRequest(message)
        request.is_valid()
        factory = request.get_factory()
        request = request.get_request(factory)

        self.assertEqual(request.path, '/api/mock/')

    def test_get_view_should_return_view_function(self):
        data = {
            'url': '/api/mock/',
            'token': 'abc'
        }

        message = json.dumps(data)
        wsrequest = WebSocketsRequest(message)
        wsrequest.is_valid()
        resolver_match = wsrequest.get_url_resolver_match()
        factory = wsrequest.get_factory()
        request = wsrequest.get_request(factory)
        view = wsrequest.get_view(resolver_match, request)

        self.assertEqual(view.status_code, 200)

    def test_get_response_should_return_view_data(self):
        data = {
            'url': '/api/mock/',
            'token': 'abc'
        }

        message = json.dumps(data)
        wsrequest = WebSocketsRequest(message)
        response = wsrequest.get_response()

        expected_response = {
            'foo': ['bar', 'baz']
        }

        self.assertEqual(response, expected_response)

    def test_get_response_should_return_error(self):
        data = {
            'url': '/api/mock/',
            'token': 'abc',
            'method': 'put'
        }

        message = json.dumps(data)
        wsrequest = WebSocketsRequest(message)
        response = wsrequest.get_response()

        expected_response = {
            'error': "Method 'PUT' not allowed.",
            'status_code': 405
        }

        self.assertEqual(response, expected_response)

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
        wsrequest = WebSocketsRequest(message)
        response = wsrequest.get_response()

        expected_response = {
            'user_id': user.id
        }

        self.assertEqual(response, expected_response)
