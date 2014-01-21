from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import SignupRequest
from .serializers import ValidateSignupRequestSerializer


class SignupRequestCreateAPIView(generics.CreateAPIView):
    model = SignupRequest
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return super(SignupRequestCreateAPIView, self).post(
                request, *args, **kwargs)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ValidateSignupRequestAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ValidateSignupRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
