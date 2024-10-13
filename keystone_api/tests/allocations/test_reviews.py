"""Function tests for the `/allocations/reviews/` endpoint."""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication      | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |---------------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous User      | 403 | 403  | 403     | 403  | 403 | 403   | 403    | 403   |
    | Authenticated User  | 200 | 200  | 200     | 403  | 403 | 403   | 403    | 403   |
    | Staff User          | 200 | 200  | 200     | 201  | 405 | 405   | 405    | 405   |
    """

    endpoint = '/allocations/reviews/'
    fixtures = ['multi_team.yaml']

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

    def test_authenticated_user_permissions(self) -> None:
        """Test general authenticated users have read-only permissions."""

        user = User.objects.get(username='generic_user')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_staff_user_permissions(self) -> None:
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
            post_body={'status': 'AP', 'request': 1}
        )


class ReviewerAssignment(APITestCase):
    """Test the automatic assignment and verification of the `reviewer` field."""

    endpoint = '/allocations/reviews/'
    fixtures = ['multi_team.yaml']

    def test_default_reviewer(self) -> None:
        """Test the reviewer field defaults to the current user."""

        staff_user = User.objects.get(username='staff_user')
        self.client.force_authenticate(user=staff_user)

        response = self.client.post(self.endpoint, {'request': 1, 'status': 'AP'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(staff_user.id, response.data['reviewer'])

    def test_reviewer_provided(self) -> None:
        """Test the reviewer is set correctly when provided."""

        staff_user = User.objects.get(username='staff_user')
        self.client.force_authenticate(user=staff_user)

        response = self.client.post(self.endpoint, {'request': 1, 'reviewer': staff_user.id, 'status': 'AP'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(staff_user.id, response.data['reviewer'])

    def test_error_when_not_matching_submitter(self) -> None:
        """Test an error is raised when the reviewer field does not match the request submitter."""

        staff_user = User.objects.get(username='staff_user')
        other_user = User.objects.get(username='member_1')
        self.client.force_authenticate(user=staff_user)

        response = self.client.post(self.endpoint, {'request': 1, 'reviewer': other_user.id, 'status': 'AP'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reviewer', response.data)
        self.assertEqual('reviewer cannot be set to a different user than the submitter', response.data['reviewer'][0].lower())
