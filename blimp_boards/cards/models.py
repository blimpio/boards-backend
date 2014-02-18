from django.db import models
from django.core.exceptions import ValidationError

from ..utils.models import BaseModel


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

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, **kwargs):
        """
        Performs all steps involved in validating  whenever
        a model object is saved.
        """
        self.full_clean()

        return super(Card, self).save(force_insert, force_update, **kwargs)

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
