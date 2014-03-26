from django.conf.urls import patterns, url

from . import views

api_urlpatterns = patterns(
    # Prefix
    '',

    (r'auth/signin/$', views.SigninAPIView.as_view()),
    (r'auth/signup/$', views.SignupAPIView.as_view()),
    (r'auth/username/validate/$', views.ValidateUsernameAPIView.as_view()),

    (r'auth/forgot_password/$', views.ForgotPasswordAPIView.as_view()),
    (r'auth/reset_password/$', views.ResetPasswordAPIView.as_view()),

    (r'users/me/$', views.UserSettingsAPIView.as_view()),
    (r'users/me/change_password/$', views.ChangePasswordAPIView.as_view()),
)

urlpatterns = patterns(
    # Prefix
    '',

    url(r'signin/$',
        views.SigninValidateTokenHTMLView.as_view(),
        name='auth-signin'),

    url(r'signup/',
        views.SignupValidateTokenHTMLView.as_view(),
        name='auth-signup'),

    url(r'reset_password/$',
        views.ResetPasswordHTMLView.as_view(),
        name='auth-reset-password'),
)
