from rest_framework import serializers

from .fields import SignupDomainsField


class ValidateSignupDomainsSerializer(serializers.Serializer):
    """
    Serializer that handles signup domains validation endpoint.
    """
    signup_domains = SignupDomainsField()
