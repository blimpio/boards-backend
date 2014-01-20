from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    # Prefix
    '',

    url(r'', include('blimp.users.urls')),
    url(r'', include('blimp.invitations.urls')),
)
