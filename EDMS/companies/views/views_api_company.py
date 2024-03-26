from companies.models import Company
from companies.serializers import CompanySerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class CompanyListCreateAPIView(ListCreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class CompanyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
