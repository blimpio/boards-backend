import os
import datetime

from configurations import Configuration, values


class Common(Configuration):

    # Application settings
    ENVIRONMENT = values.Value(environ_prefix=None)
    HTTP_PROTOCOL = 'https' if ENVIRONMENT != 'DEVELOPMENT' else 'http'

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    TEMPLATE_DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sitemaps',

        'south',
        'rest_framework',
        'django_extensions',

        'blimp_boards.utils',
        'blimp_boards.users',
        'blimp_boards.accounts',
        'blimp_boards.invitations',
        'blimp_boards.boards',
        'blimp_boards.cards',
        'blimp_boards.comments',
        'blimp_boards.notifications',
    )

    # Middlewares
    MIDDLEWARE_CLASSES = (
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'blimp_boards.urls'

    WSGI_APPLICATION = 'blimp_boards.wsgi.application'

    # Database
    DATABASES = values.DatabaseURLValue(
        'postgres://{}@localhost/boards'.format(
            os.getenv('USER')), environ=True)

    # Internationalization
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'

    # Templates
    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
        'blimp_boards.utils.context_processors.app_settings',
    )

    # Custom User Model
    AUTH_USER_MODEL = 'users.User'

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'blimp_boards.users.backends.EmailBackend',
    )

    # Logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            }
        }
    }

    # Cache
    SITEMAP_CACHE_TIMEOUT = 60 * 60 * 24

    # Django REST framework
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'blimp_boards.users.authentication.JWTAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'EXCEPTION_HANDLER':
        'blimp_boards.utils.exceptions.custom_exception_handler',
    }

    JWT_AUTH = {
        'JWT_PAYLOAD_HANDLER':
        'blimp_boafrds.utils.jwt_handlers.jwt_payload_handler',

        'JWT_EXPIRATION_DELTA': datetime.timedelta(days=90)
    }

    # Announce
    ANNOUNCE_TEST_MODE = values.BooleanValue(environ_prefix=None, default=True)

    # AWS
    AWS_ACCESS_KEY_ID = values.Value(environ_prefix=None)
    AWS_SECRET_ACCESS_KEY = values.Value(environ_prefix=None)
    AWS_STORAGE_BUCKET_NAME = values.Value(environ_prefix=None)
    AWS_SIGNATURE_EXPIRES_IN = 60 * 60 * 3

    # boards-web
    BOARDS_WEB_STATIC_URL = values.Value(environ_prefix=None)
    BOARDS_WEB_CLIENT_VERSION = values.Value(environ_prefix=None)

    # blimp-previews
    BLIMP_PREVIEWS_ACCOUNT_ID = values.Value(environ_prefix=None)
    BLIMP_PREVIEWS_SECRET_KEY = values.Value(environ_prefix=None)
    BLIMP_PREVIEWS_URL = values.Value(environ_prefix=None)

    # boards-sockets
    BOARDS_SOCKETS_URL = values.Value(environ_prefix=None)
    BOARDS_SOCKETS_REDIS_URL = values.Value(environ_prefix=None)


class Development(Common):
    """
    The in-development settings and the default configuration.
    """

    # Application settings
    DOMAIN = 'localhost:8000'
    APPLICATION_URL = '{}://{}'.format(Common.HTTP_PROTOCOL, DOMAIN)

    # Debug Mode
    DEBUG = True
    TEMPLATE_DEBUG = True

    # Allow all hosts in development
    ALLOWED_HOSTS = []

    # Development-only installed apps
    Common.INSTALLED_APPS += (
        'debug_toolbar',
    )

    # Middlewares
    MIDDLEWARE_CLASSES = (
        'blimp_boards.utils.middleware.QueryCountDebugMiddleware',
    ) + Common.MIDDLEWARE_CLASSES

    # Email settings
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Django REST framework
    Common.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

    # boards-web
    BOARDS_WEB_STATIC_URL = 'http://localhost:3333/'


class Testing(Development):
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
                'NAME': os.path.join(Common.BASE_DIR, 'testing_db.sqlite3'),
            }
        }

    # Password Hashers
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    # Email Settings
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

    # South
    SOUTH_TESTS_MIGRATE = False

    # Debug Toolbar
    DEBUG_TOOLBAR_PATCH_SETTINGS = False


class Staging(Common):
    """
    The in-staging settings.
    """
    # Application settings
    DOMAIN = 'boards-backend-staging.herokuapp.com'
    APPLICATION_URL = '{}://{}'.format(Common.HTTP_PROTOCOL, DOMAIN)

    # Installed Apps
    Common.INSTALLED_APPS += (
        'djrill',
        'djangosecure',
    )

    # django-secure
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_FRAME_DENY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    # Email settings
    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
    MANDRILL_API_KEY = os.getenv('MANDRILL_API_KEY')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

    # Static asset settings
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(Common.BASE_DIR, 'static'),
    )

    # Django REST framework
    Common.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
