from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save

from ..utils.models import BaseModel
from .constants import PERMISSION_CHOICES, READ_PERMISSION, WRITE_PERMISSION


class Board(BaseModel):
    name = models.CharField(max_length=255)

    account = models.ForeignKey('accounts.Account')
    created_by = models.ForeignKey('users.User')

    is_shared = models.BooleanField(default=False)

    thumbnail_sm_path = models.TextField(blank=True)
    thumbnail_md_path = models.TextField(blank=True)
    thumbnail_lg_path = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_thumbnail_url(self, size='sm'):
        """
        Returns full thumbnail url.
        BUCKET_URL + thumbnail path
        """
        pass

    def is_user_collaborator(self, user, permission=None):
        """
        Returns `True` if a user is a collaborator on this
        Board, `False` otherwise. Optionally checks if a user
        is a collaborator with a specific permission.
        """
        collaborators = BoardCollaborator.objects.filter(board=self, user=user)

        if permission == READ_PERMISSION:
            collaborators = collaborators.filter(
                Q(permission=WRITE_PERMISSION) | Q(permission=READ_PERMISSION))
        elif permission == WRITE_PERMISSION:
            collaborators = collaborators.filter(permission=WRITE_PERMISSION)

        return collaborators.exists()


@receiver([post_save], sender=Board)
def create_owner_collaborator(instance, created=False, **kwargs):
    """
    Create BoardCollaborator for account owner after creating a Board.
    """
    if created:
        account_owner = instance.account.owner

        BoardCollaborator.objects.create(
            board=instance,
            user=account_owner.user,
            permission=WRITE_PERMISSION
        )


class BoardCollaborator(BaseModel):
    board = models.ForeignKey('boards.Board')
    user = models.ForeignKey('users.User', blank=True, null=True)
    invited_user = models.ForeignKey('invitations.Inviteduser',
                                     blank=True, null=True)

    permission = models.CharField(max_length=5, choices=PERMISSION_CHOICES)

    def __str__(self):
        return str(self.user) if self.user else str(self.invited_user)

    def save(self, force_insert=False, force_update=False, **kwargs):
        """
        Performs all steps involved in validating  whenever
        a model object is saved, but not forced.
        """
        if not (force_insert or force_update):
            self.full_clean()

        return super(BoardCollaborator, self).save(
            force_insert, force_update, **kwargs)

    def clean(self):
        """
        Validates that either a user or an invited_user is set.
        """
        if self.user and self.invited_user:
            raise ValidationError(
                'Both user and invited_user cannot be set together.')
        elif not self.user and not self.invited_user:
            raise ValidationError('Either user or invited_user must be set.')
