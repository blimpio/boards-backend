from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    # Prefix
    '',

    url(r'auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'auth/signup/$', views.SignupAPIView.as_view(), name='auth-signup'),
    url(r'auth/username/validate/$',
        views.ValidateUsernameAPIView.as_view(),
        name='auth-username-validate'),
)
