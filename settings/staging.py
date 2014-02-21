import dj_database_url

from . import env_var
from .base import *


# Debug Mode
DEBUG = env_var('DEBUG', False)
TEMPLATE_DEBUG = env_var('TEMPLATE_DEBUG', False)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': dj_database_url.config()
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Static asset settings
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'


# Debug Toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = env_var('DEBUG_TOOLBAR_PATCH_SETTINGS', True)


# Django REST framework
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'blimp_boards.users.authentication.JWTAuthentication',
)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)

JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'blimp_boards.utils.jwt_handlers.jwt_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=90)
}


# CORS Headers
CORS_ORIGIN_ALLOW_ALL = True


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}
