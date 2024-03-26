from employees.models.models_termination import Termination
from employees.serializers import TerminationSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class TerminationListCreateAPIView(ListCreateAPIView):
    serializer_class = TerminationSerializer
    queryset = Termination.objects.all()


class TerminationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TerminationSerializer
    queryset = Termination.objects.all()
