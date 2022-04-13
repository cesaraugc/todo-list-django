from rest_framework import permissions

class CantDeletePermissionClass(permissions.BasePermission):
    SAFE_METHODS = ['GET']
    
    def is_authenticated(self, request):
        return request.user and request.user.is_authenticated

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True
        return self.is_authenticated(request)