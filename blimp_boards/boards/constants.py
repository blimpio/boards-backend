READ_PERMISSION = 'read'
WRITE_PERMISSION = 'write'

PERMISSION_CHOICES = (
    (READ_PERMISSION, 'Read'),
    (WRITE_PERMISSION, 'Read and Write'),
)


BOARD_RESERVED_KEYWORDS = (
    'settings', 'project', 'user', 'add_person',
    'remove_person', 'projects', 'people', 'users', 'guest', 'guests',
    'notifications', 'notification', 'resend_invite', 'cancel_invite',
    'basecamp', 'trello', 'asana', 'calendar', 'tasks', '-'
)
