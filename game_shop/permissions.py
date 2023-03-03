import jwt
from rest_framework.permissions import SAFE_METHODS, BasePermission

from accounts.models import User, Admin


def get_user_from_token(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return False
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return False
    user = User.objects.get(id=payload['id'])
    return user


class SuperUserOnlyPermissions(BasePermission):

    def has_permission(self, request, view):
        user = get_user_from_token(request=request)
        if not user:
            return False
        else:
            if user.is_superuser:
                return True
            else:
                return False


class ProductAndPostPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            user = get_user_from_token(request=request)
            if not user:
                return False
            else:
                if user.is_superuser:
                    return True
                elif user.is_staff:
                    admin = Admin.objects.get(parent_user=user)
                    return bool(admin.role == 'SM')
                else:
                    return False


class DiscountManagementPermissions(BasePermission):
    def has_permission(self, request, view):
        user = get_user_from_token(request=request)
        if not user:
            return False
        else:
            if user.is_superuser:
                return True
            elif user.is_staff:
                admin = Admin.objects.get(parent_user=user)
                return bool(admin.role == 'SM')
            else:
                return False


class CommentManagementPermissions(BasePermission):
    def has_permission(self, request, view):
        user = get_user_from_token(request=request)
        if not user:
            return False
        else:
            if user.is_superuser:
                return True
            elif user.is_staff:
                admin = Admin.objects.get(parent_user=user)
                return bool(admin.role == 'RM')
            else:
                return False


class UserManagementPermissions(BasePermission):
    def has_permission(self, request, view):
        user = get_user_from_token(request=request)
        if not user:
            return False
        else:
            if user.is_superuser:
                return True
            elif user.is_staff:
                admin = Admin.objects.get(parent_user=user)
                return bool(admin.role == 'UM')
            else:
                return False


class SelfProfilePermissions(BasePermission):
    def has_permission(self, request, view):
        user = get_user_from_token(request=request)
        if not user:
            return False
        else:
            return True
