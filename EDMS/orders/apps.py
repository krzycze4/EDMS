# ruff: noqa: F401
from django.apps import AppConfig

from EDMS.group_utils import create_group_with_permissions


def define_groups(sender, **kwargs):
    """
    Creates user groups and sets group's model permissions from employees app.

    Groups:
    - CEOs,
    - accountants,
    - HRs (exists in project, but doesn't have Order and Protocol permission at all),
    - managers.

    Args:
        sender (Any): The sender of the signal, typically not used in this function.
        **kwargs: Additional keyword arguments passed to the function.

    Returns:
        None: This function does not return anything. It creates groups and sets permissions.
    """
    group_names_with_permission_codenames = {
        "ceos": [
            "add_order",
            "change_order",
            "delete_order",
            "view_order",
            "add_protocol",
            "change_protocol",
            "delete_protocol",
            "view_protocol",
        ],
        "accountants": ["view_order", "view_protocol"],
        "managers": [
            "add_order",
            "change_order",
            "delete_order",
            "view_order",
            "add_protocol",
            "change_protocol",
            "delete_protocol",
            "view_protocol",
        ],
    }
    for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
        create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(define_groups, sender=self)
