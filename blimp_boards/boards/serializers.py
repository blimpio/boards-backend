from django.core.exceptions import ValidationError

from rest_framework import serializers

from ..accounts.models import AccountCollaborator
from ..invitations.models import InvitedUser
from ..accounts.permissions import AccountPermission
from ..users.serializers import UserSimpleSerializer
from ..invitations.serializers import InvitedUserSimpleSerializer
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
    email = serializers.EmailField(write_only=True, required=False)
    user_data = serializers.SerializerMethodField('get_user_data')

    class Meta:
        model = BoardCollaborator
        read_only_fields = ('board', )
        fields = ('id', 'board', 'user', 'invited_user', 'permission',
                  'email', 'user_data', 'date_created', 'date_modified',)

    def get_user_data(self, obj):
        if obj.invited_user:
            serializer = InvitedUserSimpleSerializer(obj.invited_user)
        else:
            serializer = UserSimpleSerializer(obj.user)

        return serializer.data

    def validate_email(self, attrs, source):
        email = attrs.get(source)

        if not email:
            return attrs

        del attrs[source]

        board = self.context['board']
        account = board.account

        try:
            account_collaborator = AccountCollaborator.objects.get(
                account=account, user__email=email)
            attrs['user'] = account_collaborator.user
        except AccountCollaborator.DoesNotExist:
            invited_user_data = {
                'email': email,
                'account': account,
                'created_by': self.context['request'].user,
            }

            self.invited_user, created = InvitedUser.objects.get_or_create(
                email=email, account=account, defaults=invited_user_data)

            attrs['invited_user'] = self.invited_user

        return attrs

    def validate_user(self, attrs, source):
        user = attrs.get(source)
        board = attrs.get('board')

        if user and board and board.is_user_collaborator(user):
            msg = 'User is already a collaborator in this board.'
            raise ValidationError(msg)

        return attrs

    def save_object(self, obj, **kwargs):
        created = bool(obj.pk)

        obj.board = self.context['board']

        super(BoardCollaboratorSerializer, self).save_object(obj, **kwargs)

        if not created and obj.invited_user:
            self.invited_user.board_collaborators.add(obj)
            self.invited_user.send_invite()


class BoardCollaboratorPublicSerializer(BoardCollaboratorSerializer):
    """
    BoardCollaborator serializer that removes email from
    user and invited_user fields.
    """
    class Meta:
        model = BoardCollaborator

    def get_user_data(self, obj):
        data = super(BoardCollaboratorPublicSerializer,
                     self).get_user_data(obj)

        data.pop('email', None)

        return data


class BoardCollaboratorRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = BoardCollaboratorRequest
