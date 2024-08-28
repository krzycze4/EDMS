from common_tests.consts import group_names_with_permission_codenames
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class EDMSTestCase(TestCase):
    """
    TestCase class for EDMS.

    This class sets up a test environment with predefined user groups and users. It is used to run tests.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up the initial test data for the entire TestCase.

        This method creates the groups with permissions and sets up users with different group memberships.
        The groups are:
        - Accountants
        - CEOs
        - HRs
        - Managers

        It also generates a random password that is shared among all test users.
        """
        super().setUpTestData()
        for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
            create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)

        cls.password: str = User.objects.make_random_password()
        cls.accountant: User = cls.create_user_with_group(group_name="accountants")
        cls.ceo: User = cls.create_user_with_group(group_name="ceos")
        cls.hr: User = cls.create_user_with_group(group_name="hrs")
        cls.manager: User = cls.create_user_with_group(group_name="managers")

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        """
        Create a new user and assign them to a specified group.

        Args:
            group_name (str): The name of the group to which the user should be assigned.

        Returns:
            User: The created user who is assigned to the specified group.
        """
        group: Group = get_object_or_404(Group, name=group_name)
        user: User = UserFactory(is_active=True, password=cls.password)
        user.groups.add(group)
        return user
