"""Unit tests for the `AllocationRequestReview` class."""

from django.test import TestCase

from apps.allocations.models import AllocationRequest, AllocationRequestReview
from apps.users.models import Team, User


class TeamInterface(TestCase):
    """Test the implementation of methods required by the `RGModelInterface`."""

    def setUp(self) -> None:
        """Create mock user records"""

        # Create a Team instance
        self.user = User.objects.create_user(username='pi', password='foobar123!')
        self.team = Team.objects.create(name='Test Team')

        # Create an AllocationRequest instance linked to the team
        self.allocation_request = AllocationRequest.objects.create(
            title='Test Request',
            description='A test description',
            team=self.team
        )

        # Create an AllocationRequestReview instance linked to the AllocationRequest
        self.reviewer = User.objects.create_user(username='reviewer', password='foobar123!')
        self.allocation_request_review = AllocationRequestReview.objects.create(
            status=AllocationRequestReview.StatusChoices.APPROVED,
            request=self.allocation_request,
            reviewer=self.reviewer
        )

    def test_get_team(self):
        """Test the `get_team` method returns the correct `team`."""

        team = self.allocation_request_review.get_team()
        self.assertEqual(team, self.team)
