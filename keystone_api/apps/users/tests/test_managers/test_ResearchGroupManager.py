"""Unit tests for the `Team` class."""

from django.test import TestCase

from apps.users.models import Team
from apps.users.tests.utils import create_test_user


class TeamsForUser(TestCase):
    """Test fetching team affiliations via the `teams_for_user` method."""

    def setUp(self):
        """Create temporary users and teams."""

        self.test_user = create_test_user(username='test_user')
        other_user = create_test_user(username='other_user')

        # Team where the test user is an owner
        self.team1 = Team.objects.create(name='Team1', pi=self.test_user)

        # Team where the test user is an admin
        self.team2 = Team.objects.create(name='Team2', pi=other_user)
        self.team2.members.add(self.test_user)

        # Team where the test user is an unprivileged member
        self.team3 = Team.objects.create(name='Team3', pi=other_user)
        self.team3.members.add(self.test_user)

        # Team where the test user has no role
        self.team4 = Team.objects.create(name='Team4', pi=other_user)

    def test_teams_for_user(self) -> None:
        """Test all teams are returned for a test user."""

        result = Team.objects.teams_for_user(self.test_user).all()
        self.assertCountEqual(result, [self.team1, self.team2, self.team3])
