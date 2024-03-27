from employees.api.serializers import AgreementSerializer
from employees.models.models_agreement import Agreement
from rest_framework.viewsets import ModelViewSet


class AgreementModelViewSet(ModelViewSet):
    serializer_class = AgreementSerializer
    queryset = Agreement.objects.all()
