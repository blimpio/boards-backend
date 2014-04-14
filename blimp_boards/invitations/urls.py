from django.conf.urls import patterns, url

from rest_framework.routers import DefaultRouter

from .views import (SignupRequestCreateAPIView, InvitedUserCreateAPIView,
                    InvitedUserViewSet)


router = DefaultRouter()

router.register(r'auth/invitations', InvitedUserViewSet)

api_urlpatterns = router.urls

api_urlpatterns += patterns(
    # Prefix
    '',

    url(r'auth/signup_request/$',
        SignupRequestCreateAPIView.as_view(), name='invite-request-create'),

    url(r'auth/signup_request/invite/$',
        InvitedUserCreateAPIView.as_view(), name='invited-user-create'),
)
