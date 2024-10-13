"""Function tests for the `/research/publications/` endpoint."""

import datetime

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
    | Non-Member     | 200 | 200  | 200     | 403  | 405 | 405   | 405    | 403   |
    | Team Member    | 200 | 200  | 200     | 201  | 405 | 405   | 405    | 403   |
    | Team Admin     | 200 | 200  | 200     | 201  | 405 | 405   | 405    | 403   |
    | Team Owner     | 200 | 200  | 200     | 201  | 405 | 405   | 405    | 403   |
    | Staff User     | 200 | 200  | 200     | 201  | 405 | 405   | 405    | 405   |
    """

    endpoint = '/research/publications/'
    fixtures = ['multi_team.yaml']
    valid_record_data = {
        'title': 'foo',
        'abstract': 'bar',
        'journal': 'baz',
        'date': datetime.date(1990, 1, 1),
        'team': 1}

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

    def test_non_team_member_permissions(self) -> None:
        """Test users have read access but cannot create records for teams where they are not members."""

        user = User.objects.get(username='generic_user')
        self.client.force_authenticate(user=user)

        # Post data reflects a team ID for which the user is not a member
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_403_FORBIDDEN,
            post_body=self.valid_record_data
        )

    def test_team_member_permissions(self) -> None:
        """Test regular team members have read-only access."""

        user = User.objects.get(username='member_1')
        self.client.force_authenticate(user=user)

        # Post data reflects a team ID for which the user is a regular member
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_201_CREATED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_403_FORBIDDEN,
            post_body=self.valid_record_data
        )

    def test_team_admin_permissions(self) -> None:
        """Test team admins have read and write access."""

        user = User.objects.get(username='team_admin_1')
        self.client.force_authenticate(user=user)

        # Post data reflects a team ID for which the user is an admin
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_201_CREATED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_403_FORBIDDEN,
            post_body=self.valid_record_data
        )

    def test_team_owner_permissions(self) -> None:
        """Test team owners have read and write access."""

        user = User.objects.get(username='pi_1')
        self.client.force_authenticate(user=user)

        # Post data reflects a team ID for which the user is a owner
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_201_CREATED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_403_FORBIDDEN,
            post_body=self.valid_record_data
        )

    def test_staff_user(self) -> None:
        """Test staff users have read and write permissions."""

        user = User.objects.get(username='staff_user')
        self.client.force_authenticate(user=user)

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
            post_body=self.valid_record_data
        )
