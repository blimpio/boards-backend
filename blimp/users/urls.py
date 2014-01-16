from django.conf.urls import patterns, url

from blimp.users import views


urlpatterns = patterns(
    # Prefix
    '',

    url(r'auth/login/', 'rest_framework_jwt.views.obtain_jwt_token'),
)
