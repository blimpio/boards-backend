from django.conf.urls import patterns, url

from .views import SignupRequestCreateAPIView


api_urlpatterns = patterns(
    # Prefix
    '',

    url(r'auth/signup_request/$',
        SignupRequestCreateAPIView.as_view(), name='invite-request-create'),
)
