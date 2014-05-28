from django.contrib.contenttypes.models import ContentType

from ..utils.viewsets import RetrieveUpdateDestroyViewSet
from ..cards.models import Card
from .models import Comment
from .serializers import CommentSerializer
from .permissions import CommentPermission


class CommentViewSet(RetrieveUpdateDestroyViewSet):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission, )

    def pre_delete(self, obj):
        card_type = ContentType.objects.get_for_model(Card)

        if obj.content_type == card_type:
            obj.content_object.update_comments_count(count=-1)
