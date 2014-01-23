import re
import pytz
import uuid
import os
from datetime import datetime

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.core.mail import send_mail
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone

from django_extensions.db.fields import UUIDField


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
        now = datetime.now(pytz.timezone(tz))
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

    token_version = UUIDField()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
