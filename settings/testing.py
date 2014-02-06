from .development import *


DEBUG = False
TEMPLATE_DEBUG = False

DEBUG_TOOLBAR_PATCH_SETTINGS = False

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
