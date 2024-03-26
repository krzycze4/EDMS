from employees.models.models_vacation import Vacation
from employees.serializers import VacationSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class VacationListCreateAPIView(ListCreateAPIView):
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()


class VacationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()
