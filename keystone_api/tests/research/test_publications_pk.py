"""Function tests for the `/research/publications/<pk>/` endpoint."""

import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Permissions depend on whether the user is a member of the record's associated team.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication              | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |-----------------------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous User              | 403 | 403  | 403     | 403  | 403 | 403   | 403    | 403   |
    | User accessing other team   | 404 | 404  | 200     | 405  | 404 | 404   | 404    | 403   |
    | User accessing own team     | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 403   |
    | Staff User                  | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 405   |
    """

    endpoint_pattern = '/research/publications/{pk}/'
    fixtures = ['multi_team.yaml']
    valid_record_data = {
        'title': 'foo',
        'abstract': 'bar',
        'journal': 'baz',
        'date': datetime.date(1990, 1, 1),
        'team': 1}

    def test_anonymous_user_permissions(self) -> None:
        """Test unauthenticated users cannot access resources."""

        endpoint = self.endpoint_pattern.format(pk=1)
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

    def test_authenticated_user_different_team(self) -> None:
        """Test permissions for authenticated users accessing records owned by someone else's team."""

        # Define a user / record endpoint from DIFFERENT teams
        endpoint = self.endpoint_pattern.format(pk=1)
        user = User.objects.get(username='member_2')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            endpoint,
            get=status.HTTP_404_NOT_FOUND,
            head=status.HTTP_404_NOT_FOUND,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_404_NOT_FOUND,
            patch=status.HTTP_404_NOT_FOUND,
            delete=status.HTTP_404_NOT_FOUND,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_authenticated_user_same_team(self) -> None:
        """Test permissions for authenticated users accessing records owned by their team."""

        # Define a user / record endpoint from the SAME teams
        endpoint = self.endpoint_pattern.format(pk=1)
        user = User.objects.get(username='member_1')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_403_FORBIDDEN,
            put_body=self.valid_record_data,
        )

    def test_staff_user_permissions(self) -> None:
        """Test staff users have read and write permissions."""

        endpoint = self.endpoint_pattern.format(pk=1)
        user = User.objects.get(username='staff_user')
        self.client.force_authenticate(user=user)

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
            put_body=self.valid_record_data,
            patch_body={'title': 'New Title'}
        )
