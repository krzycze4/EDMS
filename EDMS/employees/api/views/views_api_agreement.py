from employees.api.serializers import AgreementSerializer
from employees.models.models_agreement import Agreement
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class AgreementModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = AgreementSerializer
    queryset = Agreement.objects.all()
