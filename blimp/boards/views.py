from rest_framework import viewsets

from .models import Board
from .serializers import BoardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    model = Board
    serializer_class = BoardSerializer
