# Experimental notifications system

Based on ideas and approaches from:
- pinax/django-notification
- django-notifications/django-notifications

# pinax/django-notification
```
notification.send(users, label, extra_context)
```

# django-notifications
```
notify.send(
    user, recipient=user, verb='replied',
    action_object=comment, description=comment.comment,
    target=comment.content_object)
```


# Combined Approach
NotificationType stores verb.

```
actor = User.objects.first()
recipients = User.objects.all()
label = 'comment_created'
extra_context = {
    'action_object': comment,
    'description': comment.comment,
    'target': comment.content_object
}

notify.send(
    actor, recipients, label, extra_context, override_backends=('email',))
```