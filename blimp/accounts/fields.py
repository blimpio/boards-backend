from blimp.utils.fields import CharacterSeparatedField

from .validators import validate_signup_domain


class SignupDomainsField(CharacterSeparatedField):
    default_validators = [validate_signup_domain]
