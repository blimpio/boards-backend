from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic

from ..utils.models import BaseModel
from ..utils.decorators import autoconnect
from ..utils.fields import ReservedKeywordsAutoSlugField
from .constants import CARD_RESERVED_KEYWORDS


@autoconnect
class Card(BaseModel):
    TYPE_CHOICES = (
        ('note', 'Note'),
        ('link', 'Link'),
        ('text', 'Text'),
        ('file', 'File'),
        ('embed', 'Embeddable'),
        ('stack', 'Stack'),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    slug = ReservedKeywordsAutoSlugField(
        editable=True, blank=True, populate_from='name',
        unique_with='board', reserved_keywords=CARD_RESERVED_KEYWORDS)

    board = models.ForeignKey('boards.Board')
    cards = models.ManyToManyField('cards.Card', blank=True, null=True)
    created_by = models.ForeignKey('users.User')

    featured = models.BooleanField(default=False)
    origin_url = models.URLField(blank=True)
    content = models.TextField(blank=True)

    is_shared = models.BooleanField(default=False)

    thumbnail_sm_path = models.TextField(blank=True)
    thumbnail_md_path = models.TextField(blank=True)
    thumbnail_lg_path = models.TextField(blank=True)

    file_size = models.IntegerField(null=True, blank=True)
    file_extension = models.CharField(max_length=5, blank=True)

    comments = generic.GenericRelation('comments.Comment')

    class Meta:
        announce = True

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
            'file_size', 'file_extension']

        for field in disallowed_fields:
            if getattr(self, field):
                msg = 'The `{}` field should not be set on a card stack.'
                raise ValidationError(msg.format(field))
