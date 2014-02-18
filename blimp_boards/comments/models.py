from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from ..utils.models import BaseModel


User = get_user_model()


class Comment(BaseModel):
    content = models.TextField()

    created_by = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "{}...".format(self.content[:50])
