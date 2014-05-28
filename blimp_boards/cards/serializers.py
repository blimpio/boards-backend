from rest_framework import serializers

from ..comments.serializers import CommentSerializer
from ..utils.serializers import DynamicFieldsModelSerializer
from ..users.serializers import UserSimpleSerializer
from .models import Card


CardUserSerializer = UserSimpleSerializer(
    fields=('id', 'username'), read_only=True)


class CardSerializer(DynamicFieldsModelSerializer):
    created_by = CardUserSerializer
    modified_by = CardUserSerializer

    thumbnail_xs_path = serializers.Field(source='signed_thumbnail_xs_path')
    thumbnail_sm_path = serializers.Field(source='signed_thumbnail_sm_path')
    thumbnail_md_path = serializers.Field(source='signed_thumbnail_md_path')
    thumbnail_lg_path = serializers.Field(source='signed_thumbnail_lg_path')

    html_url = serializers.Field()
    download_html_url = serializers.Field()
    original_html_url = serializers.Field()

    metadata = serializers.WritableField(required=False, source='metadata')

    class Meta:
        model = Card
        read_only_fields = ('slug', 'stack', 'comments_count')
        exclude = ('data', )

    def validate_metadata(self, attrs, source):
        metadata = attrs.get(source)
        valid_metadata_keys = ['pattern']
        validation_message = 'Invalid metadata.'
        self.valid_metadata = {}

        if not metadata:
            return attrs

        if not isinstance(metadata, dict):
            raise serializers.ValidationError(validation_message)

        for key in metadata.keys():
            if key not in valid_metadata_keys:
                raise serializers.ValidationError(validation_message)

        self.valid_metadata = metadata

        return attrs

    def validate_content(self, attrs, source):
        content = attrs.get(source)
        card_type = attrs.get('type')

        if card_type != 'stack' and not content:
            raise serializers.ValidationError(self.error_messages['required'])

        return attrs

    def save_object(self, obj, **kwargs):
        created = bool(obj.pk)
        featured_diff = obj.get_field_diff('featured')
        user = self.context['request'].user

        if not created:
            obj.created_by = user

        obj.modified_by = user

        valid_metadata = getattr(self, 'valid_metadata', None)

        if obj.data and valid_metadata:
            obj.data.update(valid_metadata)
        elif valid_metadata:
            obj.data = valid_metadata

        super(CardSerializer, self).save_object(obj, **kwargs)

        # Detect if new card is a file and request thumbnails.
        if not created and obj.type == 'file' and obj.content:
            obj.request_previews()

        if featured_diff and featured_diff[1]:
            obj.notify_featured(user)

    def restore_object(self, attrs, instance=None):
        """
        Restore the model instance.
        """
        if 'metadata' in attrs:
            del attrs['metadata']

        return super(CardSerializer, self).restore_object(attrs, instance)


class StackSerializer(CardSerializer):
    class Meta:
        model = Card
        read_only_fields = ('slug', )
        exclude = ('origin_url', 'content', 'thumbnail_xs_path',
                   'thumbnail_sm_path', 'thumbnail_md_path',
                   'thumbnail_lg_path', 'file_size',
                   'mime_type', 'stack', 'data', 'metadata',
                   'download_html_url', 'original_html_url',
                   'comments_count', )

    def validate_cards(self, attrs, source):
        cards = attrs[source]
        card_type = attrs.get('type')

        if card_type != 'stack':
            attrs[source] = []
            return attrs

        request = self.context['request']

        user_cards_ids = request.user.cards.values_list('id', flat=True)

        for card in cards:
            if card.type == 'stack' or card == self.object \
                    or card.id not in user_cards_ids:
                msg = 'Invalid value.'
                raise serializers.ValidationError(msg)

        return attrs


class CardCommentSerializer(CommentSerializer):
    def save_object(self, obj, **kwargs):
        created = bool(obj.pk)
        card = self.context['content_object']
        user = self.context['request'].user

        if not created:
            obj.created_by = user

        obj.modified_by = user
        obj.content_object = card

        super(CardCommentSerializer, self).save_object(obj, **kwargs)

        if not created:
            card.notify_comment_created(user, obj)
            card.update_comments_count(count=1)