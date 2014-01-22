from django.conf.urls import patterns, include, url
from django.contrib import admin

from blimp import router

admin.autodiscover()


urlpatterns = patterns(
    # Prefix
    '',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urlpatterns)),
)
