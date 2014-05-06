import positions

from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.db.models.loading import get_model
from django.db.models.signals import m2m_changed
from django.utils.functional import cached_property
from django.contrib.contenttypes.models import ContentType

from jsonfield import JSONField
from rest_framework.utils.encoders import JSONEncoder

from ..utils.models import BaseModel
from ..utils.decorators import autoconnect
from ..utils.fields import ReservedKeywordsAutoSlugField
from ..notifications.signals import notify
from ..files.previews import queue_previews
from ..files.utils import sign_s3_url
from .constants import CARD_RESERVED_KEYWORDS


@autoconnect
class Card(BaseModel):
    TYPE_CHOICES = (
        ('note', 'Note'),
        ('file', 'File'),
        ('stack', 'Stack'),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    slug = ReservedKeywordsAutoSlugField(
        editable=True, blank=True, populate_from='name',
        unique_with='board', reserved_keywords=CARD_RESERVED_KEYWORDS)

    board = models.ForeignKey('boards.Board')
    created_by = models.ForeignKey('users.User')
    modified_by = models.ForeignKey('users.User',
                                    related_name='%(class)s_modified_by')

    position = positions.PositionField(collection='board')
    objects = positions.PositionManager()

    stack = models.ForeignKey(
        'cards.Card', blank=True, null=True, related_name='+')
    cards = models.ManyToManyField(
        'cards.Card', blank=True, null=True, related_name='+')

    featured = models.BooleanField(default=False)
    origin_url = models.URLField(blank=True)
    content = models.TextField(blank=True)

    is_shared = models.BooleanField(default=False)

    thumbnail_sm_path = models.TextField(blank=True)
    thumbnail_md_path = models.TextField(blank=True)
    thumbnail_lg_path = models.TextField(blank=True)

    file_size = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=255, blank=True)

    data = JSONField(blank=True, null=True, dump_kwargs={
                     'cls': JSONEncoder, 'separators': (',', ':')})

    comments = generic.GenericRelation('comments.Comment')

    class Meta:
        announce = True
        ordering = ['position']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('card_detail', kwargs={
            'account_slug': self.board.account.slug,
            'board_slug': self.board.slug,
            'card_slug': self.slug})

    @cached_property
    def html_url(self):
        return '{}{}'.format(settings.APPLICATION_URL, self.get_absolute_url())

    @cached_property
    def announce_room(self):
        return 'a{}'.format(self.board.account_id)

    @cached_property
    def serializer_class(self):
        from .serializers import CardSerializer
        return CardSerializer

    @cached_property
    def serializer(self):
        return self.serializer_class(self)

    @property
    def download_url(self):
        if self.type == 'file':
            headers = {
                'response-content-disposition': 'attachment'
            }

            return sign_s3_url(self.content, headers)

    def save(self, *args, **kwargs):
        """
        Performs all steps involved in validating before
        model object is saved and sets modified_by
        from created_by when creating.
        """
        if not self.pk and not self.modified_by_id:
            self.modified_by = self.created_by

        self.full_clean()

        return super(Card, self).save(*args, **kwargs)

    def post_save(self, created, *args, **kwargs):
        # Detect if new card is a file and request thumbnails.
        if created and self.type == 'file' and self.content:
            self.request_previews()

        # Notify card was created
        if created:
            self.notify_created()

        super(Card, self).post_save(created, *args, **kwargs)

    def clean(self):
        """
        Validates when card is a stack, that card specific fields arent' set.
        """
        if self.type != 'stack':
            if not self.content:
                raise ValidationError('The `content` field is required.')

            return None

        disallowed_fields = [
            'origin_url', 'content', 'thumbnail_sm_path',
            'thumbnail_md_path', 'thumbnail_lg_path',
            'file_size', 'mime_type']

        for field in disallowed_fields:
            if getattr(self, field):
                msg = 'The `{}` field should not be set on a card stack.'
                raise ValidationError(msg.format(field))

    def get_signed_thumbnail(self, field_name):
        """
        Returns an AWS S3 signed URL with expiration.
        """
        field = getattr(self, field_name)

        if field:
            return sign_s3_url(field)

    def get_thumbnail_sm_path(self):
        return self.get_signed_thumbnail('thumbnail_sm_path')

    def get_thumbnail_md_path(self):
        return self.get_signed_thumbnail('thumbnail_md_path')

    def get_thumbnail_lg_path(self):
        return self.get_signed_thumbnail('thumbnail_lg_path')

    def request_previews(self):
        url = sign_s3_url(self.content)
        sizes = ['original', '200', '500', '800']
        metadata = {
            'cardId': self.id
        }

        return queue_previews(url, sizes, metadata)

    def update_notification_data(self):
        """
        Updates thumbnail fields in notifications where this
        card is an action_object.
        """
        Notification = get_model('notifications', 'Notification')

        card_type = ContentType.objects.get_for_model(Card)
        notifications = Notification.objects.filter(
            action_object_content_type=card_type,
            action_object_object_id=self.id)

        update_fields = ('thumbnail_sm_path', 'thumbnail_md_path',
                         'thumbnail_lg_path')

        serializer = self.serializer_class(self, fields=update_fields)

        for notification in notifications:
            notification.data['action_object'].update(serializer.data)
            notification.save()

    def notify_created(self):
        user = self.created_by

        actor = user
        recipients = [user]

        if self.type == 'stack':
            label = 'card_stack_created'
        else:
            label = 'card_created'

        extra_context = {
            'action_object': self,
            'target': self.board
        }

        notify.send(
            actor,
            recipients=recipients,
            label=label,
            extra_context=extra_context
        )

    def notify_featured(self, user):
        actor = user
        recipients = [user]
        label = 'card_featured'

        extra_context = {
            'action_object': self,
            'target': self.board
        }

        notify.send(
            actor,
            recipients=recipients,
            label=label,
            extra_context=extra_context
        )

    def notify_comment_created(self, user, comment):
        User = get_model('users', 'User')
        recipients = User.objects.filter(
            boardcollaborator__board__id=self.board_id).exclude(id=user.id)

        actor = user
        recipients = recipients
        label = 'card_comment_created'

        extra_context = {
            'action_object': comment,
            'description': comment.content,
            'target': self
        }

        notify.send(
            actor,
            recipients=recipients,
            label=label,
            extra_context=extra_context
        )


@receiver(m2m_changed, sender=Card.cards.through)
def cards_changed(sender, **kwargs):
    """
    Sets the `stack` field to reference a card's stack.
    """
    instance = kwargs['instance']
    action = kwargs['action']
    pk_set = kwargs['pk_set']

    if action == 'post_add':
        Card.objects.filter(pk__in=pk_set).update(stack=instance)
    elif action == 'post_remove':
        Card.objects.filter(pk__in=pk_set, stack=instance).update(stack=None)
    elif action == 'post_clear':
        Card.objects.filter(stack=instance).update(stack=None)
