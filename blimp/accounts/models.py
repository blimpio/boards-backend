import os
import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model

from ..users.models import User
from ..utils.slugify import unique_slugify
from .managers import AccountCollaboratorManager
from .constants import COMPANY_RESERVED_KEYWORDS


def get_company_upload_path(instance, filename):
    identifier = str(uuid.uuid4())
    return os.path.join(
        'uploads', 'companies', str(instance.pk), identifier, filename)


class EmailDomain(models.Model):
    domain_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.domain_name


class Account(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image_url = models.ImageField(
        upload_to=get_company_upload_path, blank=True)
    allow_signup = models.BooleanField(default=False)
    email_domains = models.ManyToManyField(EmailDomain, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            pre_slug = slugify(self.name)
            if not self.pk or pre_slug != self.slug:
                if pre_slug in COMPANY_RESERVED_KEYWORDS:
                    pre_slug = '%s1' % pre_slug
                else:
                    pre_slug = self.name
                unique_slugify(self, pre_slug)
        return super(Account, self).save()

    def add_email_domains(self, email_domains):
        for domain in email_domains:
            self.email_domains.create(domain_name=domain)

    def invite_user(self, user_data):
        """
        Receives dictionary of InvitedUser fields
        and returns a tuple of InvitedUser, created.
        """
        InvitedUser = get_model('invitations', 'InvitedUser')

        invited_user, created = InvitedUser.objects.get_or_create(
            account=self, defaults=user_data, **user_data)

        invited_user.send_invite()

        return invited_user, created


class AccountCollaborator(models.Model):
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    is_owner = models.BooleanField(default=False)

    objects = AccountCollaboratorManager()

    def __str__(self):
        return self.user.get_full_name() or self.user.email
