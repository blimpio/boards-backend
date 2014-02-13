from django.db import models

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
    content = models.TextField()

    is_shared = models.BooleanField(default=False)

    thumbnail_sm_path = models.TextField(blank=True)
    thumbnail_md_path = models.TextField(blank=True)
    thumbnail_lg_path = models.TextField(blank=True)

    file_size = models.IntegerField(null=True, blank=True)
    file_extension = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.name
