from django.conf.urls import patterns

from .views import SignS3FileUploadAPIView, FilePreviewsWebhook

api_urlpatterns = patterns(
    # Prefix
    '',

    (r'files/uploads/sign/$', SignS3FileUploadAPIView.as_view()),
    (r'files/previews/webhook/$', FilePreviewsWebhook.as_view()),
)
