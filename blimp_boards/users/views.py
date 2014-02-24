from django.http import Http404

from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from ..utils.shortcuts import redirect_with_params
from ..invitations.models import SignupRequest, InvitedUser
from .models import User
from . import serializers


class SigninAPIView(generics.CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = serializers.SigninSerializer

    def get_serializer_class(self):
        if self.request.DATA.get('invited_user_token'):
            return serializers.SigninInvitedUserSerializer
        return super(SigninAPIView, self).get_serializer_class()

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ValidateUsernameAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.ValidateUsernameSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SignupAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.SignupSerializer

    def get_serializer_class(self):
        if self.request.DATA.get('invited_user_token'):
            return serializers.SignupInvitedUserSerializer
        return super(SignupAPIView, self).get_serializer_class()

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserSettingsAPIView(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = serializers.UserSettingsSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(generics.CreateAPIView):
    model = User
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request):
        serializer_class = serializers.ChangePasswordSerializer
        serializer = serializer_class(data=request.DATA, instance=request.user)

        if serializer.is_valid():
            data = serializers.UserSettingsSerializer(serializer.object).data
            return Response(data)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SigninValidateTokenHTMLView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        invite = request.QUERY_PARAMS.get('invite')

        if invite:
            invited_user = InvitedUser.objects.get_from_token(invite)

            if not invited_user:
                raise Http404

            if not invited_user.user:
                return redirect_with_params(request, 'auth-signup')

        return Response(template_name='index.html')


class SignupValidateTokenHTMLView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        token = request.QUERY_PARAMS.get('token')
        invite = request.QUERY_PARAMS.get('invite')

        if token and not invite:
            signup_request = SignupRequest.objects.get_from_token(token)

            if not signup_request:
                raise Http404

        if invite:
            invited_user = InvitedUser.objects.get_from_token(invite)

            if not invited_user:
                raise Http404

            if invited_user.user:
                return redirect_with_params(request, 'auth-signin')

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
