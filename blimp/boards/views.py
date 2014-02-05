from rest_framework import viewsets, filters

from .models import Board
from .serializers import BoardSerializer
from .permissions import BoardPermission


class BoardViewSet(viewsets.ModelViewSet):
    model = Board
    serializer_class = BoardSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (BoardPermission, )

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(account__in=user.accounts)
