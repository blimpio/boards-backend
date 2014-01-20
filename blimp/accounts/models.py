import os
import uuid

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

from blimp.users.models import User
from blimp.utils.slugify import unique_slugify
from blimp.invitations.models import InvitedUser
from .constants import MEMBER_ROLES


def get_company_upload_path(instance, filename):
    identifier = str(uuid.uuid4())
    return os.path.join(
        'uploads', 'companies', str(instance.pk), identifier, filename)


class AccountMemberManager(models.Manager):
    def create_owner(self, *args, **kwargs):
        kwargs.update({'role': 'owner'})
        return super(AccountMemberManager, self).create(*args, **kwargs)


class EmailDomain(models.Model):
    domain_name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.domain_name


class Account(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image_url = models.ImageField(
        upload_to=get_company_upload_path, blank=True)
    allow_signup = models.BooleanField(default=False)
    email_domains = models.ManyToManyField(EmailDomain, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            pre_slug = slugify(self.name)
            if not self.pk or pre_slug != self.slug:
                if pre_slug in settings.COMPANY_RESERVED_KEYWORDS:
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
        Receives a list of dictionaries of InvitedUser fields
        and returns a list of InvitedUser.
        """
        email = user_data.pop('email')

        return InvitedUser.objects.get_or_create(
            email=email, account=self, defaults=user_data)


class AccountMember(models.Model):
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=25, choices=MEMBER_ROLES)

    objects = AccountMemberManager()

    def __unicode__(self):
        return self.user.get_full_name() or self.user.email
