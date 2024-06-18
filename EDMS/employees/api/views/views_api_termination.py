from employees.api.serializers import TerminationSerializer
from employees.models.models_termination import Termination
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class TerminationModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = TerminationSerializer
    queryset = Termination.objects.all()
