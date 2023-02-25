from rest_framework.permissions import SAFE_METHODS, BasePermission


class ProductPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return bool(request.user.is_staff)
