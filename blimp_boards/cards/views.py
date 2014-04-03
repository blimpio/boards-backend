from rest_framework import filters, status, permissions
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from ..utils.viewsets import ModelViewSet
from ..utils.response import ErrorResponse
from .models import Card
from .serializers import CardSerializer, StackSerializer, CardCommentSerializer
from .permissions import CardPermission
from .filters import CardFilter


class CardViewSet(ModelViewSet):
    model = Card
    serializer_class = CardSerializer
    permission_classes = (CardPermission, )
    filter_class = CardFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            data = self.request.DATA

            if data and data['type'] == 'stack':
                return StackSerializer

        return super(CardViewSet, self).get_serializer_class()

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated():
            user = self.request.user
            cards = user.cards
        else:
            cards = Card.objects.filter(board__is_shared=True)

        return cards.prefetch_related('cards')

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication for `list` action with board
        filter query param.
        """
        request_method = request.method.lower()
        board = request.GET.get('board')

        if self.action_map.get(request_method) == 'list' and board:
            self.authentication_classes = ()

        return super(CardViewSet, self).initialize_request(
            request, *args, **kwargs)

    @action(methods=['GET', 'POST'], serializer_class=CardCommentSerializer)
    def comments(self, request, pk=None):
        card = self.get_object()

        if request.method == 'POST':
            context = self.get_serializer_context()

            context.update({
                'content_object': card
            })

            serializer = CardCommentSerializer(
                data=request.DATA, context=context)

            if serializer.is_valid():
                serializer.save()

                headers = self.get_success_headers(serializer.data)

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers)
            else:
                return ErrorResponse(serializer.errors)
        else:
            comments = card.comments.all()
            serializer = CardCommentSerializer(comments, many=True)

        return Response(serializer.data)

    @action(methods=['PUT'])
    def unstack(self, request, pk=None):
        card = self.get_object()

        if card.type != 'stack':
            raise ParseError

        card.cards.clear()

        card.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @link()
    def download(self, request, pk=None):
        card = self.get_object()

        data = {
            'download_url': card.download_url
        }

        return Response(data)
