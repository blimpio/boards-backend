from rest_framework import status, generics
from rest_framework.response import Response

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

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


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

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class AccountsForUserAPIView(generics.ListAPIView):
    """
    Get a list of accounts for the user in the request
    """
    serializer_class = AccountSerializer

    def get_queryset(self):
        return self.request.user.accounts
