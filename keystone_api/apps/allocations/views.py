"""Application logic for rendering HTML templates and handling HTTP requests.

View objects handle the processing of incoming HTTP requests and return the
appropriately rendered HTML template or other HTTP response.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import *
from .permissions import *
from .serializers import *
from ..users.models import Team

__all__ = [
    'AllocationRequestStatusChoicesView',
    'AllocationRequestViewSet',
    'AllocationReviewStatusChoicesView',
    'AllocationReviewViewSet',
    'AllocationViewSet',
    'AttachmentViewSet',
    'ClusterViewSet'
]


class AllocationRequestStatusChoicesView(GenericAPIView):
    """Exposes valid values for the allocation request `status` field."""

    @extend_schema(responses={'200': dict(AllocationRequest.StatusChoices.choices)})
    def get(self, request, *args, **kwargs) -> Response:
        """Return valid values for the allocation review `status` field."""

        return Response(dict(AllocationRequest.StatusChoices.choices), status=status.HTTP_200_OK)


class AllocationRequestViewSet(viewsets.ModelViewSet):
    """Manage allocation requests."""

    queryset = AllocationRequest.objects.all()
    serializer_class = AllocationRequestSerializer
    permission_classes = [permissions.IsAuthenticated, TeamAdminCreateMemberRead]

    def get_queryset(self) -> list[AllocationRequest]:
        """Return a list of allocation requests for the currently authenticated user."""

        if self.request.user.is_staff:
            return self.queryset

        teams = Team.objects.teams_for_user(self.request.user)
        return AllocationRequest.objects.filter(team__in=teams)


class AllocationReviewStatusChoicesView(GenericAPIView):
    """Exposes valid values for the allocation review `status` field."""

    @extend_schema(responses={'200': dict(AllocationReview.StatusChoices.choices)})
    def get(self, request, *args, **kwargs) -> Response:
        """Return valid values for the allocation review `status` field."""

        return Response(dict(AllocationReview.StatusChoices.choices), status=status.HTTP_200_OK)


class AllocationReviewViewSet(viewsets.ModelViewSet):
    """Manage administrator reviews of allocation requests."""

    queryset = AllocationReview.objects.all()
    serializer_class = AllocationReviewSerializer
    permission_classes = [permissions.IsAuthenticated, StaffWriteMemberRead]

    def get_queryset(self) -> list[Allocation]:
        """Return a list of allocation reviews for the currently authenticated user."""

        if self.request.user.is_staff:
            return self.queryset

        teams = Team.objects.teams_for_user(self.request.user)
        return AllocationReview.objects.filter(request__team__in=teams)

    def create(self, request, *args, **kwargs) -> Response:
        """Create a new `AllocationRequestReview` object."""

        data = request.data.copy()
        data.setdefault('reviewer', request.user.pk)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AllocationViewSet(viewsets.ModelViewSet):
    """Manage HPC resource allocations."""

    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
    permission_classes = [permissions.IsAuthenticated, StaffWriteMemberRead]

    def get_queryset(self) -> list[Allocation]:
        """Return a list of allocations for the currently authenticated user."""

        if self.request.user.is_staff:
            return self.queryset

        teams = Team.objects.teams_for_user(self.request.user)
        return Allocation.objects.filter(request__team__in=teams)


class AttachmentViewSet(viewsets.ModelViewSet):
    """Files submitted as attachments to allocation requests"""

    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated, StaffWriteMemberRead]

    def get_queryset(self) -> list[Allocation]:
        """Return a list of attachments for the currently authenticated user."""

        if self.request.user.is_staff:
            return self.queryset

        teams = Team.objects.teams_for_user(self.request.user)
        return Attachment.objects.filter(request__team__in=teams)


class ClusterViewSet(viewsets.ModelViewSet):
    """Configuration settings for managed Slurm clusters."""

    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = [permissions.IsAuthenticated, StaffWriteAuthenticatedRead]
