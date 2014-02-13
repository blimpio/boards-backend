from rest_framework import serializers

from .models import Card


class CardSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Card

    def __init__(self, *args, **kwargs):
        serializer = super(CardSerializer, self).__init__(*args, **kwargs)
        request = self.context['request']

        if request and request.user:
            self.fields['cards'].queryset = request.user.cards

        return serializer

    def validate_content(self, attrs, source):
        content = attrs.get(source)
        card_type = attrs.get('type')

        if card_type != 'stack' and not content:
            raise serializers.ValidationError(self.error_messages['required'])

        return attrs

    def save_object(self, obj, **kwargs):
        obj.created_by = self.context['request'].user
        return super(CardSerializer, self).save_object(obj, **kwargs)
