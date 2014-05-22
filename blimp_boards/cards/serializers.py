from rest_framework import serializers

from ..comments.serializers import CommentSerializer
from ..utils.serializers import DynamicFieldsModelSerializer
from .models import Card


class CardSerializer(DynamicFieldsModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_by = serializers.PrimaryKeyRelatedField(read_only=True)

    thumbnail_xs_path = serializers.Field(source='signed_thumbnail_xs_path')
    thumbnail_sm_path = serializers.Field(source='signed_thumbnail_sm_path')
    thumbnail_md_path = serializers.Field(source='signed_thumbnail_md_path')
    thumbnail_lg_path = serializers.Field(source='signed_thumbnail_lg_path')

    html_url = serializers.Field()

    class Meta:
        model = Card
        read_only_fields = ('slug', 'stack', )
        exclude = ('data', )

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

        super(CardSerializer, self).save_object(obj, **kwargs)

        if featured_diff and featured_diff[1]:
            obj.notify_featured(user)


class StackSerializer(CardSerializer):
    class Meta:
        model = Card
        read_only_fields = ('slug', )
        exclude = ('origin_url', 'content', 'thumbnail_xs_path',
                   'thumbnail_sm_path', 'thumbnail_md_path',
                   'thumbnail_lg_path', 'file_size',
                   'mime_type', 'stack', 'data')

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