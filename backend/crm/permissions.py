from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow managers to delete objects.
    Agents can read, create, and update but not delete.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions require authentication
        if request.method in ['POST', 'PUT', 'PATCH']:
            return request.user and request.user.is_authenticated
        
        # Delete permissions only for managers
        if request.method == 'DELETE':
            return request.user and request.user.is_authenticated and request.user.is_manager
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require authentication
        if request.method in ['PUT', 'PATCH']:
            return True
        
        # Delete permissions only for managers
        if request.method == 'DELETE':
            return request.user.is_manager
        
        return False


class IsManager(permissions.BasePermission):
    """
    Permission to only allow managers.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_manager

