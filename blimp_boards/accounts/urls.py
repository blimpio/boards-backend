from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'accounts', views.AccountViewSet)

api_urlpatterns = router.urls

api_urlpatterns += patterns(
    # Prefix
    '',

    url(r'auth/signup_domains/check/$',
        views.CheckSignupDomainAPIView.as_view(),
        name='auth-signup-domains-check'),

    url(r'auth/signup_domains/validate/$',
        views.ValidateSignupDomainsAPIView.as_view(),
        name='auth-signup-domains-validate'),
)
