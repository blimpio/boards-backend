import webbrowser
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class BrowsableEmailBackend(BaseEmailBackend):
    """
    An email backend that opens HTML parts of emails sent
    in a local web browser, for testing during development.

    Adapted from https://github.com/stephenmcd/django-email-extras
    """
    def send_messages(self, email_messages):
        # Should never be used in production.
        if not settings.DEBUG:
            return

        for message in email_messages:
            alternatives = getattr(message, 'alternatives', [])

            for body, content_type in alternatives:
                if content_type == 'text/html':
                    self.open(body.encode('utf-8'))

    def open(self, body):
        temp = NamedTemporaryFile(delete=False)
        temp.write(body)
        temp.close()

        webbrowser.open('file://{}'.format(temp.name))
