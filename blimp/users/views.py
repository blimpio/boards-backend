from django.http import Http404

from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken

from blimp.users.models import User
from blimp.invitations.models import SignupRequest
from .serializers import (ValidateUsernameSerializer, SignupSerializer,
                          ForgotPasswordSerializer, ResetPasswordSerializer)


class SigninAPIView(ObtainJSONWebToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(serializer.object)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SignupValidateTokenHTMLView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        token = request.QUERY_PARAMS.get('token')

        if token:
            signup_request = SignupRequest.objects.get_from_token(token)

            if not signup_request:
                raise Http404

        return Response(template_name='index.html')


class ResetPasswordHTMLView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        token = request.QUERY_PARAMS.get('token')

        user = User.objects.get_from_password_reset_token(token)

        if not user:
            raise Http404

        return Response(template_name='index.html')
