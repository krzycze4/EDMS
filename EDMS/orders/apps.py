# ruff: noqa: F401
from django.apps import AppConfig

from EDMS.group_utils import create_group_with_permissions


def define_groups(sender, **kwargs):
    group_names_with_permission_codenames = {
        "ceos": ["add_order", "change_order", "delete_order", "view_order"],
        "accountants": ["view_order"],
        "managers": ["add_order", "change_order", "delete_order", "view_order"],
    }
    for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
        create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(define_groups, sender=self)
