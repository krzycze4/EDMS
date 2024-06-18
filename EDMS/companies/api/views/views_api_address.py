from companies.api.serializers import AddressSerializer
from companies.models import Address
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class AddressModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
