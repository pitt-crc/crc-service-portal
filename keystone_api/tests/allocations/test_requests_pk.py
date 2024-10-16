"""Function tests for the `/allocations/requests/<pk>/` endpoint."""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |----------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous User | 403 | 403  | 403     | 403  | 403 | 403   | 403    | 403   |
    | Non-Member     | 404 | 404  | 200     | 403  | 403 | 403   | 403    | 403   |
    | Team Member    | 200 | 200  | 200     | 403  | 403 | 403   | 403    | 403   |
    | Team Admin     | 200 | 200  | 200     | 403  | 403 | 403   | 403    | 403   |
    | Team Owner     | 200 | 200  | 200     | 403  | 403 | 403   | 403    | 403   |
    | Staff User     | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 405   |
    """

    endpoint = '/allocations/requests/1/'
    endpoint_pattern = '/allocations/requests/{pk}/'
    fixtures = ['testing_common.yaml']

    def test_anonymous_user_permissions(self) -> None:
        """Test unauthenticated users cannot access resources."""

        endpoint = self.endpoint.format(pk=1)
        self.assert_http_responses(
            endpoint,
            get=status.HTTP_403_FORBIDDEN,
            head=status.HTTP_403_FORBIDDEN,
            options=status.HTTP_403_FORBIDDEN,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_non_team_member_permissions(self) -> None:
        """Test authenticated users cannot access records for teams where they are not members."""

        self.client.force_authenticate(user=User.objects.get(username='generic_user'))

        endpoint = self.endpoint_pattern.format(pk=1)
        self.assert_http_responses(
            endpoint,
            get=status.HTTP_404_NOT_FOUND,
            head=status.HTTP_404_NOT_FOUND,
            options=status.HTTP_200_OK,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_team_member_permissions(self) -> None:
        """Test regular team members have read-only access."""

        self.client.force_authenticate(user=User.objects.get(username='member_1'))

        endpoint = self.endpoint_pattern.format(pk=1)
        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_team_admin_permissions(self) -> None:
        """Test team admins have read-only access."""

        self.client.force_authenticate(user=User.objects.get(username='team_admin_1'))

        endpoint = self.endpoint_pattern.format(pk=1)
        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_team_owner_permissions(self) -> None:
        """Test team owners have read-only access."""

        self.client.force_authenticate(user=User.objects.get(username='pi_1'))

        endpoint = self.endpoint_pattern.format(pk=1)
        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN,
        )

    def test_staff_user(self) -> None:
        """Test staff users have read and write permissions."""

        user = User.objects.get(username='staff_user')
        self.client.force_authenticate(user=user)

        record_data = {'title': 'foo', 'description': 'bar', 'team': 1}
        endpoint = self.endpoint_pattern.format(pk=1)
        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
            put_body=record_data,
            patch_data=record_data
        )
