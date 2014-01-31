from django.db import models

from blimp.utils.models import BaseModel


class Stack(BaseModel):
    name = models.CharField(max_length=255)

    board = models.ForeignKey('boards.Board')
    created_by = models.ForeignKey('users.User')

    is_shared = models.BooleanField(default=False)

    thumbnail_sm_path = models.TextField(blank=True)
    thumbnail_md_path = models.TextField(blank=True)
    thumbnail_lg_path = models.TextField(blank=True)

    def __str__(self):
        return self.name
