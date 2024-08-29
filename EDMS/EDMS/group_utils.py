# ruff: noqa: F821
from typing import List


def create_group_with_permissions(group_name: str, permission_codenames: List[str]) -> "Group":
    """
    Create a group with the specified permissions.

    Args:
        group_name (str): The name of the group to create or update.
        permission_codenames (List[str]): A list of permission codenames to assign to the group.

    Returns:
        Group: The created or updated group with the assigned permissions.
    """
    from django.contrib.auth.models import Group, Permission

    permissions = Permission.objects.filter(codename__in=permission_codenames)
    group, _ = Group.objects.get_or_create(name=group_name)
    group.permissions.add(*permissions)
    return group
