from rest_framework import serializers

from ..accounts.models import Account
from .models import SignupRequest, InvitedUser


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupRequest
        fields = ('email',)

    def full_clean(self, instance):
        """
        Prevent error because of unique email
        before trying to get or save object.
        """
        return instance

    def save_object(self, obj, **kwargs):
        SignupRequest.objects.get_or_create(email=obj.email)


class InvitedUserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedUser
        fields = ('id', 'first_name', 'last_name', 'email',
                  'date_created', 'date_modified')


class InvitedUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    account = serializers.IntegerField()

    def validate_account(self, attrs, source):
        account_id = attrs[source]
        email = attrs.get('email')

        if not email:
            return attrs

        signup_domain = email.split('@')[1]

        try:
            self.account = Account.objects.get(
                pk=account_id,
                allow_signup=True,
                email_domains__domain_name=signup_domain
            )
        except Account.DoesNotExist:
            msg = 'Account does not allow signup with email address.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate(self, attrs):
        self.user_data = {
            'email': attrs['email'],
            'created_by': self.account.owner.user
        }

        return attrs

    def send_invite(self):
        self.account.invite_user(self.user_data)
