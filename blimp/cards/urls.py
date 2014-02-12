from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'cards', views.CardViewSet)

api_urlpatterns = router.urls
