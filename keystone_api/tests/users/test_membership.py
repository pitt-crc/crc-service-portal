"""Function tests for the `/users/membership/` endpoint."""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import Team, User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Permissions depend on whether the user is a member of the record's associated team.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication               | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |------------------------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous user              | 403 | 403  | 403     | 403  | 403 | 403   | 403    | 403   |
    | Staff user                  | 200 | 200  | 200     | 201  | 405 | 405   | 405    | 405   |
    """

    endpoint = '/users/membership/'
    fixtures = ['testing_common.yaml']

    def setUp(self) -> None:
        """Load user teams and accounts from testing fixtures."""

        self.staff_user = User.objects.get(username='staff_user')
        self.non_team_member = User.objects.get(username='generic_user')

        # Load user accounts for (non)team members
        self.team = Team.objects.get(name='Team 1')
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

    def test_staff_user_permissions(self) -> None:
        """Test staff users have read and write permissions."""

        self.client.force_authenticate(user=self.staff_user)
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_201_CREATED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
            post_body={'team': self.team.pk, 'user': self.non_team_member.pk, 'role': 'MB'},
        )
