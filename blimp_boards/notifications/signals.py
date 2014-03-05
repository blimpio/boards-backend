from django.dispatch import Signal

notify = Signal(providing_args=[
    'actor', 'recipients', 'label', 'extra_context', 'override_backends'
])
