from companies.api.serializers import CompanySerializer
from companies.models import Company
from rest_framework.viewsets import ModelViewSet


class CompanyModelViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
