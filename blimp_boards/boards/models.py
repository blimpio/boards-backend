from copy import deepcopy

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.loading import get_model
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.log import getLogger

from ..files.utils import sign_s3_url
from ..notifications.signals import notify
from ..utils.decorators import autoconnect
from ..utils.fields import ReservedKeywordsAutoSlugField
from ..utils.models import BaseModel
from .constants import BOARD_RESERVED_KEYWORDS


logger = getLogger(__name__)


@autoconnect
@python_2_unicode_compatible
class Board(BaseModel):
    name = models.CharField(max_length=255)
    slug = ReservedKeywordsAutoSlugField(
        populate_from='name', unique_with='account', editable=True,
        reserved_keywords=BOARD_RESERVED_KEYWORDS)

    account = models.ForeignKey('accounts.Account')
    created_by = models.ForeignKey('users.User')
    modified_by = models.ForeignKey('users.User',
                                    related_name='%(class)s_modified_by')

    is_shared = models.BooleanField(default=False)

    color = models.CharField(max_length=255, blank=True)

    thumbnail_xs_path = models.TextField(blank=True, null=True)
    thumbnail_sm_path = models.TextField(blank=True, null=True)
    thumbnail_md_path = models.TextField(blank=True, null=True)
    thumbnail_lg_path = models.TextField(blank=True, null=True)

    class Meta:
        announce = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board_detail', kwargs={
            'account_slug': self.account.slug,
            'board_slug': self.slug})

    @cached_property
    def html_url(self):
        return '{}{}'.format(settings.APPLICATION_URL, self.get_absolute_url())

    @cached_property
    def activity_html_url(self):
        activity_url = reverse('account_board_activity', kwargs={
            'account_slug': self.account.slug,
            'board_slug': self.slug,
        })

        return '{}{}'.format(settings.APPLICATION_URL, activity_url)

    @cached_property
    def announce_room(self):
        return 'a{}'.format(self.account_id)

    @cached_property
    def serializer(self):
        from .serializers import BoardSerializer
        return BoardSerializer(self)

    @property
    def signed_thumbnail_xs_path(self):
        if self.thumbnail_xs_path:
            return sign_s3_url(self.thumbnail_xs_path)

    @property
    def signed_thumbnail_sm_path(self):
        if self.thumbnail_sm_path:
            return sign_s3_url(self.thumbnail_sm_path)

    @property
    def signed_thumbnail_md_path(self):
        if self.thumbnail_md_path:
            return sign_s3_url(self.thumbnail_md_path)

    @property
    def signed_thumbnail_lg_path(self):
        if self.thumbnail_lg_path:
            return sign_s3_url(self.thumbnail_lg_path)

    @cached_property
    def file_card(self):
        """
        Returns board's first card of type file.
        """
        return self.card_set.filter(type='file').first()

    @property
    def card_thumbnail_xs_path(self):
        if self.file_card:
            return self.file_card.signed_thumbnail_xs_path

    @property
    def card_thumbnail_sm_path(self):
        if self.file_card:
            return self.file_card.signed_thumbnail_sm_path

    @property
    def card_thumbnail_md_path(self):
        if self.file_card:
            return self.file_card.signed_thumbnail_md_path

    @property
    def card_thumbnail_lg_path(self):
        if self.file_card:
            return self.file_card.signed_thumbnail_lg_path

    def save(self, *args, **kwargs):
        """
        Sets modified_by from created_by when creating.
        """
        if not self.pk and not self.modified_by_id:
            self.modified_by_id = self.created_by_id

        return super(Board, self).save(*args, **kwargs)

    def clean(self):
        """
        Sets nullable string fields back to empty strings
        """
        string_fields = [
            'thumbnail_xs_path', 'thumbnail_sm_path',
            'thumbnail_md_path', 'thumbnail_lg_path'
        ]

        for field in string_fields:
            if field is None:
                setattr(self, field, '')

    def post_save(self, created, *args, **kwargs):
        """
        Create BoardCollaborator for account owner and user creating board.
        """
        if created:
            account_owner = self.account.owner.user

            BoardCollaborator.objects.create(
                board=self,
                user=account_owner,
                created_by_id=self.created_by_id,
                permission=BoardCollaborator.WRITE_PERMISSION
            )

            if account_owner != self.created_by:
                BoardCollaborator.objects.create(
                    board=self,
                    user_id=self.created_by_id,
                    created_by_id=self.created_by_id,
                    permission=BoardCollaborator.WRITE_PERMISSION
                )

        super(Board, self).post_save(created, *args, **kwargs)

    def is_user_collaborator(self, user, permission=None):
        """
        Returns `True` if a user is a collaborator on this
        Board, `False` otherwise. Optionally checks if a user
        is a collaborator with a specific permission.
        """
        collaborators = BoardCollaborator.objects.filter(board=self, user=user)
        read_permission = BoardCollaborator.READ_PERMISSION
        write_permission = BoardCollaborator.WRITE_PERMISSION

        if permission == read_permission:
            collaborators = collaborators.filter(
                Q(permission=write_permission) | Q(permission=read_permission))
        elif permission == write_permission:
            collaborators = collaborators.filter(permission=write_permission)

        return collaborators.exists()

    @classmethod
    def create_demo_board(cls, account, user):
        try:
            board = Board.objects.get(pk=settings.BOARDS_DEMO_BOARD_ID)
        except Exception as e:
            logger.exception(e)
            return None

        return board.clone(account, user)

    def clone(self, account, user):
        """
        Clones a board to another account using a given user for User FKs.
        """
        board = deepcopy(self)
        cards = board.card_set.all()

        board.pk = None
        board.id = None
        board.account = account
        board.created_by_id = user.id
        board.modified_by_id = user.id
        board.set_revisions(False)
        board.save()

        for card in cards:
            comments = card.comments.all()
            card.pk = None
            card.id = None
            card.board = board
            card.created_by = user
            card.modified_by = user
            card.set_revisions(False)
            card.save()

            for comment in comments:
                comment.pk = None
                comment.id = None
                comment.content_object = card
                comment.created_by = user
                comment.modified_by = user
                comment.set_revisions(False)
                comment.save()

        return board


