import os

from .development import *


DEBUG = False
TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'testing_db.sqlite3'),
    }
}

WERCKER_POSTGRESQL_DATABASE = os.getenv('WERCKER_POSTGRESQL_DATABASE')

if WERCKER_POSTGRESQL_DATABASE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': WERCKER_POSTGRESQL_DATABASE,
            'USER': os.getenv('WERCKER_POSTGRESQL_USERNAME'),
            'PASSWORD': os.getenv('WERCKER_POSTGRESQL_PASSWORD'),
            'HOST': os.getenv('WERCKER_POSTGRESQL_HOST'),
            'PORT': os.getenv('WERCKER_POSTGRESQL_PORT'),
        }
    }

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
