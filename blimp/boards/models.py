from django.db import models

from blimp.utils.models import BaseModel


class Board(BaseModel):
    name = models.CharField(max_length=255)

    created_by = models.ForeignKey('users.User')

    is_shared = models.BooleanField(default=False)

    thumbnail_sm_path = models.TextField(blank=True)
    thumbnail_md_path = models.TextField(blank=True)
    thumbnail_lg_path = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_thumbnail_url(self, size='sm'):
        """
        Returns full thumbnail url.
        BUCKET_URL + thumbnail path
        """
        pass


class BoardCollaborator(BaseModel):
    PERMISSION_CHOICES = (
        ('read', 'Read'),
        ('write', 'Read and Write'),
    )

    user = models.ForeignKey('users.User')
    board = models.ForeignKey('boards.Board')

    permission = models.CharField(max_length=5, choices=PERMISSION_CHOICES)

    def __str__(self):
        return self.user
