from django.conf.urls import patterns, include
from django.views.generic import TemplateView
from django.contrib import admin


admin.autodiscover()

index_view = TemplateView.as_view(template_name='index.html')

urlpatterns = patterns(
    # Prefix
    '',

    (r'^admin/', include(admin.site.urls)),

    (r'^api/', include('blimp_boards.router')),

    (r'', include('blimp_boards.users.urls')),

    (r'', include('blimp_boards.boards.urls')),

    # Catch all URL
    (r'^($|.*/$)', index_view),
)
