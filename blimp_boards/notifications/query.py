from django.db.models.query import QuerySet


class NotificationQuerySet(QuerySet):
    def unread(self):
        """
        Return only unread items in the current queryset
        """
        return self.filter(unread=True)

    def read(self):
        """
        Return only read items in the current queryset
        """
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """
        Mark as read any unread messages in the current queryset.
        Optionally, filter these by recipient first.
        """
        qs = self.unread()

        if recipient:
            qs = qs.filter(recipient=recipient)

        qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """
        Mark as unread any read messages in the current queryset.
        Optionally, filter these by recipient first.
        """
        qs = self.read()

        if recipient:
            qs = qs.filter(recipient=recipient)

        qs.update(unread=True)
