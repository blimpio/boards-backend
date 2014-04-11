import os
import uuid

from django.db import models
from django.db.models.loading import get_model
from django.core.exceptions import ValidationError

from ..users.models import User
from ..utils.models import BaseModel
from ..utils.decorators import autoconnect
from ..utils.fields import ReservedKeywordsAutoSlugField
from .constants import ACCOUNT_RESERVED_KEYWORDS
from . import managers


def get_company_upload_path(instance, filename):
    identifier = str(uuid.uuid4())
    return os.path.join(
        'uploads', 'companies', str(instance.pk), identifier, filename)


class EmailDomain(BaseModel):
    domain_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.domain_name


@autoconnect
class Account(BaseModel):
    PERSONAL_ACCOUNT = 'personal'
    TEAM_ACCOUNT = 'team'

    ACCOUNT_TYPE_CHOICES = (
        (PERSONAL_ACCOUNT, 'Personal'),
        (TEAM_ACCOUNT, 'Team'),
    )

    name = models.CharField(max_length=255)
    slug = ReservedKeywordsAutoSlugField(
        populate_from='name', blank=True, unique=True, editable=True,
        reserved_keywords=ACCOUNT_RESERVED_KEYWORDS)

    type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)

    allow_signup = models.BooleanField(default=False)
    email_domains = models.ManyToManyField(EmailDomain, blank=True, null=True)

    logo_color = models.CharField(max_length=255, blank=True)
    disqus_shortname = models.CharField(max_length=255, blank=True)

    objects = models.Manager()
    personals = managers.PersonalAccountManager()
    teams = managers.TeamAccountManager()

    class Meta:
        announce = True

    def __str__(self):
        return self.name

    @property
    def announce_room(self):
        return 'a{}'.format(self.id)

    @property
    def serializer(self):
        from .serializers import AccountSerializer
        return AccountSerializer(self)

    @property
    def owner(self):
        return AccountCollaborator.objects.select_related(
            'user').get(account=self, is_owner=True)

    @property
    def boards(self):
        Board = get_model('boards', 'Board')

        return Board.objects.filter(account=self)

    def save(self, *args, **kwargs):
        """
        Performs all steps involved in validating  whenever
        a model object is saved.
        """
        self.full_clean()

        return super(Account, self).save(*args, **kwargs)

    def clean(self):
        """
        Validates that either a user or an invited_user is set.
        """
        if not self.type:
            raise ValidationError('Account type is required.')

    def add_email_domains(self, email_domains):
        for domain in email_domains:
            self.email_domains.create(domain_name=domain)

    def invite_user(self, user_data):
        """
        Returns a tuple (invited_user, created) after creating
        an InvitedUser, if one does not yet exist for user_data,
        and send the invited user email.
        """
        InvitedUser = get_model('invitations', 'InvitedUser')

        invited_user, created = InvitedUser.objects.get_or_create(
            account=self, defaults=user_data, **user_data)

        invited_user.send_invite()

        return invited_user, created

    def is_user_collaborator(self, user, is_owner=None):
        """
        Returns `True` if a user is a collaborator on this
        Account, `False` otherwise. Optionally checks if a user
        is the account owner.
        """
        collaborators = AccountCollaborator.objects.filter(
            account=self, user=user)

        if is_owner is not None:
            collaborators = collaborators.filter(is_owner=is_owner)

        return collaborators.exists()


class AccountCollaborator(BaseModel):
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    is_owner = models.BooleanField(default=False)

    objects = managers.AccountCollaboratorManager()

    class Meta:
        unique_together = (
            ('account', 'user')
        )

    def __str__(self):
        return self.user.get_full_name() or self.user.email
