from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .base import BaseBackend


class EmailBackend(BaseBackend):
    def can_send(self, user, notification_type):
        can_send = super(EmailBackend, self).can_send(user, notification_type)

        if can_send and user.email:
            return True

        return False

    def deliver(self, recipient, sender, notification_type, extra_context):
        context = self.default_context()
        context.update({
            'recipient': recipient,
            'sender': sender,
            'notification_type': notification_type,
        })
        context.update(extra_context)

        messages = self.get_formatted_messages((
            'subject.txt',
            'body.txt',
            'body.html'
        ), notification_type.label, context)

        subject = messages['subject.txt']
        text_content = messages['body.txt']
        html_content = messages['body.html']
        from_email = settings.DEFAULT_FROM_EMAIL
        recipients = [recipient.email]

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            recipients
        )

        msg.attach_alternative(html_content, "text/html")

        msg.send()
