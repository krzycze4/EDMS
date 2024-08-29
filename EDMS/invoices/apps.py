from __future__ import annotations

from django.apps import AppConfig

from EDMS.group_utils import create_group_with_permissions


def define_groups(sender, **kwargs):
    """
    Creates user groups and sets group's model permissions from employees app.

    Groups:
    - CEOs,
    - accountants,
    - HRs (exists in project, but doesn't have Invoice permission at all),
    - managers.

    Args:
        sender (Any): The sender of the signal, typically not used in this function.
        **kwargs: Additional keyword arguments passed to the function.

    Returns:
        None: This function does not return anything. It creates groups and sets permissions.
    """
    group_names_with_permission_codenames = {
        "ceos": ["add_invoice", "change_invoice", "delete_invoice", "view_invoice"],
        "accountants": [
            "add_invoice",
            "change_invoice",
            "delete_invoice",
            "view_invoice",
        ],
        "managers": ["view_invoice"],
    }
    for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
        create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)


class InvoicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "invoices"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(define_groups, sender=self)
