from rest_framework.pagination import PaginationSerializer

from .serializers import NotificationSerializer


class PaginatedNotificationSerializer(PaginationSerializer):
    """
    Serializes page objects of notification querysets.
    """
    class Meta:
        object_serializer_class = NotificationSerializer
