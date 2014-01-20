from rest_framework import serializers

from .models import InviteRequest


class ValidateInviteRequestSerializer(serializers.Serializer):
    email = serializers.CharField(read_only=True)
    token = serializers.CharField(write_only=True)

    def validate_token(self, attrs, source):
        token = attrs[source]

        self.invite_request = InviteRequest.objects.get_from_token(token)

        if not self.invite_request:
            msg = 'No Invite Request found.'
            raise serializers.ValidationError(msg)

        return attrs

    def restore_object(self, attrs, instance=None):
        return self.invite_request
