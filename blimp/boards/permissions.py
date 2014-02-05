from rest_framework import permissions


class BoardPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if user is a collaborator with the
        corresponding permission on this board, `False` otherwise.
        """
        permission = 'read'

        if request.method not in permissions.SAFE_METHODS:
            permission = 'write'

        return obj.is_user_collaborator(request.user, permission=permission)
