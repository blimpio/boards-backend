from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    # Prefix
    '',

    url(r'auth/signin/$', views.SigninAPIView.as_view(), name='auth-signin'),
    url(r'auth/signup/$', views.SignupAPIView.as_view(), name='auth-signup'),
    url(r'auth/username/validate/$',
        views.ValidateUsernameAPIView.as_view(),
        name='auth-username-validate'),
)
