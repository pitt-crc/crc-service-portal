"""Application logic for rendering HTML templates and handling HTTP requests.

View objects handle the processing of incoming HTTP requests and return the
appropriately rendered HTML template or other HTTP response.
"""

from rest_framework import permissions, viewsets
from rest_framework.serializers import Serializer

from .models import *
from .permissions import TeamMembershipPermissions, TeamPermissions, UserPermissions
from .serializers import *

__all__ = ['TeamViewSet', 'TeamMembershipViewSet', 'UserViewSet']


class TeamViewSet(viewsets.ModelViewSet):
    """Manage user teams."""

    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated, TeamPermissions]
    serializer_class = TeamSerializer


class TeamMembershipViewSet(viewsets.ModelViewSet):
    """Manage team membership."""

    queryset = TeamMembership.objects.all()
    permission_classes = [permissions.IsAuthenticated, TeamMembershipPermissions]
    serializer_class = TeamMembershipSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Manage user account data."""

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, UserPermissions]

    def get_serializer_class(self) -> type[Serializer]:
        """Return the appropriate data serializer based on user roles/permissions."""

        # Allow staff users to read/write administrative fields
        if self.request.user.is_staff:
            return PrivilegedUserSerializer

        return RestrictedUserSerializer
