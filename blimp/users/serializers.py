from django.utils.encoding import smart_str
from rest_framework import serializers

from blimp.utils import fields
from blimp.utils.jwt_handlers import jwt_payload_handler, jwt_encode_handler
from blimp.utils.validators import is_valid_email
from blimp.accounts.models import Account, AccountMember, EmailDomain
from blimp.accounts.fields import SignupDomainsField
from blimp.invitations.models import SignupRequest
from .models import User


class ValidateUsernameSerializer(serializers.Serializer):
    """
    Serializer that handles username validation endpoint.
    """
    username = serializers.CharField(write_only=True)

    def validate_username(self, attrs, source):
        username = attrs[source]

        return {
            'exists': User.objects.filter(username=username).exists()
        }


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
    invite_emails = fields.CharacterSeparatedField(required=False)
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
        signup_domains = set(attrs.get(source, []))
        allow_signup = attrs.get('allow_signup')

        if not allow_signup:
            return attrs

        for domain in signup_domains:
            is_valid = EmailDomain.is_signup_domain_valid(domain)

            if not is_valid:
                msg = "{} is an invalid sign-up domain.".format(domain)
                raise serializers.ValidationError(msg)

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

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']
        password = attrs['password']
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        account_name = attrs['account_name']
        allow_signup = attrs['allow_signup']
        invite_emails = attrs.get('invite_emails', [])
        signup_domains = attrs.get('signup_domains', [])

        extra_fields = {
            'first_name': first_name,
            'last_name': last_name
        }

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

        account = Account.objects.create(
            name=account_name,
            allow_signup=allow_signup
        )

        if allow_signup and signup_domains:
            account.add_email_domains(signup_domains)

        AccountMember.objects.create_owner(account=account, user=user)

        for invite_email in invite_emails:
            user_data = {
                'email': invite_email,
                'role': 'team_member',
                'created_by': user
            }

            account.invite_user(user_data)

        payload = jwt_payload_handler(user)

        return {
            'token': jwt_encode_handler(payload)
        }


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
