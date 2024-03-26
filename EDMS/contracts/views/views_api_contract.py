from contracts.models import Contract
from contracts.serializers import ContractSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ContractListCreateAPIView(ListCreateAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()


class ContractRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