@autoconnect
class BoardCollaborator(BaseModel):
    READ_PERMISSION = 'read'
    WRITE_PERMISSION = 'write'

    PERMISSION_CHOICES = (
        (READ_PERMISSION, 'Read'),
        (WRITE_PERMISSION, 'Read and Write'),
    )

    board = models.ForeignKey('boards.Board')
    user = models.ForeignKey('users.User', blank=True, null=True)
    invited_user = models.ForeignKey(
        'invitations.InvitedUser', blank=True, null=True)

    created_by = models.ForeignKey(
        'users.User', related_name='%(class)s_created_by')

    modified_by = models.ForeignKey(
        'users.User', related_name='%(class)s_modified_by')

    permission = models.CharField(max_length=5, choices=PERMISSION_CHOICES)

    class Meta:
        announce = True
        unique_together = (
            ('board', 'user'),
            ('board', 'invited_user'),
        )

    def __str__(self):
        return str(self.user) if self.user else str(self.invited_user)

    @cached_property
    def announce_room(self):
        return 'a{}'.format(self.board.account_id)

    @cached_property
    def serializer(self):
        from .serializers import BoardCollaboratorSerializer
        return BoardCollaboratorSerializer(self)

    @property
    def email(self):
        if self.user:
            return self.user.email
        elif self.invited_user:
            return self.invited_user.email

    def save(self, force_insert=False, force_update=False, **kwargs):
        """
        Performs all steps involved in validating  whenever
        a model object is saved.
        """
        AccountCollaborator = get_model('accounts', 'AccountCollaborator')

        if not self.pk and self.user_id:
            # Make sure BoardCollaborator has an AccountCollaborator
            AccountCollaborator.objects.get_or_create(
                user_id=self.user_id, account_id=self.board.account_id)

        if not self.pk and not self.modified_by_id:
            self.modified_by_id = self.created_by_id

        self.full_clean()

        return super(BoardCollaborator, self).save(
            force_insert, force_update, **kwargs)

    def clean(self):
        """
        Validates that either a user or an invited_user is set.
        """
        if self.user_id and self.invited_user_id:
            raise ValidationError(
                'Both user and invited_user cannot be set together.')
        elif not self.user_id and not self.invited_user_id:
            raise ValidationError('Either user or invited_user must be set.')

    def post_save(self, created, *args, **kwargs):
        if created and self.user_id and self.user_id != self.created_by_id:
            self.notify_created()

        super(BoardCollaborator, self).post_save(created, *args, **kwargs)

    def notify_created(self):
        actor = self.created_by
        recipients = [self.user]

        label = 'board_collaborator_created'

        extra_context = {
            'action_object': self,
            'target': self.board
        }

        notify.send(
            actor,
            recipients=recipients,
            label=label,
            extra_context=extra_context
        )


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

    def post_save(self, created, *args, **kwargs):
        # Notify account owner
        if created:
            self.notify_account_owner()

        super(BoardCollaboratorRequest, self).post_save(
            created, *args, **kwargs)

    def accept(self):
        """
        - Creates an InvitedUser for this board
        - Creates a BoardCollaborator for invited_user
        - Sets it in the InvitedUser.board_collaborator
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
            permission=BoardCollaborator.READ_PERMISSION,
            created_by=self.board.account.owner.user
        )

        invited_user.board_collaborator = board_collaborator
        invited_user.save()

        invited_user.send_invite()

        self.delete()

    def reject(self):
        """
        Deletes BoardCollaboratorRequest.
        """
        self.delete()

    def notify_account_owner(self):
        actor = None
        recipients = [self.email]
        label = 'board_collaborator_requested'

        extra_context = {
            'action_object': self,
        }

        notify.send(
            actor,
            recipients=recipients,
            label=label,
            extra_context=extra_context,
            override_backends=('email', )
        )
