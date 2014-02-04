from django.core.exceptions import ValidationError

from ..utils.validators import validate_domain_name
from .models import EmailDomain
from .constants import BLACKLIST_SIGNUP_DOMAINS


class SignupDomainValidator(object):
    """
    Validates the specified signup_domain by checking for blacklisted
    domains and already existing signup domains.
    """
    message = 'Enter a valid sign-up domain.'

    def __call__(self, value):
        if not value:
            raise ValidationError(self.message)

        self.message = "{} is an invalid sign-up domain.".format(value)

        try:
            validate_domain_name(value)
        except ValidationError:
            raise ValidationError(self.message)

        domain_exists = EmailDomain.objects.filter(
            domain_name=value).exists()

        if value in BLACKLIST_SIGNUP_DOMAINS or domain_exists:
            raise ValidationError(self.message)


validate_signup_domain = SignupDomainValidator()
