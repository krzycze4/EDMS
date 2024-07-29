from employees.api.serializers import SalarySerializer
from employees.models.models_salaries import Salary
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class SalaryModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = SalarySerializer
    queryset = Salary.objects.all()
