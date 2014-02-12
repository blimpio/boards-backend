from rest_framework import serializers

from .models import Card


class CardSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Card

    def save_object(self, obj, **kwargs):
        obj.created_by = self.context['request'].user
        return super(CardSerializer, self).save_object(obj, **kwargs)
