"""Function tests for the `/users/membership/<pk>/` endpoint."""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import Team, User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication                     | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |------------------------------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous user                     | 403 | 403  | 403     | 403  | 403 | 403   | 403    | 403   |
    | User accessing another user        | 200 | 200  | 200     | 405  | 403 | 403   | 403    | 405   |
    | Team member accessing self         | 200 | 200  | 200     | 405  | 403 | 403   | 403    | 405   |
    | Team member accessing other member | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 405   |
    | Team admin accessing other member  | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 405   |
    | Team owner accessing other member  | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 405   |
    | Staff user                         | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 405   |
    """

    endpoint_pattern = '/users/membership/{pk}/'
    fixtures = ['testing_common.yaml']

    def setUp(self) -> None:
        """Load user teams and accounts from testing fixtures."""

        # Define the API endpoint for Team 1
        self.team = Team.objects.get(name='Team 1')
        self.endpoint = self.endpoint_pattern.format(pk=self.team.pk)

        # Load user accounts for (non)team members
        self.staff_user = User.objects.get(username='staff_user')
        self.non_team_member = User.objects.get(username='generic_user')
        self.team_owner = User.objects.get(username='owner_1')
        self.team_admin = User.objects.get(username='admin_1')
        self.team_member = User.objects.get(username='member_1')

    def test_anonymous_user_permissions(self) -> None:
        """Test unauthenticated users cannot access resources."""

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_403_FORBIDDEN,
            head=status.HTTP_403_FORBIDDEN,
            options=status.HTTP_403_FORBIDDEN,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_user_accessing_another_user(self) -> None:
        """Test regular user accessing another user's membership (read-only)."""

        self.client.force_authenticate(user=self.non_team_member)
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_team_member_accessing_self(self) -> None:
        """Test team member accessing their own membership (read-only)."""

        self.client.force_authenticate(user=self.team_member)
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_team_member_accessing_other_member(self) -> None:
        """Test team member accessing another member's details (can update or delete)."""

        self.client.force_authenticate(user=self.team_member)
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_team_admin_accessing_other_member(self) -> None:
        """Test team admin accessing another member's details (can update or delete)."""

        self.client.force_authenticate(user=self.team_admin)
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_team_owner_accessing_other_member(self) -> None:
        """Test team owner accessing another member's details (can update or delete)."""

        self.client.force_authenticate(user=self.team_owner)
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_staff_user_permissions(self) -> None:
        """Test staff users can manage memberships (can update or delete)."""

        self.client.force_authenticate(user=self.staff_user)
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
