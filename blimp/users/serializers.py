from django.utils.encoding import smart_str
from rest_framework import serializers

from blimp.utils import fields
from blimp.utils.validators import is_valid_email
from blimp.accounts.models import Account, AccountMember
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
    password = serializers.CharField(write_only=True)
    allow_signup = serializers.BooleanField()
    signup_domains = fields.CharacterSeparatedField(required=False)
    invite_emails = fields.CharacterSeparatedField(required=False)

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

        blacklist = set(['gmail.com', 'yahoo.com', 'hotmail.com'])
        unallowed_domains = signup_domains.intersection(blacklist)

        if allow_signup and len(unallowed_domains) > 0:
            for domain in unallowed_domains:
                msg = "You can't have {} as a sign-up domain.".format(domain)
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

    def signup(self):
        user = self.create_user()
        account, owner = self.create_account(user)

        self.invite_users(account, user)

        return user

    def create_user(self):
        username = self.object['username']
        email = self.object['email']
        password = self.object['password']
        first_name = self.object['first_name']
        last_name = self.object['last_name']

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

    def create_account(self, user):
        account_name = self.object['account_name']
        allow_signup = self.object['allow_signup']

        account = Account.objects.create(
            name=account_name,
            allow_signup=allow_signup
        )

        if allow_signup:
            account.add_email_domains(self.object['signup_domains'])

        owner = AccountMember.objects.create_owner(account=account, user=user)

        return account, owner

    def invite_users(self, account, user):
        invite_emails = self.object.get('invite_emails', [])
        invited_users = []

        for invite_email in invite_emails:
            user_data = {
                'email': invite_email,
                'role': 'team_member',
                'created_by': user
            }

            invited_users.append(account.invite_user(user_data))

        return invited_users
