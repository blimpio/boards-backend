from django.core.exceptions import ValidationError

from blimp.utils.validators import validate_domain_name
from .models import EmailDomain
from .constants import BLACKLIST_SIGNUP_DOMAINS


def validate_signup_domain(value):
    """
    Validates the specified signup_domain by checking for blacklisted
    domains and already existing signup domains.
    """
    error_message = "{} is an invalid sign-up domain.".format(value)

    try:
        validate_domain_name(value)
    except ValidationError:
        raise ValidationError(error_message)

    domain_exists = EmailDomain.objects.filter(
        domain_name=value).exists()

    if value in BLACKLIST_SIGNUP_DOMAINS or domain_exists:
        raise ValidationError(error_message)
