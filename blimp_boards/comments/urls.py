from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'comments', views.CommentViewSet)

api_urlpatterns = router.urls
