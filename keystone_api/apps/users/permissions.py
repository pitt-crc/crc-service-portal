"""Custom permission objects used to manage access to HTTP endpoints.

Permission classes control access to API resources by determining user
privileges for different HTTP operations. They are applied at the view level,
enabling authentication and authorization to secure endpoints based on
predefined access rules.
"""

from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

__all__ = ['IsStaffOrIsSelf', 'StaffWriteAuthenticatedRead']


class StaffWriteAuthenticatedRead(permissions.BasePermission):
    """Grant read-only access is granted to all authenticated users.

    Staff users retain all read/write permissions.
    """

    def has_permission(self, request, view) -> bool:
        """Return whether the request has permissions to access the requested resource"""

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated


class IsStaffOrIsSelf(permissions.BasePermission):
    """Gives read-only permissions to everyone but limits write access to staff users and record owners"""

    def has_permission(self, request: Request, view: View) -> bool:
        """Return whether the request has permissions to access the requested resource"""

        is_readonly = request.method in permissions.SAFE_METHODS
        return is_readonly or request.user.is_staff

    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        """Return whether the incoming HTTP request has permission to access a database record"""

        is_readonly = request.method in permissions.SAFE_METHODS
        is_record_owner = obj == request.user
        return is_readonly or is_record_owner or request.user.is_staff
