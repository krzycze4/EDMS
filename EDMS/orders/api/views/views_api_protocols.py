from orders.api.serializers import ProtocolSerializer
from orders.models import Protocol
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class ProtocolModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = ProtocolSerializer
    queryset = Protocol.objects.all()
