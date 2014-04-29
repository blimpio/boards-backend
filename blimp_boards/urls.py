from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from django.contrib import admin

from .utils.sitemap import sitemaps


admin.autodiscover()

index_view = TemplateView.as_view(template_name='index.html')

urlpatterns = patterns(
    # Prefix
    '',

    (r'^admin/', include(admin.site.urls)),

    (r'^api/', include('blimp_boards.router')),

    (r'', include('blimp_boards.users.urls')),

    (r'', include('blimp_boards.accounts.urls')),

    (r'', include('blimp_boards.boards.urls')),

    # Catch all URL
    (r'^($|.*/$)', index_view),

    # Sitemap
    url(r'^sitemap\.xml$',
        cache_page(settings.SITEMAP_CACHE_TIMEOUT)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps}),
)
