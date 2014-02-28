from django.conf.urls import patterns

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'boards/collaborators/requests',
                views.BoardCollaboratorRequestViewSet)
router.register(r'boards/collaborators', views.BoardCollaboratorViewSet)
router.register(r'boards', views.BoardViewSet)

api_urlpatterns = router.urls


urlpatterns = patterns(
    # Prefix
    '',

    (r'^(?P<account_slug>[-\w]+)/(?P<board_slug>[-\w]+)/',
     views.BoardHTMLView.as_view())
)
