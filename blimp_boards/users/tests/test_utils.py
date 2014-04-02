from ...utils.tests import BaseTestCase
from ..utils import get_gravatar_url


class UtilsTestCase(BaseTestCase):
    def test_get_gravatar_url_should_return_gravatar_url_for_email(self):
        """
        Tests that get_gravatar_url should return a Gravatar URL
        for a given email.
        """
        gravatar_url = get_gravatar_url('jpueblo@example.com')
        expected_url = ("https://secure.gravatar.com/"
                        "avatar/8964266c2b9182617beb65e50fc00031")

        self.assertEqual(gravatar_url, expected_url)
