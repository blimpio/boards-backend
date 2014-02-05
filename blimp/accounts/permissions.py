from rest_framework import permissions


class AccountPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if user is a collaborator on
        this account, `False` otherwise.
        """
        return obj.is_user_collaborator(request.user)
