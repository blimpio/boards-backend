from rest_framework import filters

from ..utils.viewsets import ModelViewSet
from .models import Card
from .serializers import CardSerializer
from .permissions import CardPermission


class CardViewSet(ModelViewSet):
    model = Card
    serializer_class = CardSerializer
    permission_classes = (CardPermission, )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('board', )

    def get_queryset(self):
        user = self.request.user
        return Card.objects.filter(board__in=user.boards)
