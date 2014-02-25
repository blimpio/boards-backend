import inspect
from functools import wraps

from django.db.models import signals


def autoconnect(cls):
    """
    From: https://djangosnippets.org/snippets/2124/

    Class decorator that automatically connects all model signals on
    a model class to methods named like the signals. Note that the
    instance keyword argument will be available as self. All other
    arguments like sender, created, etc. are also sent as keyword arguments.

    @autoconnect
    class Thing(models.Model):
        title = models.CharField()

        def pre_save(self, **kwargs):
            pass

        def post_save(self, **kwargs):
            pass
    """
    is_signal = lambda x: isinstance(x, signals.Signal)
    model_signals = inspect.getmembers(signals, is_signal)

    def connect(signal, func):
        cls.func = staticmethod(func)

        @wraps(func)
        def wrapper(sender, **kwargs):
            instance = kwargs.pop('instance')
            return func(instance, **kwargs)
        signal.connect(wrapper, sender=cls)
        return wrapper

    for (name, method) in model_signals:
        if hasattr(cls, name):
            setattr(cls, name, connect(method, getattr(cls, name)))

    return cls
