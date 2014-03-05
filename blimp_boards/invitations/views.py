from rest_framework import generics
from rest_framework.response import Response

from ..utils.response import ErrorResponse
from .models import SignupRequest
from .serializers import SignupRequestSerializer, InvitedUserSerializer


class SignupRequestCreateAPIView(generics.CreateAPIView):
    model = SignupRequest
    serializer_class = SignupRequestSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return super(SignupRequestCreateAPIView, self).post(
                request, *args, **kwargs)

        return ErrorResponse(serializer.errors)

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
