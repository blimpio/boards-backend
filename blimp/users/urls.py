from django.conf.urls import patterns, url

from . import views


api_urlpatterns = patterns(
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

    (r'signup/$', views.SignupValidateTokenHTMLView.as_view()),
    (r'reset_password/$', views.ResetPasswordHTMLView.as_view()),
)
