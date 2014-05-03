from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import get_language, activate
from django.utils.log import getLogger

from model_utils import Choices
from model_utils.managers import PassThroughManager
from jsonfield import JSONField
from rest_framework.utils.encoders import JSONEncoder

from ..utils.models import BaseModel
from ..utils.date import timesince as timesince_
from .signals import notify
from .query import NotificationQuerySet
from .types import NOTIFICATION_TYPES, get_notification_type
from . import backends


logger = getLogger(__name__)

NOTIFICATION_TYPE_CHOICES = [
    (n['label'], n['display']) for n in NOTIFICATION_TYPES]

NOTIFICATION_BACKENDS = backends.load_backends()
NOTIFICATION_MEDIA, NOTIFICATION_MEDIA_DEFAULTS = \
    backends.load_media_defaults(backends=NOTIFICATION_BACKENDS)


class NotificationSetting(BaseModel):
    """
    Indicates, for a given user, whether to send notifications
    of a given type to a given medium.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))

    notification_type = models.CharField(
        _("notification type"), max_length=255,
        choices=NOTIFICATION_TYPE_CHOICES)

    medium = models.CharField(
        _("medium"), max_length=50, choices=NOTIFICATION_MEDIA)

    send = models.BooleanField(_("send"))

    class Meta:
        verbose_name = _("notification setting")
        verbose_name_plural = _("notification settings")
        unique_together = ("user", "notification_type", "medium")

    @classmethod
    def for_user(cls, user, notification_type, medium):
        data = {
            'user': user,
            'notification_type': notification_type,
            'medium': medium
        }

        obj, created = NotificationSetting.objects.get_or_create(
            defaults={'send': True}, **data)

        return obj

    @classmethod
    def create_default_settings(cls, user):
        settings = []
        for notification_type in NOTIFICATION_TYPES:
            for (key, value) in NOTIFICATION_MEDIA:
                setting = NotificationSetting(
                    user=user, notification_type=notification_type['label'],
                    medium=key, send=notification_type[key])

                settings.append(setting)

        return NotificationSetting.objects.bulk_create(settings)


class Notification(BaseModel):
    """
    Action model describing the actor acting out a verb
    on an optional target.

    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/

    Generalized Format::

        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <action_object> <target> <time>
    """
    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(choices=LEVELS, default='info', max_length=20)

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, related_name='notifications')
    unread = models.BooleanField(default=True, blank=False)

    actor_content_type = models.ForeignKey(
        ContentType, related_name='notify_actor')
    actor_object_id = models.PositiveIntegerField()
    actor = generic.GenericForeignKey('actor_content_type', 'actor_object_id')
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(
        ContentType, related_name='notify_target', blank=True, null=True)
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target = generic.GenericForeignKey(
        'target_content_type', 'target_object_id')

    action_object_content_type = models.ForeignKey(
        ContentType, related_name='notify_action_object',
        blank=True, null=True)
    action_object_object_id = models.PositiveIntegerField(
        blank=True, null=True)
    action_object = generic.GenericForeignKey(
        'action_object_content_type', 'action_object_object_id')

    public = models.BooleanField(default=True)

    data = JSONField(blank=True, null=True, dump_kwargs={
                     'cls': JSONEncoder, 'separators': (',', ':')})

    objects = PassThroughManager.for_queryset_class(NotificationQuerySet)()

    def __str__(self):
        context = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'target': self.target,
            'timesince': self.timesince()
        }

        if self.target and self.action_object:
            msg = '{actor} {verb} {action_object} on {target} {timesince} ago'
        elif self.target:
            msg = '{actor} {verb} {target} {timesince} ago'
        elif self.action_object:
            msg = '{actor} {verb} {action_object} {timesince} ago'
        else:
            msg = '{actor} {verb} {timesince} ago'

        return msg.format(**context)

    def timesince(self):
        return timesince_(self.date_created)


class LanguageStoreNotAvailable(Exception):
    pass


def get_notification_language(user):
    """
    Returns site-specific notification language for this user. Raises
    LanguageStoreNotAvailable if this site does not use translated
    notifications.
    """
    LANGUAGE_MODULE = getattr(settings, 'NOTIFICATION_LANGUAGE_MODULE', False)

    if LANGUAGE_MODULE:
        try:
            app_label, model_name = LANGUAGE_MODULE.split('.')
            model = models.get_model(app_label, model_name)
            language_model = model.objects.get(user__id__exact=user.id)
            if hasattr(language_model, 'language'):
                return language_model.language
        except (ImportError, ImproperlyConfigured, model.DoesNotExist):
            raise LanguageStoreNotAvailable
    raise LanguageStoreNotAvailable


@receiver(notify)
def notify_handler(sender, **kwargs):
    from ..utils.validators import is_valid_email
    """
    Example signal usage:

    actor = User.objects.first()
    recipients = User.objects.all().exclude(pk=actor.pk)
    label = 'comment_created'
    extra_context = {
        'action_object': Comment.objects.last(),
        'description': Comment.objects.last().content,
        'target': Comment.objects.last().content_object
    }

    notify.send(actor, recipients=recipients, label=label,
                extra_context=extra_context)
    """
    kwargs.pop('signal', None)

    recipients = kwargs.pop('recipients')
    label = kwargs.pop('label')
    extra_context = kwargs.pop('extra_context', {})
    override_backends = kwargs.pop('override_backends', None)
    notice_type = get_notification_type(label)
    current_language = get_language()
    sent = False

    if override_backends:
        backends = []

        for media in NOTIFICATION_MEDIA:
            if media[0] in override_backends:
                backends.append(NOTIFICATION_BACKENDS[media])
    else:
        backends = NOTIFICATION_BACKENDS.values()

    for user in recipients:
        if is_valid_email(user):
            class User(object):
                pk = None
                email = user

            user = User()

        # Get user language for user from language store
        try:
            language = get_notification_language(user)
        except LanguageStoreNotAvailable:
            language = None

        if language is not None:
            # Activate the user's language
            activate(language)

        for backend in backends:
            if backend.can_send(user, notice_type):
                msg = 'Delivering notification {} from {} to {} via {}'
                log = msg.format(notice_type, sender, user.email, backend)
                logger.info(log)

                backend.deliver(user, sender, notice_type, extra_context)

                sent = True

    # Reset environment to original language
    activate(current_language)

    return sent
