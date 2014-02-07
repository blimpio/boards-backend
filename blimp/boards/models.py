from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.loading import get_model
from django.core.mail import send_mail

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

    class Meta:
        unique_together = (
            ('board', 'user'),
            ('board', 'invited_user'),
        )

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


class BoardCollaboratorRequest(BaseModel):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    user = models.ForeignKey('users.User', blank=True, null=True)
    board = models.ForeignKey('boards.Board')
    message = models.TextField(blank=True)

    class Meta:
        unique_together = (
            ('email', 'board'),
            ('user', 'board'),
        )

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """
        When saving a BoardCollaboratorRequest, try to set first_name,
        last_name, and email if a user is given. If no user is given,
        try to find an existing user with matching email.
        """
        User = get_model('users', 'User')

        if not self.user:
            try:
                self.user = User.objects.get(email=self.email)
            except User.DoesNotExist:
                pass

        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
            self.email = self.user.email

        self.full_clean()

        return super(BoardCollaboratorRequest, self).save(*args, **kwargs)

    def clean(self):
        """
        Validates that either a user or an email is set.
        """
        if not self.user and not self.email:
            raise ValidationError('Either user or email must be set.')

    def accept(self):
        """
        - Creates an InvitedUser for this board
        - Creates a BoardCollaborator for invited_user
        - Sets it in the InvitedUser.board_collaborators
        - Sends invitation
        - Deletes BoardCollaboratorRequest
        """
        InvitedUser = get_model('invitations', 'InvitedUser')

        invited_user_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'user': self.user,
            'account': self.board.account,
            'created_by': self.board.account.owner.user,
        }

        invited_user = InvitedUser.objects.create(**invited_user_data)

        board_collaborator = BoardCollaborator.objects.create(
            board=self.board,
            invited_user=invited_user,
            permission=READ_PERMISSION
        )

        invited_user.board_collaborators.add(board_collaborator)

        invited_user.send_invite()

        self.delete()

    def reject(self):
        """
        Deletes BoardCollaboratorRequest.
        """
        self.delete()

    def notify_account_owner(self):
        message = '{} wants to join your board'.format(self.email)

        return send_mail(
            'Blimp Board Collaborator Request',
            message,
            'from@example.com',
            [self.email],
            fail_silently=False
        )
