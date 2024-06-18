from employees.api.serializers import VacationSerializer
from employees.models.models_vacation import Vacation
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class VacationModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()
