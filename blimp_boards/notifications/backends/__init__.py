import sys

from django.conf import settings
from django.core import exceptions


default_backends = [
    ('email', 'blimp_boards.notifications.backends.email.EmailBackend'),
    ('notification', 'blimp_boards.notifications.backends.notification.NotificationBackend'),
]


def load_backends():
    backends = []
    configured_backends = getattr(
        settings, 'NOTIFICATION_BACKENDS', default_backends)

    for label, backend_path in configured_backends:
        dot = backend_path.rindex('.')
        backend_mod, backend_class = backend_path[:dot], backend_path[dot + 1:]

        try:
            # import the module and get the module from sys.modules
            __import__(backend_mod)
            mod = sys.modules[backend_mod]
        except ImportError as e:
            msg = 'Error importing notification backend {}: \'{}\''
            raise exceptions.ImproperlyConfigured(msg.format(backend_mod, e))

        # add the backend label and an instantiated backend class to the
        # backends list.
        backend_instance = getattr(mod, backend_class)(label)
        backends.append(((label, label.title()), backend_instance))

    return dict(backends)


def load_media_defaults(backends):
    media = []
    defaults = {}

    for key, backend in backends.items():
        media.append(key)

    return media, defaults
