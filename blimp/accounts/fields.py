from blimp.utils.fields import CharacterSeparatedField
from blimp.utils.validators import validate_domain_name


class SignupDomainsField(CharacterSeparatedField):
    default_validators = [validate_domain_name]
