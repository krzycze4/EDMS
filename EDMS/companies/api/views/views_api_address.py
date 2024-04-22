from companies.api.serializers import AddressSerializer
from companies.models import Address
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class AddressModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
