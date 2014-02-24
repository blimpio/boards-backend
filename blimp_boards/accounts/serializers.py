from rest_framework import serializers

from ..utils.fields import DomainNameField
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
        fields = ('id', 'name', 'slug', 'image_url',
                  'date_created', 'date_modified')


class CheckSignupDomainSerializer(serializers.Serializer):
    """
    Serializer to get account that has signup domain setup.
    """
    signup_domain = DomainNameField()

    def validate_signup_domain(self, attrs, source):
        signup_domain = attrs[source]
        data = {}

        try:
            account = Account.objects.get(
                allow_signup=True, email_domains__domain_name=signup_domain)
            data = AccountSerializer(account).data
        except Account.DoesNotExist:
            pass

        return data
