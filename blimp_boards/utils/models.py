from django.db import models
from django.conf import settings
from django.utils.encoding import smart_text

from announce import Announce
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers

from .fields import DateTimeCreatedField, DateTimeModifiedField


models.options.DEFAULT_NAMES += ('announce', )


def json_renderer(data):
    return smart_text(JSONRenderer().render(data))


class BaseModel(models.Model):
    """
    An abstract base class model that provides:
        - date_created
        - date_modified
    """
    date_created = DateTimeCreatedField()
    date_modified = DateTimeModifiedField()

    class Meta:
        get_latest_by = 'date_modified'
        ordering = ('-date_modified', '-date_created',)
        abstract = True

    def to_dict(self):
        """
        Returns a dictionary representation of the model using
        REST framework's model serializers. Uses a specified serializer
        on the model or defaults to a generic ModelSerializer.
        """
        try:
            serializer = self.serializer
        except:
            class ModelSerializer(serializers.ModelSerializer):
                class Meta:
                    model = self.__class__

            serializer = ModelSerializer(self)

        return serializer.data

    def announce(self, method):
        """
        Announces to SocketIO Redis store that a model has changed.
        Includes the model name as a data_type, method, and a serialized
        representation of the model instance.
        """
        room = self.announce_room

        data = {
            'data_type': self.__class__.__name__.lower(),
            'method': method,
            'data': self.to_dict()
        }

        announce = Announce(
            json_dumps=json_renderer,
            _test_mode=settings.ANNOUNCE_TEST_MODE)

        announce.emit('message', data, room=room)

    def post_save(self, created, **kwargs):
        """
        If model's Meta class has `announce = True`, announces
        when a model instance is created or updated.
        """
        if self._meta.announce:
            method = 'create' if created else 'update'
            self.announce(method)

    def post_delete(self, **kwargs):
        """
        If model's Meta class has `announce = True`, announces
        when a model instance deleted.
        """
        if self._meta.announce:
            self.announce('delete')
