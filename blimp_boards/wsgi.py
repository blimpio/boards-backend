"""
WSGI config for blimp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import newrelic.agent
import dotenv


dotenv.read_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

ENVIRONMENT = os.getenv('ENVIRONMENT')
NEW_RELIC_LICENSE_KEY = os.getenv('NEW_RELIC_LICENSE_KEY')

if ENVIRONMENT == 'STAGING':
    settings = 'staging'
elif ENVIRONMENT == 'PRODUCTION':
    settings = 'production'
else:
    settings = 'development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blimp_boards.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', settings.title())

from configurations.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())

if NEW_RELIC_LICENSE_KEY:
    application = newrelic.agent.WSGIApplicationWrapper(application)
