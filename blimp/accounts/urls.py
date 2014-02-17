from django.conf.urls import patterns, url

from . import views


api_urlpatterns = patterns(
    # Prefix
    '',

    url(r'auth/signup_domains/check/$',
        views.CheckSignupDomainAPIView.as_view(),
        name='auth-signup-domains-check'),

    url(r'auth/signup_domains/validate/$',
        views.ValidateSignupDomainsAPIView.as_view(),
        name='auth-signup-domains-validate'),

    url(r'accounts/$', views.AccountsForUserAPIView.as_view(),
        name='accounts_for_user')
)
