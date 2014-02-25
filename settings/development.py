import os

from . import env_var
from .base import *


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

# Middleware Classes
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


DEBUG_TOOLBAR_PATCH_SETTINGS = env_var('DEBUG_TOOLBAR_PATCH_SETTINGS', True)

# Django REST framework
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'blimp_boards.users.authentication.JWTAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'blimp_boards.utils.jwt_handlers.jwt_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=90)
}

# CORS Headers
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8000',
    'localhost:8000',
    'localhost:3333',
)

# Announce
ANNOUNCE_TEST_MODE = False


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     }
# }
