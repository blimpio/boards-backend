notify.send([user, user2], notification_type)


'recipient', 'actor', 'verb', 'action_object', 'target', 'description',
'timestamp'

notify.send(from_user, recipient=to_user, target)
send_now([recipient], 'comment_created')

Developer should be able to trigger notification.
    - Either trigger email or create notification, or both.

notify.send()
notification.send()
email.send()


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