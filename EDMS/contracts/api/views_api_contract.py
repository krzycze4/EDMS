from contracts.api.serializers import ContractSerializer
from contracts.models import Contract
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class ContractModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
