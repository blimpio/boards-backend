from rest_framework import serializers

from ..accounts.permissions import AccountPermission
from .models import Board, BoardCollaborator, BoardCollaboratorRequest


class BoardSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Board
        read_only_fields = ('slug', )

    def validate_account(self, attrs, source):
        account = attrs[source]
        request = self.context['request']
        view = self.context['view']

        permission = AccountPermission()
        has_object_permission = permission.has_object_permission(
            request, view, account)

        if not has_object_permission:
            msg = 'You are not a collaborator in this account.'
            raise serializers.ValidationError(msg)

        return attrs

    def save_object(self, obj, **kwargs):
        obj.created_by = self.context['request'].user
        return super(BoardSerializer, self).save_object(obj, **kwargs)


class BoardCollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCollaborator


class BoardCollaboratorRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = BoardCollaboratorRequest
