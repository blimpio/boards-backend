import pytz
import uuid
import datetime
import jwt

from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from django.db.models.loading import get_model

from ..utils.jwt_handlers import jwt_payload_handler, jwt_encode_handler
from ..utils.validators import username_validator
from ..utils.models import BaseModel
from ..utils.decorators import autoconnect
from ..notifications.models import NotificationSetting
from ..notifications.signals import notify
from .utils import get_gravatar_url
from .managers import UserManager


def update_last_ip(sender, user, request, **kwargs):
    """
    A signal receiver which updates the last_ip for
    the user logging in.
    """
    user.last_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    user.save()
user_logged_in.connect(update_last_ip)


@autoconnect
class User(BaseModel, AbstractBaseUser):
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

    is_staff_help_text = _(
        'Designates whether the user can log into this admin site.'
    )

    is_active_help_text = _(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'
    )

    is_superuser_help_text = _('Designates that this user has all '
                               'permissions without explicitly '
                               'assigning them.')

    username = models.CharField(
        _('username'), max_length=30, unique=True,
        help_text=username_help_text, validators=[username_validator]
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)

    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    email = models.EmailField(_('email address'), max_length=254, unique=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=is_staff_help_text)

    is_superuser = models.BooleanField(
        _('superuser status'), default=False, help_text=is_superuser_help_text)

    is_active = models.BooleanField(
        _('active'), default=True, help_text=is_active_help_text)

    job_title = models.CharField(max_length=255, blank=True)
    avatar_path = models.TextField(blank=True)

    gravatar_url = models.URLField(blank=True)
    last_ip = models.IPAddressField(blank=True, null=True, default='127.0.0.1')
    timezone = models.CharField(
        max_length=255, default='UTC', choices=PRETTY_TIMEZONE_CHOICES)

    token_version = models.CharField(
        max_length=36, default=str(uuid.uuid4()), unique=True, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        announce = True

    def __str__(self):
        return self.username

    @property
    def announce_room(self):
        return 'u{}'.format(self.id)

    @property
    def serializer(self):
        from .serializers import UserSimpleSerializer
        return UserSimpleSerializer(self)

    def save(self, *args, **kwargs):
        if not self.pk or self.has_field_changed('email'):
            self.gravatar_url = get_gravatar_url(self.email)

        return super(User, self).save(*args, **kwargs)

    def post_save(self, created, *args, **kwargs):
        if created:
            NotificationSetting.create_default_settings(self)

        return super(User, self).post_save(created, *args, **kwargs)

    def has_perm(self, perm, obj=None):
        """
        Returns True if user is an active superuser.
        """
        if self.is_active and self.is_superuser:
            return True

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms
        for this object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if user is an active superuser.
        """
        if self.is_active and self.is_superuser:
            return True

    @property
    def token(self):
        """
        Returns a JSON Web Token used for Authentication.
        """
        payload = jwt_payload_handler(self)
        return jwt_encode_handler(payload)

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

    def change_password(self, raw_password):
        """
        Sets the user's password and changes token_version.
        """
        self.set_password(raw_password)
        self.reset_token_version()
        self.save()

    def reset_token_version(self):
        """
        Resets the user's token_version.
        """
        self.token_version = str(uuid.uuid4())

    def send_password_reset_email(self):
        actor = None
        recipients = [self]
        label = 'password_reset_requested'

        notify.send(
            actor,
            recipients=recipients,
            label=label,
            override_backends=('email', )
        )
