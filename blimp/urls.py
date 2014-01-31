from django.conf.urls import patterns, include
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    # Prefix
    '',

    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('blimp.router')),

    (r'', include('blimp.users.urls')),

    # Catch all URL
    (r'^.*/$', TemplateView.as_view(template_name='index.html'))
)
