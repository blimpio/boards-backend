from django.http import HttpResponse
from django.test import TestCase

from rest_framework import permissions, status
from rest_framework.compat import patterns
from rest_framework.test import APIClient
from rest_framework.views import APIView

from ..models import User
from ..authentication import JWTAuthentication


class MockView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return HttpResponse({'a': 1, 'b': 2, 'c': 3})


urlpatterns = patterns(
    '',
    (r'^jwt/$', MockView.as_view()),
)


class JSONWebTokenAuthenticationTests(TestCase):
    urls = 'blimp_boards.users.tests.test_authentication'

    def setUp(self):
        self.csrf_client = APIClient(enforce_csrf_checks=True)
        self.username = 'jpueblo'
        self.email = 'jpueblo@example.com'
        self.user = User.objects.create_user(self.username, self.email)

    def test_token_version_change_should_invalidate_token(self):
        """
        Tests that a token is invalidated if User.token_version changes.
        """
        token = self.user.token

        self.user.reset_token_version()
        self.user.save()

        auth = 'JWT {0}'.format(token)
        response = self.csrf_client.post(
            '/jwt/', {'example': 'example'},
            HTTP_AUTHORIZATION=auth, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
