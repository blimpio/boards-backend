from django.core.exceptions import ValidationError
from rest_framework import serializers

from .validators import validate_list, validate_domain_name


class PasswordField(serializers.CharField):
    """
    A password field that extends CharField to provide custom defaults.
    """
    min_length = 6
    max_length = None

    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(
            min_length=self.min_length,
            max_length=self.max_length,
            *args,
            **kwargs
        )


class DomainNameField(serializers.CharField):
    default_validators = [validate_domain_name]


class ListField(serializers.WritableField):
    type_name = 'ListField'
    type_label = 'list'

    def validate(self, value_list):
        validate_list(value_list)

        for value in value_list:
            super(ListField, self).validate(value)

    def run_validators(self, value_list):
        errors = []

        for v in self.validators:
            try:
                for value in value_list:
                    v(value)
            except ValidationError as e:
                if hasattr(e, 'code') and e.code in self.error_messages:
                    message = self.error_messages[e.code]
                    if e.params:
                        message = message % e.params
                    errors.append(message)
                else:
                    errors.extend(e.messages)
        if errors:
            raise ValidationError(errors)
