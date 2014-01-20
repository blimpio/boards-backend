from django.conf.urls import patterns, url

from .views import InviteRequestCreateAPIView, ValidateInviteRequestAPIView


urlpatterns = patterns(
    # Prefix
    '',

    url(r'auth/invite_request/$',
        InviteRequestCreateAPIView.as_view(), name='invite-request-create'),

    url(r'auth/invite_request/validate/$',
        ValidateInviteRequestAPIView.as_view(),
        name='validate-invite-request'),
)
