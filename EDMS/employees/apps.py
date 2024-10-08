from django.apps import AppConfig

from EDMS.group_utils import create_group_with_permissions


def define_groups(sender, **kwargs):
    """
    Creates user groups and sets group's model permissions from employees app.

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
            "add_addendum",
            "change_addendum",
            "delete_addendum",
            "view_addendum",
            "add_agreement",
            "change_agreement",
            "delete_agreement",
            "view_agreement",
            "add_salary",
            "change_salary",
            "delete_salary",
            "view_salary",
            "add_termination",
            "change_termination",
            "delete_termination",
            "view_termination",
            "add_vacation",
            "change_vacation",
            "delete_vacation",
            "view_vacation",
            "add_address",
            "change_address",
            "change_user",
        ],
        "accountants": [
            "view_addendum",
            "view_agreement",
            "add_salary",
            "change_salary",
            "delete_salary",
            "view_salary",
            "view_termination",
        ],
        "managers": [
            "view_addendum",
            "view_agreement",
            "view_termination",
            "view_vacation",
        ],
        "hrs": [
            "add_addendum",
            "change_addendum",
            "delete_addendum",
            "view_addendum",
            "add_agreement",
            "change_agreement",
            "delete_agreement",
            "view_agreement",
            "add_salary",
            "change_salary",
            "delete_salary",
            "view_salary",
            "add_termination",
            "change_termination",
            "delete_termination",
            "view_termination",
            "add_vacation",
            "change_vacation",
            "delete_vacation",
            "view_vacation",
            "add_address",
            "change_address",
        ],
    }
    for group_name, permission_codenames in group_names_with_permission_codenames.items():
        create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)


class EmployeesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employees"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(define_groups, sender=self)
