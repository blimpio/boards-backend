import positions

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic
from django.db.models.loading import get_model
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

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

    comments = generic.GenericRelation('comments.Comment')

    class Meta:
        announce = True
        ordering = ['position']

    def __str__(self):
        return self.name

    @property
    def announce_room(self):
        return 'a{}'.format(self.board.account_id)

    @property
    def serializer(self):
        from .serializers import CardSerializer
        return CardSerializer(self)

    def pre_save(self, *args, **kwargs):
        """
        Performs all steps involved in validating before
        model object is saved.
        """
        self.full_clean()

    def post_save(self, created, *args, **kwargs):
        # Detect if new card is a file and request thumbnails.
        if created and self.type == 'file' and self.content:
            url = sign_s3_url(self.content)
            sizes = ['200', '500', '800']
            metadata = {
                'cardId': self.id
            }

            queue_previews(url, sizes, metadata)

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
