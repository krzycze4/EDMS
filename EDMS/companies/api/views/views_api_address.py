from companies.api.serializers import AddressSerializer
from companies.models import Address
from rest_framework.viewsets import ModelViewSet


class AddressModelViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
