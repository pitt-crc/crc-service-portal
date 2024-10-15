"""Application logic for rendering HTML templates and handling HTTP requests.

View objects handle the processing of incoming HTTP requests and return the
appropriately rendered HTML template or other HTTP response.
"""

from rest_framework import permissions, viewsets
from rest_framework.serializers import Serializer

from .models import *
from .permissions import IsTeamAdminOrReadOnly, IsSelfOrReadOnly
from .serializers import *

__all__ = ['TeamViewSet', 'UserViewSet']


class TeamViewSet(viewsets.ModelViewSet):
    """Manage user team membership."""

    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTeamAdminOrReadOnly]
    serializer_class = TeamSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Manage user account data."""

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]

    def get_serializer_class(self) -> type[Serializer]:
        """Return the appropriate data serializer based on user roles/permissions."""

        if self.request.user.is_staff:
            return PrivilegedUserSerializer

        return RestrictedUserSerializer
