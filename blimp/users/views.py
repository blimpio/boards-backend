from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ValidateUsernameSerializer, SignupSerializer


class ValidateUsernameAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ValidateUsernameSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SignupAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            serializer.signup()
            return Response(serializer.data)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
