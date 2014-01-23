from rest_framework import serializers

from .models import SignupRequest


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupRequest
        fields = ('email',)


class ValidateSignupRequestSerializer(serializers.Serializer):
    email = serializers.CharField(read_only=True)
    token = serializers.CharField(write_only=True)

    def validate_token(self, attrs, source):
        token = attrs[source]

        self.signup_request = SignupRequest.objects.get_from_token(token)

        if not self.signup_request:
            msg = 'No Invite Request found.'
            raise serializers.ValidationError(msg)

        return attrs

    def restore_object(self, attrs, instance=None):
        return self.signup_request
