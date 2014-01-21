from django.conf.urls import patterns, url

from .views import SignupRequestCreateAPIView, ValidateSignupRequestAPIView


urlpatterns = patterns(
    # Prefix
    '',

    url(r'auth/signup_request/$',
        SignupRequestCreateAPIView.as_view(), name='invite-request-create'),

    url(r'auth/signup_request/validate/$',
        ValidateSignupRequestAPIView.as_view(),
        name='validate-invite-request'),
)
