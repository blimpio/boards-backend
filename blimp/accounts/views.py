from rest_framework import status, generics
from rest_framework.response import Response

from .serializers import (ValidateSignupDomainsSerializer,
                          AccountSerializer)

from .models import AccountCollaborator


class ValidateSignupDomainsAPIView(generics.CreateAPIView):
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


class AccountsForUserView(generics.ListAPIView):
    """
    Get a list of accounts for the user in the request
    """
    serializer_class = AccountSerializer

    def get_queryset(self):
        user = self.request.user
        acs = AccountCollaborator.objects.select_related(
            'account').filter(user=user)

        return [ac.account for ac in acs]
