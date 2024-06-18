from employees.api.serializers import AddendumSerializer
from employees.models.models_addendum import Addendum
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class AddendumModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = AddendumSerializer
    queryset = Addendum.objects.all()
