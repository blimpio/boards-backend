import os

from .development import *


# Debug Mode
DEBUG = False
TEMPLATE_DEBUG = False

# Database Settings
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
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'testing_db.sqlite3'),
        }
    }


# Password Hashers
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


# Announce
ANNOUNCE_TEST_MODE = True

# South
SOUTH_TESTS_MIGRATE = False

# Debug Toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
