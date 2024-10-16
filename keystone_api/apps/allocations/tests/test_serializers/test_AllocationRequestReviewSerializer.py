"""Unit tests for the `AllocationRequestReviewSerializer` class."""

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from apps.allocations.models import AllocationRequest, AllocationRequestReview
from apps.allocations.serializers import AllocationRequestReviewSerializer
from apps.users.models import Team, User


class Validation(TestCase):
    """Test record validation."""

    def setUp(self) -> None:
        """Create dummy user accounts and test data."""

        self.user = User.objects.create_user(username='testuser', password='foobar123!')
        self.another_user = User.objects.create_user(username='anotheruser', password='foobar123!')

        self.team = Team.objects.create(name='Test Team')
        self.request = AllocationRequest.objects.create(
            title='Test Allocation Request',
            description="This is a test.",
            team=self.team
        )

    def test_reviewer_matches_submitter(self) -> None:
        """Test validation passes when the reviewer is the submitting user."""

        # Create a POST where the submitter matches the reviewer
        post_data = {'request': self.request.id, 'reviewer': self.user.id, 'status': AllocationRequestReview.StatusChoices.APPROVED}
        request = APIRequestFactory().post('/reviews/', post_data)
        request.user = self.user

        serializer = AllocationRequestReviewSerializer(data=post_data, context={'request': request})
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_different_reviewer_from_submitter(self) -> None:
        """Test validation fails when the reviewer is different from the submitting user."""

        # Create a POST where the submitter is different from the reviewer
        post_data = {'request': self.request.id, 'reviewer': self.user.id, 'status': AllocationRequestReview.StatusChoices.APPROVED}
        request = APIRequestFactory().post('/reviews/', post_data)
        request.user = self.another_user

        serializer = AllocationRequestReviewSerializer(data=post_data, context={'request': request})
        with self.assertRaisesRegex(ValidationError, "Reviewer cannot be set to a different user"):
            serializer.is_valid(raise_exception=True)

    def test_reviewer_is_optional(self) -> None:
        """Test the reviewer field is optional."""

        post_data = {'request': self.request.id, 'status': AllocationRequestReview.StatusChoices.APPROVED}
        request = APIRequestFactory().post('/reviews/', post_data)

        serializer = AllocationRequestReviewSerializer(data=post_data, context={'request': request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
