from .development import *


DEBUG = False
TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DATABASES['default']['TEST_NAME'] = 'test_db'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
