from employees.api.serializers import SerializerSerializer
from employees.models.models_salaries import Salary
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class SalaryModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = SerializerSerializer
    queryset = Salary.objects.all()
