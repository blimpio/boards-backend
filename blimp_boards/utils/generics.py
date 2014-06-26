from rest_framework import generics, mixins


from .mixins import UpdateModelMixin


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            UpdateModelMixin,
                            generics.GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
