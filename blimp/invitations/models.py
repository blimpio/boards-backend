import jwt

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.loading import get_model

from blimp.boards.constants import PERMISSION_CHOICES
from blimp.users.models import User
from blimp.users.utils import get_gravatar_url
from .managers import SignupRequestManager, InvitedUserManager


class SignupRequest(models.Model):
    email = models.EmailField(unique=True)
    objects = SignupRequestManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Returns a JSON Web Token
        """
        payload = {
            'type': 'SignupRequest',
            'email': self.email,
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY)

        return jwt_token.decode('utf-8')

    def send_email(self):
        message = '{}'.format(self.token)

        return send_mail(
            'Blimp Signup Request',
            message,
            'from@example.com',
            [self.email],
            fail_silently=False
        )


class InvitedUser(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    user = models.ForeignKey('users.User', null=True, blank=True)
    account = models.ForeignKey('accounts.Account')
    created_by = models.ForeignKey(
        'users.User', related_name='%(class)s_created_by')

    board_collaborators = models.ManyToManyField('boards.BoardCollaborator',
                                                 blank=True, null=True)

    objects = InvitedUserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Returns a JSON Web Token
        """
        payload = {
            'type': 'InvitedUser',
            'pk': self.pk
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY)

        return jwt_token.decode('utf-8')

    def save(self, *args, **kwargs):
        """
        When saving a new InvitedUser, try to set first_name,
        last_name, and email if a user is given. If no user is given,
        try to find an existing user with matching email.
        """
        if not self.pk:
            if not self.user:
                try:
                    self.user = User.objects.get(email=self.email)
                except User.DoesNotExist:
                    pass

            if self.user:
                self.first_name = self.user.first_name
                self.last_name = self.user.last_name
                self.email = self.user.email

        return super(InvitedUser, self).save(*args, **kwargs)

    def get_email(self):
        return self.user.email if self.user else self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = u'{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_gravatar_url(self):
        return get_gravatar_url(self.email)

    def get_invite_url(self):
        pass

    def accept(self, user):
        """
        - Create AccountCollaborator
        - Set user to BoardCollaborators
        - Delete invitation
        """
        AccountCollaborator = get_model('accounts', 'AccountCollaborator')

        collaborator = AccountCollaborator.objects.create(
            user=user, account=self.account)

        self.board_collaborators.all().update(user=user, invited_user=None)

        self.delete()

        return collaborator

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        if self.user:
            self.user.email_user(
                subject, message, from_email=from_email, **kwargs)
        else:
            send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_invite(self):
        message = '{}'.format(self.token)

        self.email_user(
            'You were invited to join {}'.format(self.account),
            message,
            from_email='from@example.com',
        )
