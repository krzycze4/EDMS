from common_tests.consts import group_names_with_permission_codenames
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class EDMSTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
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
        group: Group = get_object_or_404(Group, name=group_name)
        user: User = UserFactory(is_active=True, password=cls.password)
        user.groups.add(group)
        return user
