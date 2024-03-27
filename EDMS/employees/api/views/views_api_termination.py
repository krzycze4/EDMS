from employees.api.serializers import TerminationSerializer
from employees.models.models_termination import Termination
from rest_framework.viewsets import ModelViewSet


class TerminationModelViewSet(ModelViewSet):
    serializer_class = TerminationSerializer
    queryset = Termination.objects.all()
