from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    target = serializers.Field(source='data.target')
    action_object = serializers.Field(source='data.action_object')
    actor = serializers.Field(source='data.sender')
    timesince = serializers.Field(source='timesince')

    class Meta:
        model = Notification
        fields = ('target', 'action_object', 'actor', 'verb', 'timesince',
                  'date_created', 'date_modified')
