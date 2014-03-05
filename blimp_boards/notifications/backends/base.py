from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string


class BaseBackend(object):
    """
    The base backend.
    """
    def __init__(self, medium):
        self.medium = medium

    def can_send(self, user, notice_type):
        """
        Determines whether this backend is allowed to send a notification to
        the given user and notice_type.
        """
        from ..models import NotificationSetting

        if not user.pk:
            return True

        return NotificationSetting.for_user(
            user, notice_type, self.medium).send

    def deliver(self, recipient, sender, notice_type, extra_context):
        """
        Deliver a notification to the given recipient.
        """
        raise NotImplementedError()

    def get_formatted_messages(self, formats, label, context):
        """
        Returns a dictionary with the format identifier as the key.
        The values are are fully rendered templates with the given context.
        """
        format_templates = {}
        for fmt in formats:
            # conditionally turn off autoescaping for .txt extensions in format
            if fmt.endswith('.txt'):
                context.autoescape = False
            format_templates[fmt] = render_to_string((
                'notifications/%s/%s' % (label, fmt),
                'notifications/%s' % fmt), context_instance=context)
        return format_templates

    def default_context(self):
        return Context({
            'application_url': settings.APPLICATION_URL
        })
