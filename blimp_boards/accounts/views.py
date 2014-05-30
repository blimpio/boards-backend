import operator

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import link
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from ..boards.models import Board
from ..cards.models import Card
from ..notifications.pagination import PaginatedNotificationSerializer
from ..notifications.models import Notification
from ..utils.response import ErrorResponse
from ..utils.viewsets import ListRetrieveUpdateViewSet
from .models import Account
from .permissions import AccountPermission
from .serializers import (ValidateSignupDomainsSerializer,
                          AccountSerializer, CheckSignupDomainSerializer)


class ValidateSignupDomainsAPIView(generics.CreateAPIView):
    """
    Validate a given list of signup domains.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ValidateSignupDomainsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


class CheckSignupDomainAPIView(generics.CreateAPIView):
    """
    Check if an account has a given domain name as a signup domain.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CheckSignupDomainSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


class AccountViewSet(ListRetrieveUpdateViewSet):
    """
    Get a list of accounts for the user in the request
    """
    model = Account
    serializer_class = AccountSerializer
    permission_classes = (AccountPermission, )

    def get_queryset(self):
        user = self.request.user
        request_method = self.request.method.lower()
        action = self.action_map.get(request_method)

        accounts = Account.objects.none()
        user_accounts = None
        public_accounts = None

        if user.is_authenticated():
            user_accounts = user.accounts.distinct()

        if action == 'retrieve':
            public_accounts = Account.objects.filter(
                board__is_shared=True).distinct()

        if user_accounts and public_accounts:
            accounts = user_accounts | public_accounts
        elif user_accounts:
            accounts = user_accounts
        elif public_accounts:
            accounts = public_accounts

        return accounts.select_related('created_by', 'modified_by')

    @link(paginate_by=10)
    def activity(self, request, pk=None):
        user = self.request.user
        account = self.get_object()

        if account.type == 'personal':
            boards = user.boards
        else:
            boards = account.boards

        board_id = request.QUERY_PARAMS.get('board')

        if board_id:
            boards = boards.filter(pk=board_id)

        board_ids = boards.values_list('id', flat=True)
        card_ids = Card.objects.filter(board__pk__in=board_ids)

        board_type = ContentType.objects.get_for_model(Board)
        card_type = ContentType.objects.get_for_model(Card)

        # Get notifications for account's boards.
        notifications = Notification.objects.filter(
            (Q(target_content_type=board_type) &
             Q(target_object_id__in=board_ids)) |
            (Q(target_content_type=card_type) &
             Q(target_object_id__in=card_ids))
        ).order_by().distinct(
            'target_content_type', 'target_object_id',
            'action_object_content_type', 'action_object_object_id',
            'actor_content_type', 'actor_object_id',
            'verb', 'description'
        )

        sorted_notifications = sorted(
            notifications,
            key=operator.attrgetter('date_created'),
            reverse=True
        )

        page = self.paginate_queryset(sorted_notifications)

        context = {
            'request': request
        }

        serializer = PaginatedNotificationSerializer(page, context=context)

        return Response(serializer.data)


class AccountHTMLView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request, *args, **kwargs):
        account_slug = kwargs['account_slug']

        get_object_or_404(Account, slug=account_slug)

        return Response(template_name='index.html')
