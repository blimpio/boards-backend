import os

from .development import *


DEBUG = False
TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

DEBUG_TOOLBAR_PATCH_SETTINGS = False

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('WERCKER_POSTGRESQL_DATABASE', 'boards'),
        'USER': os.getenv('WERCKER_POSTGRESQL_USERNAME', os.getenv('USER')),
        'PASSWORD': os.getenv('WERCKER_POSTGRESQL_PASSWORD', ''),
        'HOST': os.getenv('WERCKER_POSTGRESQL_HOST', 'localhost'),
        'PORT': os.getenv('WERCKER_POSTGRESQL_PORT', ''),
    }
}
