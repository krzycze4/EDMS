from employees.api.serializers import TerminationSerializer
from employees.models.models_termination import Termination
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class TerminationModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = TerminationSerializer
    queryset = Termination.objects.all()
