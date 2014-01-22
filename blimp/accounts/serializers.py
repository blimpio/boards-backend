from rest_framework import serializers

from blimp.utils import fields
from blimp.accounts.models import EmailDomain


class ValidateSignupDomainsSerializer(serializers.Serializer):
    """
    Serializer that handles signup domains validation endpoint.
    """
    signup_domains = fields.CharacterSeparatedField()

    def validate_signup_domains(self, attrs, source):
        signup_domains = attrs[source]

        for domain in signup_domains:
            is_valid = EmailDomain.is_signup_domain_valid(domain)
            if not is_valid:
                msg = "You can't have {} as a sign-up domain.".format(domain)
                raise serializers.ValidationError(msg)

        return attrs
