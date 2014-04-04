from rest_framework import permissions


class AccountPermission(permissions.IsAuthenticated):
    def is_authenticated(self, request):
        return request.user and request.user.is_authenticated()

    def has_permission(self, request, view):
        """
        Returns `True` if the user is authenticated. If the user is
        not authenticated and view.action is `list` or is not safe.
        """
        is_authenticated = self.is_authenticated(request)
        is_safe = request.method in permissions.SAFE_METHODS

        if is_safe and view.action == 'retrieve':
            return True

        if is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if user is a collaborator on
        this account, `False` otherwise.
        """
        is_safe = request.method in permissions.SAFE_METHODS

        if is_safe and view.action == 'retrieve':
            return True

        return obj.is_user_collaborator(request.user)
