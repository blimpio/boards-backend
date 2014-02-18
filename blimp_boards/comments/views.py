from ..utils.viewsets import RetrieveUpdateDestroyViewSet
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(RetrieveUpdateDestroyViewSet):
    model = Comment
    serializer_class = CommentSerializer
