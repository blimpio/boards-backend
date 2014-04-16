from django.db import models


class PersonalAccountManager(models.Manager):
    def get_queryset(self):
        queryset = super(PersonalAccountManager, self).get_queryset()
        return queryset.filter(type=self.model.PERSONAL_ACCOUNT)

    def create(self, *args, **kwargs):
        kwargs.update({'type': self.model.PERSONAL_ACCOUNT})
        return super(PersonalAccountManager, self).create(*args, **kwargs)


class TeamAccountManager(models.Manager):
    def get_queryset(self):
        queryset = super(TeamAccountManager, self).get_queryset()
        return queryset.filter(type=self.model.TEAM_ACCOUNT)

    def create(self, *args, **kwargs):
        kwargs.update({'type': self.model.TEAM_ACCOUNT})
        return super(TeamAccountManager, self).create(*args, **kwargs)


class AccountCollaboratorManager(models.Manager):
    def create_owner(self, *args, **kwargs):
        kwargs.update({'is_owner': True})
        return super(AccountCollaboratorManager, self).create(*args, **kwargs)
