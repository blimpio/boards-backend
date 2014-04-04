from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import link
from rest_framework.pagination import PaginationSerializer

from ..boards.models import Board
from ..notifications.serializers import NotificationSerializer
from ..notifications.pagination import PaginatedNotificationSerializer
from ..notifications.models import Notification
from ..utils.response import ErrorResponse
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


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
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

        user_accounts = None
        public_accounts = None

        if user.is_authenticated():
            user_accounts = user.accounts.distinct()

        if action == 'retrieve':
            public_accounts = Account.objects.filter(
                board__is_shared=True).distinct()

        if user_accounts and public_accounts:
            return user_accounts | public_accounts
        elif user_accounts:
            return user_accounts
        elif public_accounts:
            return public_accounts

        return []

    @link(paginate_by=10)
    def activity(self, request, pk=None):
        account = self.get_object()
        boards = account.boards

        board_id = request.QUERY_PARAMS.get('board')

        if board_id:
            boards = boards.filter(pk=board_id)

        board_ids = boards.values_list('id', flat=True)

        board_type = ContentType.objects.get_for_model(Board)

        # Get notifications for account's boards.
        notifications = Notification.objects.filter(
            target_content_type=board_type,
            target_object_id__in=board_ids)

        page = self.paginate_queryset(notifications)

        context = {
            'request': request
        }

        serializer = PaginatedNotificationSerializer(page, context=context)

        return Response(serializer.data)
