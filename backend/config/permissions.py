from rest_framework.permissions import BasePermission


class IsAdminOrStaff(BasePermission):
    """role が admin または staff のユーザーのみ許可"""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ('admin', 'staff')
        )
