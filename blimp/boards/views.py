from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action

from ..utils.viewsets import ModelViewSet, CreateListRetrieveViewSet
from .models import Board, BoardCollaboratorRequest
from .serializers import BoardSerializer, BoardCollaboratorRequestSerializer
from .permissions import BoardPermission, BoardCollaboratorRequestPermission


class BoardViewSet(ModelViewSet):
    model = Board
    serializer_class = BoardSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (BoardPermission, )

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(account__in=user.accounts)


class BoardCollaboratorRequestViewSet(CreateListRetrieveViewSet):
    model = BoardCollaboratorRequest
    serializer_class = BoardCollaboratorRequestSerializer
    permission_classes = (BoardCollaboratorRequestPermission, )

    def get_queryset(self):
        user = self.request.user
        return BoardCollaboratorRequest.objects.filter(
            board__account__in=user.accounts)

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication and permissions for `create` action.
        """
        request_method = request.method.lower()

        if self.action_map.get(request_method) == 'create':
            self.authentication_classes = ()
            self.permission_classes = ()

        return super(BoardCollaboratorRequestViewSet,
                     self).initialize_request(request, *args, **kwargs)

    @action()
    def accept(self, request, pk=None):
        object = self.get_object()
        serializer = self.get_serializer(object)

        object.accept()

        return Response(serializer.data)

    @action()
    def reject(self, request, pk=None):
        object = self.get_object()
        serializer = self.get_serializer(object)

        object.reject()

        return Response(serializer.data)

    def post_save(self, obj, created=False):
        if created:
            obj.notify_account_owner()
