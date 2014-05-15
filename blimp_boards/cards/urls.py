from django.conf.urls import patterns, url

from rest_framework.routers import DefaultRouter

from ..boards.views import BoardHTMLView
from . import views


router = DefaultRouter()

router.register(r'cards', views.CardViewSet)

api_urlpatterns = router.urls

urlpatterns = patterns(
    # Prefix
    '',

    url(r'^$',
        BoardHTMLView.as_view(), name='card_detail'),

    url(r'^download/$',
        views.CardDownloadHTMLView.as_view(), name='card_download'),
)
