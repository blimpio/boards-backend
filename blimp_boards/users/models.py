import re
import pytz
import uuid
import os
import datetime
import jwt

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.conf import settings
from django.db.models.loading import get_model

from .managers import UserManager


def update_last_ip(sender, user, request, **kwargs):
    """
    A signal receiver which updates the last_ip for
    the user logging in.
    """
    user.last_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    user.save()
user_logged_in.connect(update_last_ip)


def get_user_upload_path(instance, filename):
    # TODO: Change to uploads/users/avatars/?
    identifier = str(uuid.uuid4())
    return os.path.join(
        'uploads', 'users', instance.email, identifier, filename)


class User(AbstractBaseUser, PermissionsMixin):
    PRETTY_TIMEZONE_CHOICES = [('', '--- Select ---')]

    for tz in pytz.common_timezones:
        now = datetime.datetime.now(pytz.timezone(tz))
        PRETTY_TIMEZONE_CHOICES.append(
            (tz, ' %s (GMT%s)' % (tz, now.strftime('%z'))))

    username_help_text = _(
        'Required. 30 characters or fewer. '
        'Letters, numbers and '
        '@/./+/-/_ characters'
    )

    username_validator = validators.RegexValidator(
        re.compile('^[\w.@+-]+$'),
        _('Enter a valid username.'),
        'invalid'
    )

    is_staff_help_text = _(
        'Designates whether the user can log into this admin site.'
    )

    is_active_help_text = _(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'
    )

    username = models.CharField(
        _('username'), max_length=30, unique=True,
        help_text=username_help_text, validators=[username_validator]
    )

    first_name = models.CharField(_('first name'), max_length=30)

    last_name = models.CharField(_('last name'), max_length=30)

    email = models.EmailField(_('email address'), max_length=254, unique=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=is_staff_help_text
    )

    is_active = models.BooleanField(
        _('active'), default=True, help_text=is_active_help_text
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    phone = models.CharField(max_length=40, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to=get_user_upload_path,
                               blank=True, max_length=255)
    gravatar_url = models.URLField(blank=True)
    facebook_id = models.CharField(max_length=255, blank=True)
    twitter_username = models.CharField(max_length=255, blank=True)
    skype_username = models.CharField(max_length=255, blank=True)
    aim_username = models.CharField(max_length=255, blank=True)
    gtalk_username = models.CharField(max_length=255, blank=True)
    windows_live_id = models.CharField(max_length=255, blank=True)
    last_ip = models.IPAddressField(blank=True, null=True, default='127.0.0.1')
    timezone = models.CharField(max_length=255, default='UTC',
                                choices=PRETTY_TIMEZONE_CHOICES)

    token_version = models.CharField(max_length=36, default=str(uuid.uuid4()),
                                     unique=True, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    @property
    def password_reset_token(self):
        """
        Returns a JSON Web Token used for Password Reset
        """
        payload = {
            'type': 'PasswordReset',
            'id': self.pk,
            'token_version': self.token_version,
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY)

        return jwt_token.decode('utf-8')

    @property
    def accounts(self):
        """
        Returns a list of all accounts where user is a collaborator.
        """
        Account = get_model('accounts', 'Account')
        AccountCollaborator = get_model('accounts', 'AccountCollaborator')

        account_ids = AccountCollaborator.objects.filter(
            user=self).values_list('account_id', flat=True)

        return Account.objects.filter(pk__in=account_ids)

    @property
    def boards(self):
        """
        Returns a list of all boards where user is a collaborator.
        """
        Board = get_model('boards', 'Board')
        BoardCollaborator = get_model('boards', 'BoardCollaborator')

        board_ids = BoardCollaborator.objects.filter(
            user=self).values_list('board_id', flat=True)

        return Board.objects.filter(pk__in=board_ids)

    @property
    def cards(self):
        """
        Returns a list of all cards of boards where user is a collaborator.
        """
        Card = get_model('cards', 'Card')

        return Card.objects.filter(board__in=self.boards)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def set_password(self, raw_password):
        """
        Sets the user's password and changes token_version.
        """
        super(User, self).set_password(raw_password)
        self.reset_token_version()

    def reset_token_version(self):
        """
        Resets the user's token_version.
        """
        self.token_version = str(uuid.uuid4())

    def send_password_reset_email(self):
        message = '{}'.format(self.password_reset_token)

        self.email_user(
            'Password Reset',
            message,
            from_email='from@example.com',
        )
