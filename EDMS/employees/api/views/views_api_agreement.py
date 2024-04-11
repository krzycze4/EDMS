from employees.api.serializers import AgreementSerializer
from employees.models.models_agreement import Agreement
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class AgreementModelViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AgreementSerializer
    queryset = Agreement.objects.all()
