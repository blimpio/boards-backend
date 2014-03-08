import dj_database_url

from . import env_var
from .base import *


# Application settings
DOMAIN = 'boards-backend-staging.herokuapp.com'
APPLICATION_URL = '{}://{}'.format(HTTP_PROTOCOL, DOMAIN)

# Debug Mode
DEBUG = env_var('DEBUG', False)
TEMPLATE_DEBUG = env_var('TEMPLATE_DEBUG', False)

# Installed Apps
INSTALLED_APPS += (
    'djrill',
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': dj_database_url.config()
}

# Email settings
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
MANDRILL_API_KEY = os.getenv('MANDRILL_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


# Static asset settings
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Django REST framework
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'blimp_boards.users.authentication.JWTAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)


# boards-web
BOARDS_WEB_STATIC_URL = os.getenv('BOARDS_WEB_STATIC_URL')
BOARDS_WEB_CLIENT_VERSION = os.getenv('BOARDS_WEB_CLIENT_VERSION')


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
