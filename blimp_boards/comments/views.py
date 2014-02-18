from ..utils.viewsets import RetrieveUpdateDestroyViewSet
from .models import Comment
from .serializers import CommentSerializer
from .permissions import CommentPermission


class CommentViewSet(RetrieveUpdateDestroyViewSet):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission, )
