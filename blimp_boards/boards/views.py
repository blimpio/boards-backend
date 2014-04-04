from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from ..utils.viewsets import ModelViewSet, CreateListRetrieveViewSet
from .models import Board, BoardCollaborator, BoardCollaboratorRequest
from .serializers import (BoardSerializer, BoardCollaboratorSerializer,
                          BoardCollaboratorPublicSerializer,
                          BoardCollaboratorRequestSerializer)
from .permissions import (BoardPermission, BoardCollaboratorPermission,
                          BoardCollaboratorRequestPermission)


class BoardViewSet(ModelViewSet):
    model = Board
    serializer_class = BoardSerializer
    permission_classes = (BoardPermission, )

    def get_queryset(self):
        user = self.request.user
        request_method = self.request.method.lower()
        action = self.action_map.get(request_method)

        boards = Board.objects.none()
        user_boards = None
        public_boards = None

        if user.is_authenticated():
            user_boards = user.boards

        if action == 'retrieve':
            public_boards = Board.objects.filter(is_shared=True)

        if user_boards and public_boards:
            boards = user_boards | public_boards
        elif user_boards:
            boards = user_boards
        elif public_boards:
            boards = public_boards

        return boards


class BoardCollaboratorViewSet(ModelViewSet):
    model = BoardCollaborator
    serializer_class = BoardCollaboratorSerializer
    permission_classes = (BoardCollaboratorPermission, )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('board', )

    def get_queryset(self):
        user = self.request.user
        request_method = self.request.method.lower()
        action = self.action_map.get(request_method)
        board = self.request.QUERY_PARAMS.get('board')

        collaborators = BoardCollaborator.objects.none()
        user_collaborators = None
        public_collaborators = None

        if user.is_authenticated():
            user_collaborators = BoardCollaborator.objects.filter(
                board__in=user.boards)

        if action == 'list' and board:
            public_collaborators = BoardCollaborator.objects.filter(
                board__is_shared=True)

        if user_collaborators and public_collaborators:
            collaborators = user_collaborators | public_collaborators
        elif user_collaborators:
            collaborators = user_collaborators
        elif public_collaborators:
            collaborators = public_collaborators

        return collaborators

    def get_serializer_class(self):
        user = self.request.user
        user_ids = []

        for collaborator in self.object_list:
            user_ids.append(collaborator.user_id)

        if not user.is_authenticated() or user.id not in user_ids:
            return BoardCollaboratorPublicSerializer

        return super(BoardCollaboratorViewSet, self).get_serializer_class()


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
        initialized_request = super(
            BoardCollaboratorRequestViewSet, self).initialize_request(
            request, *args, **kwargs)

        user = request.user
        request_method = request.method.lower()
        action = self.action_map.get(request_method)

        if not user.is_authenticated() and action == 'create':
            self.authentication_classes = ()
            self.permission_classes = ()

        return initialized_request

    @action(methods=['PUT'])
    def accept(self, request, pk=None):
        object = self.get_object()
        serializer = self.get_serializer(object)

        object.accept()

        return Response(serializer.data)

    @action(methods=['PUT'])
    def reject(self, request, pk=None):
        object = self.get_object()
        serializer = self.get_serializer(object)

        object.reject()

        return Response(serializer.data)


class BoardHTMLView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        account_slug = kwargs['account_slug']
        board_slug = kwargs['board_slug']

        board = get_object_or_404(
            Board.objects.values_list('id', 'account', 'is_shared'),
            account__slug=account_slug,
            slug=board_slug)

        data = {
            'board_id': board[0],
            'board_account_id': board[1],
            'board_is_shared': board[2],
        }

        return Response(data, template_name='index.html')
