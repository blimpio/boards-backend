from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'boards', views.BoardViewSet)

api_urlpatterns = router.urls
