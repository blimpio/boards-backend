from django.db import models


class AccountCollaboratorManager(models.Manager):
    def create_owner(self, *args, **kwargs):
        kwargs.update({'is_owner': True})
        return super(AccountCollaboratorManager, self).create(*args, **kwargs)
