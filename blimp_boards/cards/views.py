from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..utils.viewsets import ModelViewSet
from .models import Card
from .serializers import CardSerializer, CardCommentSerializer
from .permissions import CardPermission


class CardViewSet(ModelViewSet):
    model = Card
    serializer_class = CardSerializer
    permission_classes = (CardPermission, )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('board', )

    def get_queryset(self):
        user = self.request.user
        return user.cards.prefetch_related('cards')

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
                return Response({
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            comments = card.comments.all()
            serializer = CardCommentSerializer(comments, many=True)

        return Response(serializer.data)
