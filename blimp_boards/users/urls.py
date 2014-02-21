from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'users', views.UserViewSet)

api_urlpatterns = router.urls

api_urlpatterns += patterns(
    # Prefix
    '',

    url(r'auth/signin/$', views.SigninAPIView.as_view()),
    url(r'auth/signup/$', views.SignupAPIView.as_view()),
    url(r'auth/username/validate/$', views.ValidateUsernameAPIView.as_view()),

    (r'auth/forgot_password/$', views.ForgotPasswordAPIView.as_view()),
    (r'auth/reset_password/$', views.ResetPasswordAPIView.as_view()),
)

urlpatterns = patterns(
    # Prefix
    '',

    url(r'signin/$',
        views.SigninValidateTokenHTMLView.as_view(),
        name='auth-signin'),

    url(r'signup/$',
        views.SignupValidateTokenHTMLView.as_view(),
        name='auth-signup'),

    (r'reset_password/$', views.ResetPasswordHTMLView.as_view()),
)
