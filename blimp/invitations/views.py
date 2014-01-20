from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InviteRequest
from .serializers import ValidateInviteRequestSerializer


class InviteRequestCreateAPIView(generics.CreateAPIView):
    model = InviteRequest
    authentication_classes = ()
    permission_classes = ()


class ValidateInviteRequestAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ValidateInviteRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
