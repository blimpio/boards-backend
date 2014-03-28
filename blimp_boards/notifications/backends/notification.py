from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext
from django.db.models.loading import get_model

from .base import BaseBackend


class NotificationBackend(BaseBackend):
    def deliver(self, recipient, sender, notice_type, extra_context):
        Notification = get_model('notifications', 'Notification')

        notification = Notification(
            recipient=recipient,
            actor_content_type=ContentType.objects.get_for_model(sender),
            actor_object_id=sender.pk,
            verb=notice_type['description'],
            public=extra_context.get('public', True),
            description=extra_context.get('description', None)
        )

        for opt in ('target', 'action_object'):
            obj = extra_context.get(opt, None)

            extra_context[opt] = obj.serializer.data

            if not obj is None:
                setattr(notification, '{}_object_id'.format(opt), obj.pk)
                setattr(notification, '{}_content_type'.format(opt),
                        ContentType.objects.get_for_model(obj))

        extra_context.update({
            "recipient": recipient.serializer.data,
            "sender": sender.serializer.data,
            "notice": ugettext(notice_type['display']),
        })

        notification.data = extra_context

        notification.save()
