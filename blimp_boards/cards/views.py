from django.shortcuts import redirect
from django.http import HttpResponse, Http404

from rest_framework import filters, status, permissions
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from ..utils.viewsets import ModelViewSet
from ..utils.response import ErrorResponse
from ..boards.views import BoardHTMLView
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
        request_method = self.request.method.lower()
        action = self.action_map.get(request_method)
        board = self.request.QUERY_PARAMS.get('board')

        cards = Card.objects.none()
        user_cards = None
        public_cards = None

        if user.is_authenticated():
            user_cards = user.cards.prefetch_related('cards')

        public_criteria = [
            (action == 'list' and board),
            (action == 'comments' and request_method == 'get'),
            (action == 'download' and request_method == 'get'),
            (action == 'original_thumbnail' and request_method == 'get'),
        ]

        if any(public_criteria):
            public_cards = Card.objects.prefetch_related(
                'cards').filter(board__is_shared=True)

        if user_cards and public_cards:
            cards = user_cards | public_cards
        elif user_cards:
            cards = user_cards
        elif public_cards:
            cards = public_cards

        return cards.select_related(
            'board', 'board__account', 'created_by', 'modified_by')

    def pre_delete(self, obj):
        """
        Set modified_by before deleting card.
        """
        obj.set_announce(False)

        obj.modified_by = self.request.user
        obj.save()

        obj.set_announce(True)

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
            comments = card.comments.select_related(
                'created_by', 'modified_by').all()

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

    @link()
    def original_thumbnail(self, request, pk=None):
        card = self.get_object()

        data = {
            'original_thumbnail_url': card.original_thumbnail_url
        }

        return Response(data)


class CardDownloadHTMLView(BoardHTMLView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        account_slug = kwargs['account_slug']
        board_slug = kwargs['board_slug']
        card_slug = kwargs['card_slug']

        token = request.QUERY_PARAMS.get('token')

        if not token:
            return super(CardDownloadHTMLView, self).get(
                request, *args, **kwargs)

        try:
            card = Card.objects.get_from_download_token(
                token, slug=card_slug, board__slug=board_slug,
                board__account__slug=account_slug)
        except Card.DoesNotExist:
            raise Http404

        if card.type == 'file':
            return redirect(card.file_download_url)

        if card.type == 'note':
            response = HttpResponse(card.content, content_type='text/plain')

            disposition = 'attachment; filename="{}"'.format(card.name)

            response['Content-Disposition'] = disposition
            response['Content-Length'] = len(card.content)

            return response

        raise Http404
