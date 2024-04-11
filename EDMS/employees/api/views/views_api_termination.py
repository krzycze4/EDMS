from employees.api.serializers import TerminationSerializer
from employees.models.models_termination import Termination
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class TerminationModelViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TerminationSerializer
    queryset = Termination.objects.all()
