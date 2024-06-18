from companies.api.serializers import CompanySerializer
from companies.models import Company
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class CompanyModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
