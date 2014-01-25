from django.db import models


class AccountMemberManager(models.Manager):
    def create_owner(self, *args, **kwargs):
        kwargs.update({'role': 'owner'})
        return super(AccountMemberManager, self).create(*args, **kwargs)
