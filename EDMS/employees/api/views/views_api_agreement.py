from employees.api.serializers import AgreementSerializer
from employees.models.models_agreement import Agreement
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class AgreementModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = AgreementSerializer
    queryset = Agreement.objects.all()
