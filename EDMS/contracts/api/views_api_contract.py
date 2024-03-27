from contracts.api.serializers import ContractSerializer
from contracts.models import Contract
from rest_framework.viewsets import ModelViewSet


class ContractModelViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
