from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customers to access the view.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'customer')
        )
