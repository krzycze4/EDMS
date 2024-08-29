from django.apps import AppConfig

from EDMS.group_utils import create_group_with_permissions


def define_groups(sender, **kwargs):
    """
    Creates user groups and sets group's model permissions from companies app.

    Groups:
    - CEOs,
    - accountants,
    - HRs,
    - managers.

    Args:
        sender (Any): The sender of the signal, typically not used in this function.
        **kwargs: Additional keyword arguments passed to the function.

    Returns:
        None: This function does not return anything. It creates groups and sets permissions.
    """
    group_names_with_permission_codenames = {
        "ceos": [
            "add_company",
            "change_company",
            "delete_company",
            "view_company",
            "add_contact",
            "change_contact",
            "delete_contact",
            "add_address",
            "change_address",
            "delete_address",
            "view_address",
        ],
        "accountants": [
            "add_company",
            "change_company",
            "delete_company",
            "view_company",
            "add_contact",
            "change_contact",
            "delete_contact",
            "add_address",
            "change_address",
            "delete_address",
            "view_address",
        ],
        "managers": ["view_company", "add_contact", "view_address"],
        "hrs": ["view_company", "add_contact", "view_address"],
    }
    for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
        create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)


class CompaniesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "companies"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(define_groups, sender=self)
