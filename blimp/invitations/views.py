from rest_framework import generics, status
from rest_framework.response import Response

from .models import SignupRequest
from .serializers import SignupRequestSerializer


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

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def post_save(self, obj, created=False):
        obj.send_email()
