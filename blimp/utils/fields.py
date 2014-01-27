from rest_framework import serializers


class CharacterSeparatedField(serializers.WritableField):
    """
    A field that separates a string with a given separator into
    a native list and reverts a list into a string separated with a given
    separator.
    """
    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ',')
        super(CharacterSeparatedField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        if obj:
            return self.separator.join(obj)

    def from_native(self, data):
        return data.split(self.separator)

    def run_validators(self, value):
        for val in value:
            return super(CharacterSeparatedField, self).run_validators(val)


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
