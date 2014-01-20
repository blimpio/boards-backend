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
