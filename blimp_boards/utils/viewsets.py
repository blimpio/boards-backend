from rest_framework import mixins, viewsets

from .mixins import CreateModelMixin, UpdateModelMixin


class ModelViewSet(CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass


class CreateViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    A viewset that provides only a `create` action.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class CreateListViewSet(CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    A viewset that provides only `create` and `list` actions.

    To use it, override the class and set the  `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class CreateListRetrieveViewSet(CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `create`, `list`, and `retrieve` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class RetrieveUpdateDestroyViewSet(mixins.RetrieveModelMixin,
                                   UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    """
    A viewset that provides default `retrieve()`, `update()`,
    `partial_update()`, and `destroy()` actions.
    """
    pass


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                            UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    A viewset that provides default `retrieve()`, `update()`,
    and `partial_update()` actions.
    """
    pass


class ListRetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                UpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides default `list()`, `retrieve()`,
    `update()`, and `partial_update()` actions.
    """
    pass
