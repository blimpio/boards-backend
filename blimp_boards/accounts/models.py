from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.loading import get_model
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property

from ..users.models import User
from ..utils.decorators import autoconnect
from ..utils.fields import ReservedKeywordsAutoSlugField
from ..utils.models import BaseModel
from .constants import ACCOUNT_RESERVED_KEYWORDS
from . import managers


@python_2_unicode_compatible
class EmailDomain(BaseModel):
    domain_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.domain_name


@autoconnect
@python_2_unicode_compatible
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

    created_by = models.ForeignKey('users.User')
    modified_by = models.ForeignKey('users.User',
                                    related_name='%(class)s_modified_by')

    objects = models.Manager()
    personals = managers.PersonalAccountManager()
    teams = managers.TeamAccountManager()

    class Meta:
        announce = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('account_detail', kwargs={'account_slug': self.slug})

    @cached_property
    def html_url(self):
        return '{}{}'.format(settings.APPLICATION_URL, self.get_absolute_url())

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
        Performs all steps involved in validating before
        model object is saved and sets modified_by
        from created_by when creating.
        """
        if not self.pk and not self.modified_by_id:
            self.modified_by = self.created_by

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


@python_2_unicode_compatible
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
        return self.user.full_name or self.user.email
