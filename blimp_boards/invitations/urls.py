from django.conf.urls import patterns, url

from .views import SignupRequestCreateAPIView, InvitedUserCreateAPIView


api_urlpatterns = patterns(
    # Prefix
    '',

    url(r'auth/signup_request/$',
        SignupRequestCreateAPIView.as_view(), name='invite-request-create'),

    url(r'auth/signup_request/invite/$',
        InvitedUserCreateAPIView.as_view(), name='invited-user-create'),
)
