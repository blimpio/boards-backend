from django.utils.encoding import smart_str
from django.contrib.auth import authenticate
from rest_framework import serializers

from ..utils import fields
from ..utils.validators import is_valid_email
from ..accounts.models import Account, AccountCollaborator
from ..accounts.fields import SignupDomainsField
from ..accounts.serializers import AccountSerializer
from ..invitations.models import SignupRequest, InvitedUser
from .models import User


class ValidateUsernameSerializer(serializers.Serializer):
    """
    Serializer that handles username validation endpoint.
    """
    username = serializers.CharField()

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

        self.signup_request = SignupRequest.objects.get_from_token(
            signup_request_token)

        if not self.signup_request:
            msg = 'No signup request found for token.'
            raise serializers.ValidationError(msg)

        if self.signup_request.email != email:
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
                'created_by': user
            }

            account.invite_user(user_data)

    def validate(self, attrs):
        user = self.create_user(attrs)
        account = self.create_account(attrs)

        self.create_account_owner(account, user)

        self.invite_users(account, user, attrs)

        self.signup_request.delete()

        return UserSerializer(user).data


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

        return UserSerializer(user).data


class SigninSerializer(serializers.Serializer):
    """
    Serializer that handles signin endpoint data.
    """
    username = serializers.CharField()
    password = fields.PasswordField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        self.user = authenticate(username=username, password=password)

        if self.user:
            if not self.user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg)

            return UserSerializer(self.user).data
        else:
            msg = 'Unable to login with provided credentials.'
            raise serializers.ValidationError(msg)


class SigninInvitedUserSerializer(SigninSerializer):
    """
    Serializer that handles signin endpoint data with an invited_user_token.
    """
    invited_user_token = serializers.CharField(write_only=True)

    class Meta:
        fields = ('username', 'password', 'invited_user_token', )

    def validate_invited_user_token(self, attrs, source):
        invited_user_token = attrs[source]

        self.invited_user = InvitedUser.objects.get_from_token(
            invited_user_token)

        if not self.invited_user:
            msg = 'No invited user found for token.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate(self, attrs):
        user_data = super(SigninInvitedUserSerializer, self).validate(attrs)

        self.invited_user.accept(self.user)

        return user_data


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

    def send_password_reset_email(self):
        self.user.send_password_reset_email()


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
        self.user.change_password(attrs['password'])

        return {
            'password_reset': True
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Serializers used for User objects.
    """
    token = serializers.Field(source='token')
    accounts = AccountSerializer(many=True, source='accounts')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'job_title', 'avatar_path', 'gravatar_url',
                  'timezone', 'date_created', 'date_modified',
                  'token', 'accounts',)


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer that handles user settings endpoint.
    """
    token = serializers.Field(source='token')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'job_title', 'avatar_path', 'gravatar_url',
                  'timezone', 'date_created', 'date_modified', 'token',)

    def validate_email(self, attrs, source):
        email = attrs[source].lower()
        user = self.object

        users = User.objects.filter(
            email__iexact=email).exclude(pk=user.id)

        if users.exists():
            msg = 'Email already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_username(self, attrs, source):
        username = attrs[source].lower()
        user = self.object

        if is_valid_email(username):
            msg = 'Invalid username.'
            raise serializers.ValidationError(msg)

        users = User.objects.filter(
            username=username).exclude(pk=user.id)

        if users.exists():
            msg = 'Username already exists.'
            raise serializers.ValidationError(msg)

        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer that handles change pagssword in user settings endpoint.
    """
    current_password = fields.PasswordField(write_only=True)
    password1 = fields.PasswordField(write_only=True)
    password2 = fields.PasswordField(write_only=True)

    class Meta:
        model = User
        fields = ('current_password', 'password1', 'password2')

    def validate_current_password(self, attrs, source):
        password = attrs[source]
        user = self.object

        if user and not user.check_password(password):
            msg = 'Current password is invalid.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_password2(self, attrs, source):
        password_confirmation = attrs[source]
        password = attrs['password1']

        if password_confirmation != password:
            msg = "Password doesn't match the confirmation."
            raise serializers.ValidationError(msg)

        attrs[source] = smart_str(password_confirmation)

        return attrs

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.change_password(attrs.get('password2'))
            return instance

        return User()
