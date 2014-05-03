from django.utils.six.moves.urllib import parse

from rest_framework import serializers

from ..files.utils import sign_s3_url
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    target = serializers.SerializerMethodField('get_target_data')
    action_object = serializers.SerializerMethodField('get_action_object_data')
    actor = serializers.Field(source='data.sender')
    timesince = serializers.Field(source='timesince')

    class Meta:
        model = Notification
        fields = ('target', 'action_object', 'actor', 'verb', 'timesince',
                  'date_created', 'date_modified')

    def get_action_object_data(self, obj):
        return self._data_with_signed_urls(obj.data['action_object'])

    def get_target_data(self, obj):
        return self._data_with_signed_urls(obj.data['target'])

    def _data_with_signed_urls(self, data):
        thumbnail_keys = [
            'thumbnail_sm_path',
            'thumbnail_md_path',
            'thumbnail_lg_path'
        ]

        for key, value in data.items():
            if key in thumbnail_keys and value:
                split_results = list(tuple(parse.urlsplit(value)))
                split_results[-2] = ''
                cleaned_url = parse.unquote(parse.urlunsplit(split_results))
                data[key] = sign_s3_url(cleaned_url)

        return data
