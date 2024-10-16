"""Function tests for the `/health/` endpoint."""

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from apps.users.models import User


class EndpointPermissions(APITransactionTestCase):
    """Test endpoint user permissions.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication      | GET     | HEAD     | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |---------------------|---------|----------|---------|------|-----|-------|--------|-------|
    | Anonymous User      | 200/500 | 200/500  | 200/500 | 405  | 405 | 405   | 405    | 405   |
    | Authenticated User  | 200/500 | 200/500  | 200/500 | 405  | 405 | 405   | 405    | 405   |
    | Staff User          | 200/500 | 200/500  | 200/500 | 405  | 405 | 405   | 405    | 405   |
    """

    endpoint = '/health/'
    fixtures = ['testing_common.yaml']
    valid_responses = (status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def setUp(self) -> None:
        """Load user accounts from testing fixtures."""

        self.staff_user = User.objects.get(username='staff_user')
        self.generic_user = User.objects.get(username='generic_user')

    def assert_read_only_responses(self) -> None:
        """Assert the currently authenticated user has read only permissions."""

        self.assertIn(self.client.get(self.endpoint).status_code, self.valid_responses)
        self.assertIn(self.client.head(self.endpoint).status_code, self.valid_responses)
        self.assertIn(self.client.options(self.endpoint).status_code, self.valid_responses)

        self.assertEqual(self.client.post(self.endpoint).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.put(self.endpoint).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.patch(self.endpoint).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(self.endpoint).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.trace(self.endpoint).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_anonymous_user_permissions(self) -> None:
        """Test unauthenticated users have read-only permissions."""

        self.assert_read_only_responses()

    def test_authenticated_user_permissions(self) -> None:
        """Test authenticated users have read-only permissions."""

        self.client.force_authenticate(user=self.generic_user)
        self.assert_read_only_responses()

    def test_staff_user_permissions(self) -> None:
        """Test staff users have read-only permissions."""

        self.client.force_authenticate(user=self.staff_user)
        self.assert_read_only_responses()
