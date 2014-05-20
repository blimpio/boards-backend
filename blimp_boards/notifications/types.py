from django.utils.translation import ugettext_lazy as _


NOTIFICATION_TYPES = [
    {
        'label': 'card_comment_created',
        'display': _('Comment created'),
        'description': _('commented'),
        'email': True,
        'notification': True,
        'toggable': True,
    },
    {
        'label': 'signup_request_created',
        'display': _('Signup Request Created'),
        'description': _('invited'),
        'email': True,
        'notification': False,
        'toggable': False,
    },
    {
        'label': 'user_invited',
        'display': _('Invited to join account'),
        'description': _('invited'),
        'email': True,
        'notification': False,
        'toggable': False,
    },
    {
        'label': 'board_collaborator_requested',
        'display': _('Blimp Board Collaborator Request'),
        'description': _('wants to join your board'),
        'email': True,
        'notification': False,
        'toggable': False,
    },
    {
        'label': 'password_reset_requested',
        'display': _('Password Reset'),
        'description': _('reset your password'),
        'email': True,
        'notification': False,
        'toggable': False,
    },
    {
        'label': 'card_created',
        'display': _('Card created'),
        'description': _('created a card on board'),
        'email': False,
        'notification': True,
        'toggable': False,
    },
    {
        'label': 'card_featured',
        'display': _('Card highlighted'),
        'description': _('highlighted'),
        'email': False,
        'notification': True,
        'toggable': False,
    },
    {
        'label': 'card_stack_created',
        'display': _('Stack created'),
        'description': _('created a stack'),
        'email': False,
        'notification': True,
        'toggable': False,
    },
    {
        'label': 'board_collaborator_created',
        'display': _('New board collaborator'),
        'description': _('is now a collaborator on board'),
        'email': True,
        'notification': True,
        'toggable': True,
    },
    {
        'label': 'user_password_updated',
        'display': _('Your password has changed'),
        'description': _('password updated'),
        'email': True,
        'notification': False,
        'toggable': False,
    },
]


def get_notification_type(label):
    for type in NOTIFICATION_TYPES:
        if type['label'] == label:
            return type
