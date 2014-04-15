from django.http import Http404

from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from ..utils.response import ErrorResponse
from ..utils.mixins import BulkCreateModelMixin
from .models import SignupRequest, InvitedUser
from .serializers import (SignupRequestSerializer, InvitedUserSerializer,
                          InvitedUserFullSerializer)


class SignupRequestCreateAPIView(BulkCreateModelMixin, generics.CreateAPIView):
    model = SignupRequest
    serializer_class = SignupRequestSerializer
    authentication_classes = ()
    permission_classes = ()

    def post_save(self, obj, created=False):
        obj.send_email()


class InvitedUserCreateAPIView(generics.CreateAPIView):
    serializer_class = InvitedUserSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            serializer.send_invite()
            return Response(serializer.data)

        return ErrorResponse(serializer.errors)


class InvitedUserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    model = InvitedUser
    serializer_class = InvitedUserFullSerializer
    permission_classes = ()

    def get_object(self, queryset=None):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup = self.kwargs.get(lookup_url_kwarg, None)

        obj = InvitedUser.objects.get_from_token(lookup)

        if not obj:
            raise Http404

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    @action(methods=['PUT'])
    def accept(self, request, pk=None):
        object = self.get_object()
        serializer = self.get_serializer(object)

        object.accept(request.user)

        return Response(serializer.data)

    @action(methods=['PUT'], authentication_classes=())
    def reject(self, request, pk=None):
        object = self.get_object()
        serializer = self.get_serializer(object)

        object.reject()

        return Response(serializer.data)
