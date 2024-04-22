from companies.api.serializers import CompanySerializer
from companies.models import Company
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class CompanyModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
