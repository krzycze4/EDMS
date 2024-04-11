from employees.api.serializers import VacationSerializer
from employees.models.models_vacation import Vacation
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class VacationModelViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()
