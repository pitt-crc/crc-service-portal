"""Unit tests for the `WhoAmIView` class."""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication      | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |---------------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous User      | 401 | 401  | 200     | 405  | 405 | 405   | 405    | 405   |
    | Authenticated User  | 200 | 200  | 200     | 405  | 405 | 405   | 405    | 405   |
    """

    endpoint = '/authentication/whoami/'
    fixtures = ['testing_common.yaml']

    def test_user_not_authenticated(self) -> None:
        """Test unauthenticated users cannot access the endpoint."""

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_401_UNAUTHORIZED,
            head=status.HTTP_401_UNAUTHORIZED,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_user_authenticated(self) -> None:
        """Test authenticated users can perform read operations."""

        user = User.objects.get(username='generic_user')
        self.client.force_authenticate(user=user)
        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class UserData(APITestCase):
    """Test the fetching of user metadata."""

    endpoint = '/authentication/whoami/'
    fixtures = ['testing_common.yaml']

    def test_metadata_is_returned(self) -> None:
        """Test GET responses include metadata for the currently authenticated user."""

        user = User.objects.get(username='generic_user')
        self.client.force_authenticate(user=user)

        response = self.client.get(self.endpoint)
        data = response.json()

        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.is_staff, data['is_staff'])
        self.assertEqual(user.is_active, data['is_active'])

    def test_password_is_not_returned(self) -> None:
        """Test the password field is excluded from the returned data."""

        user = User.objects.get(username='generic_user')
        self.client.force_authenticate(user=user)

        response = self.client.get(self.endpoint)
        self.assertNotIn('password', response.json())
