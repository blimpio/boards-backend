from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ..utils.decorators import autoconnect
from ..utils.models import BaseModel


@autoconnect
@python_2_unicode_compatible
class Comment(BaseModel):
    content = models.TextField()

    created_by = models.ForeignKey('users.User')
    modified_by = models.ForeignKey('users.User',
                                    related_name='%(class)s_modified_by')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        announce = True

    def __str__(self):
        return "{}...".format(self.content[:50])

    @property
    def announce_room(self):
        return self.content_object.announce_room

    @property
    def serializer(self):
        from .serializers import CommentSerializer
        return CommentSerializer(self)

    def save(self, *args, **kwargs):
        """
        Sets modified_by from created_by when creating.
        """
        if not self.pk and not self.modified_by_id:
            self.modified_by_id = self.created_by_id

        return super(Comment, self).save(*args, **kwargs)
