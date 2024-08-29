from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """
    Custom permissions for Django models based on HTTP methods.

    This class maps HTTP methods to model permissions. For example:
    - GET, OPTIONS, HEAD require view permissions.
    - POST requires add permission.
    - PUT and PATCH require change permissions.
    - DELETE requires delete permission.

    Attributes:
        perms_map (dict): A dictionary mapping HTTP methods to permissions.
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
