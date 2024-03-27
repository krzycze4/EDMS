from employees.api.serializers import VacationSerializer
from employees.models.models_vacation import Vacation
from rest_framework.viewsets import ModelViewSet


class VacationModelViewSet(ModelViewSet):
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()
