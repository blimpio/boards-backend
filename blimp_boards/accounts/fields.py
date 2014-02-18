from ..utils.fields import ListField
from .validators import validate_signup_domain


class SignupDomainsField(ListField):
    default_validators = [validate_signup_domain]
