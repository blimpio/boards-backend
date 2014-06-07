from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from rest_framework import serializers
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify

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
    default_error_messages = {
        'invalid': 'Enter a valid domain name.',
    }


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


class DateTimeCreatedField(models.DateTimeField):
    """
    DateTimeField that by default, sets editable=False,
    blank=True, default=now.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', now)
        super(DateTimeCreatedField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'DateTimeField'

    def pre_save(self, model, add):
        if not model.pk:
            value = now()

            setattr(model, self.attname, value)

            return value

        return super(DateTimeCreatedField, self).pre_save(model, add)

    def south_field_triple(self):
        """
        Returns a suitable description of this field for South.
        """
        from south.modelsinspector import introspector

        field_class = 'django.db.models.fields.DateTimeField'
        args, kwargs = introspector(self)

        return (field_class, args, kwargs)


class DateTimeModifiedField(DateTimeCreatedField):
    """
    DateTimeField that by default, sets editable=False,
    blank=True, default=datetime.now.

    Sets value to now() on each save of the model.
    """

    def pre_save(self, model, add):
        value = now()
        setattr(model, self.attname, value)
        return value


class ReservedKeywordsAutoSlugField(AutoSlugField):
    def __init__(self, *args, **kwargs):
        reserved_keywords = kwargs.pop('reserved_keywords')

        super(ReservedKeywordsAutoSlugField, self).__init__(*args, **kwargs)

        def custom_slugify(value):
            value = value.replace('.', '-')
            pre_slug = default_slugify(value)

            if pre_slug in reserved_keywords:
                pre_slug = '{}1'.format(pre_slug)

            return pre_slug

        self.slugify = custom_slugify
