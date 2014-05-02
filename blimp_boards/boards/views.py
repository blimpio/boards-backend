from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from ..accounts.models import Account, AccountCollaborator
from ..utils.response import ErrorResponse
from ..utils.mixins import BulkCreateModelMixin
from ..utils.viewsets import (ModelViewSet, CreateListRetrieveViewSet,
                              RetrieveUpdateDestroyViewSet)
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
            user_boards = user.boards.select_related('account')

        public_criteria = [
            (action == 'retrieve'),
            (action == 'collaborators')
        ]

        if any(public_criteria):
            public_boards = Board.objects.filter(is_shared=True)

        if user_boards and public_boards:
            boards = user_boards | public_boards
        elif user_boards:
            boards = user_boards
        elif public_boards:
            boards = public_boards

        return boards

    def filter_queryset(self, queryset):
        user = self.request.user
        account_id = self.request.QUERY_PARAMS.get('account')

        if not account_id or not user.is_authenticated():
            return queryset

        try:
            Account.personals.get(pk=account_id)
            queryset = queryset.filter(boardcollaborator__user=user)
        except Account.DoesNotExist:
            pass

        return queryset

    def pre_delete(self, obj):
        """
        Set modified_by before deleting board.
        """
        obj.set_announce(False)

        obj.modified_by = self.request.user
        obj.save()

        obj.set_announce(True)

    @action(methods=['GET', 'POST'])
    def collaborators(self, request, pk=None):
        self.serializer_class = BoardCollaboratorSerializer

        board = self.get_object()
        user = self.request.user
        user_ids = []

        if request.method == 'POST':
            bulk = isinstance(request.DATA, list)
            context = self.get_serializer_context()

            context.update({
                'board': board
            })

            serializer_kwargs = {
                'data': request.DATA,
                'context': context
            }

            if bulk:
                serializer_kwargs.update({'many': True})

            serializer = self.serializer_class(**serializer_kwargs)

            if serializer.is_valid():
                self.object = serializer.save(force_insert=True)

                headers = self.get_success_headers(serializer.data)

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers)
            else:
                return ErrorResponse(serializer.errors)
        else:
            self.object_list = BoardCollaborator.objects.select_related(
                'user', 'invited_user').filter(board=board)

            for collaborator in self.object_list:
                user_ids.append(collaborator.user_id)

            if not user.is_authenticated() or user.id not in user_ids:
                self.serializer_class = BoardCollaboratorPublicSerializer

            serializer = self.get_serializer(self.object_list, many=True)

        return Response(serializer.data)


class BoardCollaboratorViewSet(BulkCreateModelMixin,
                               RetrieveUpdateDestroyViewSet):
    model = BoardCollaborator
    serializer_class = BoardCollaboratorSerializer
    permission_classes = (BoardCollaboratorPermission, )


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

        account_collaborator = get_object_or_404(
            AccountCollaborator.objects.select_related('account', 'user'),
            account__slug=account_slug,
            is_owner=True)

        if account_collaborator.account.type == Account.PERSONAL_ACCOUNT:
            boards = account_collaborator.user.boards

        board = get_object_or_404(boards, slug=board_slug)

        collaborator_users = []

        if board.is_shared:
            collaborator_users = BoardCollaborator.objects.filter(
                board_id=board.id, user__isnull=False
            ).values_list('user', flat=True)

        data = {
            'board': board,
            'collaborator_users': collaborator_users
        }

        return Response(data, template_name='index.html')
