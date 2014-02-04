from rest_framework import serializers

from .fields import SignupDomainsField
from .models import Account


class ValidateSignupDomainsSerializer(serializers.Serializer):
    """
    Serializer that handles signup domains validation endpoint.
    """
    signup_domains = SignupDomainsField()


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Accounts.
    """
    class Meta:
        model = Account
        fields = ('id', 'name', 'slug', 'image_url')
