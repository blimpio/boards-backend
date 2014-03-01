from rest_framework import permissions

from ..boards.permissions import BoardPermission, BoardCollaboratorPermission


class CardPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Returns `True` if the user is a board collaborator with
        write permissions trying to create. Returns `True` if
        user is the account owner. Returns `False` if user is not
        authenticated and method is not safe. Returns `True if user
        is not authenticated and view action is `list` and `board`
        query parameter is set, `False` if it's not set.
        """
        is_authenticated = request.user and request.user.is_authenticated()
        is_safe = request.method in permissions.SAFE_METHODS

        if not is_authenticated and not is_safe:
            return False

        if not is_authenticated and view.action == 'list':
            return bool(request.QUERY_PARAMS.get('board'))

        permission = BoardCollaboratorPermission()
        return permission.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if user is a collaborator with the
        corresponding permission on this board, `False` otherwise.
        """
        permission = BoardPermission()

        return permission.has_object_permission(request, view, obj.board)
