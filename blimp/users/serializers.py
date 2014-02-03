from django.utils.encoding import smart_str
from django.contrib.auth import authenticate
from rest_framework import serializers

from blimp.utils import fields
from blimp.utils.jwt_handlers import jwt_payload_handler, jwt_encode_handler
from blimp.utils.validators import is_valid_email
from blimp.accounts.models import Account, AccountCollaborator
from blimp.accounts.fields import SignupDomainsField
from blimp.invitations.models import SignupRequest, InvitedUser
from .models import User


class ValidateUsernameSerializer(serializers.Serializer):
    """
    Serializer that handles username validation endpoint.
    """
    username = serializers.CharField()

    def validate_username(self, attrs, source):
        username = attrs[source]

        if User.objects.filter(username__iexact=username).exists():
            msg = 'Username is already taken.'
            raise serializers.ValidationError(msg)

        return attrs


class SignupSerializer(serializers.Serializer):
    """
    Serializer that handles signup endpoint data.
    """
    email = serializers.EmailField()
    full_name = serializers.CharField()
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    account_name = serializers.CharField()
    username = serializers.CharField()
    password = fields.PasswordField(write_only=True)
    allow_signup = serializers.BooleanField()
    signup_domains = SignupDomainsField(required=False)
    invite_emails = fields.ListField(required=False)
    signup_request_token = serializers.CharField(write_only=True)

    def validate_signup_request_token(self, attrs, source):
        signup_request_token = attrs[source]
        email = attrs['email']

        signup_request = SignupRequest.objects.get_from_token(
            signup_request_token)

        if not signup_request:
            msg = 'No signup request found for token.'
            raise serializers.ValidationError(msg)

        if signup_request.email != email:
            msg = 'Signup request email does not match email.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_full_name(self, attrs, source):
        full_name = attrs[source]

        attrs['first_name'] = full_name.split(' ')[0]
        attrs['last_name'] = " ".join(full_name.split(' ')[1:])

        return attrs

    def validate_email(self, attrs, source):
        email = attrs[source].lower()

        users_found = User.objects.filter(email__iexact=email)

        if len(users_found) > 0:
            msg = 'Email already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_username(self, attrs, source):
        username = attrs[source].lower()

        if is_valid_email(username):
            msg = 'Invalid username.'
            raise serializers.ValidationError(msg)

        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            msg = 'Username already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_password(self, attrs, source):
        password = attrs[source]

        if password:
            attrs['password'] = smart_str(password)

        return attrs

    def validate_signup_domains(self, attrs, source):
        signup_domains = attrs.get('signup_domains')
        allow_signup = attrs.get('allow_signup')

        if allow_signup and not signup_domains:
            raise serializers.ValidationError(self.error_messages['required'])

        return attrs

    def validate_invite_emails(self, attrs, source):
        invite_emails = set(attrs.get(source, []))
        allow_signup = attrs.get('allow_signup')

        if not allow_signup:
            return attrs

        for email in invite_emails:
            if not is_valid_email(email):
                msg = "{} is not a valid email address.".format(email)
                raise serializers.ValidationError(msg)

        return attrs

    def create_user(self, attrs):
        username = attrs['username']
        email = attrs['email']
        password = attrs['password']
        first_name = attrs['first_name']
        last_name = attrs['last_name']

        extra_fields = {
            'first_name': first_name,
            'last_name': last_name
        }

        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

    def create_account(self, attrs):
        account_name = attrs['account_name']
        allow_signup = attrs['allow_signup']
        signup_domains = attrs.get('signup_domains', [])

        account = Account.objects.create(
            name=account_name,
            allow_signup=allow_signup
        )

        if allow_signup and signup_domains:
            account.add_email_domains(signup_domains)

        return account

    def create_account_owner(self, account, user):
        return AccountCollaborator.objects.create_owner(
            account=account, user=user)

    def invite_users(self, account, user, attrs):
        invite_emails = attrs.get('invite_emails', [])

        for invite_email in invite_emails:
            user_data = {
                'email': invite_email,
                'role': 'team_member',
                'created_by': user
            }

            account.invite_user(user_data)

    def generate_user_token(self, user):
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    def validate(self, attrs):
        user = self.create_user(attrs)
        account = self.create_account(attrs)

        self.create_account_owner(account, user)

        self.invite_users(account, user, attrs)

        return {
            'token': self.generate_user_token(user)
        }


class SignupInvitedUserSerializer(SignupSerializer):
    """
    Serializer that handles signup endpoint data with an invited_user_token.
    """
    invited_user_token = serializers.CharField(write_only=True)

    class Meta:
        fields = ('email', 'full_name', 'first_name', 'last_name', 'username',
                  'password', 'invite_emails', 'invited_user_token')

    def validate_invited_user_token(self, attrs, source):
        invited_user_token = attrs[source]
        email = attrs['email']

        self.invited_user = InvitedUser.objects.get_from_token(
            invited_user_token)

        if not self.invited_user:
            msg = 'No invited user found for token.'
            raise serializers.ValidationError(msg)

        if self.invited_user.email != email:
            msg = 'Invited user email does not match signup email.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate(self, attrs):
        user = self.create_user(attrs)
        account = self.invited_user.account

        self.invited_user.accept(user)

        self.invite_users(account, user, attrs)

        return {
            'token': self.generate_user_token(user)
        }


class SigninInvitedUserSerializer(serializers.Serializer):
    """
    Serializer that handles signin endpoint data with an invited_user_token.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    invited_user_token = serializers.CharField(write_only=True)

    def validate_invited_user_token(self, attrs, source):
        invited_user_token = attrs[source]

        self.invited_user = InvitedUser.objects.get_from_token(
            invited_user_token)

        if not self.invited_user:
            msg = 'No invited user found for token.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                self.invited_user.accept(user)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload)
                }
            else:
                msg = 'Unable to login with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password"'
            raise serializers.ValidationError(msg)


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer that handles forgot password endpoint.
    """
    email = serializers.EmailField()

    def validate_email(self, attrs, source):
        email = attrs[source].lower()

        try:
            self.user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            msg = 'No user found.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate(self, attrs):
        self.user.send_password_reset_email()
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer that handles reset password endpoint.
    """
    token = serializers.CharField(write_only=True)
    password = fields.PasswordField(write_only=True)

    def validate_password(self, attrs, source):
        password = attrs[source]

        if password:
            attrs['password'] = smart_str(password)

        return attrs

    def validate_token(self, attrs, source):
        token = attrs[source]

        self.user = User.objects.get_from_password_reset_token(token)

        if not self.user:
            msg = 'Invalid password reset token.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate(self, attrs):
        self.user.set_password(attrs['password'])
        self.user.save()

        return {
            'password_reset': True
        }
