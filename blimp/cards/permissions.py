from rest_framework import permissions

from ..boards.permissions import BoardPermission, BoardCollaboratorPermission


class CardPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        """
        Returns `True` if the user is a board collaborator with
        write permissions trying to create. Returns `True` if
        user is the account owner.
        """
        permission = BoardCollaboratorPermission()

        return permission.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if user is a collaborator with the
        corresponding permission on this board, `False` otherwise.
        """
        permission = BoardPermission()

        return permission.has_object_permission(request, view, obj.board)
