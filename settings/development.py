import os

from .base import *


# Application settings
DOMAIN = 'localhost:8000'
APPLICATION_URL = '{}://{}'.format(PROTOCOL, DOMAIN)

# Development Secret Key
SECRET_KEY = 'bb!onz3e2hc1l-192ug40g@ykf^3@e4rtl!t9(i)d7n#oeo^!r'

# Debug Mode
DEBUG = True
TEMPLATE_DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = []

# Development-only installed apps
INSTALLED_APPS += (
    'debug_toolbar',
)

# Middlewares
MIDDLEWARE_CLASSES = (
    'blimp_boards.utils.middleware.QueryCountDebugMiddleware',
) + MIDDLEWARE_CLASSES

# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'boards',
        'USER': os.getenv('USER'),
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Django REST framework
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'blimp_boards.users.authentication.JWTAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)


# Announce
ANNOUNCE_TEST_MODE = True

# boards-web
BOARDS_WEB_STATIC_URL = 'http://localhost:3333'
