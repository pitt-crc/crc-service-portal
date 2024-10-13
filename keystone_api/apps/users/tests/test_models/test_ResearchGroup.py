"""Unit tests for the `Team` model."""

from django.test import TestCase

from apps.users.models import Team
from apps.users.tests.utils import create_test_user


class GetAllMembers(TestCase):
    """Test fetching all team members via the `get_all_members` method."""

    def setUp(self) -> None:
        """Create temporary user accounts for use in tests."""

        self.pi = create_test_user(username='pi')
        self.admin1 = create_test_user(username='admin1')
        self.admin2 = create_test_user(username='admin2')
        self.member1 = create_test_user(username='unprivileged1')
        self.member2 = create_test_user(username='unprivileged2')

    def test_all_accounts_returned(self) -> None:
        """Test all team members are included in the returned queryset."""

        team = Team.objects.create(pi=self.pi)
        team.admins.add(self.admin1)
        team.admins.add(self.admin2)
        team.members.add(self.member1)
        team.members.add(self.member2)

        expected_members = [self.pi, self.admin1, self.admin2, self.member1, self.member2]

        self.assertQuerySetEqual(
            expected_members,
            team.get_all_members(),
            ordered=False
        )


class GetPrivilegedMembers(TestCase):
    """Test fetching team members via the `get_privileged_members` member."""

    def setUp(self) -> None:
        """Create temporary user accounts for use in tests."""

        self.pi = create_test_user(username='pi')
        self.admin1 = create_test_user(username='admin1')
        self.admin2 = create_test_user(username='admin2')
        self.member1 = create_test_user(username='member1')
        self.member2 = create_test_user(username='member2')

    def test_owner_only(self) -> None:
        """Test returned team members for a team with an owner only."""

        team = Team.objects.create(pi=self.pi)
        expected_members = (self.pi,)
        self.assertQuerySetEqual(expected_members, team.get_privileged_members(), ordered=False)

    def test_pi_with_admins(self) -> None:
        """Test returned team members for a team with an owner and admins."""

        team = Team.objects.create(pi=self.pi)
        team.admins.add(self.admin1)
        team.admins.add(self.admin2)

        expected_members = (self.pi, self.admin1, self.admin2)
        self.assertQuerySetEqual(expected_members, team.get_privileged_members(), ordered=False)

    def test_pi_with_members(self) -> None:
        """Test returned team members for a team with am owner and unprivileged members."""

        team = Team.objects.create(pi=self.pi)
        team.members.add(self.member1)
        team.members.add(self.member2)

        expected_members = (self.pi,)
        self.assertQuerySetEqual(expected_members, team.get_privileged_members(), ordered=False)

    def test_pi_with_admin_and_members(self) -> None:
        """Test returned team members for a team with an owner, admins, and unprivileged members."""

        team = Team.objects.create(pi=self.pi)
        team.admins.add(self.admin1)
        team.admins.add(self.admin2)
        team.members.add(self.member1)
        team.members.add(self.member2)

        expected_members = (self.pi, self.admin1, self.admin2)
        self.assertQuerySetEqual(expected_members, team.get_privileged_members(), ordered=False)
