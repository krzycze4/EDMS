from contracts.api.serializers import ContractSerializer
from contracts.models import Contract
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class ContractModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
