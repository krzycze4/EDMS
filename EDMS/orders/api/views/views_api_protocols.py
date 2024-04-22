from orders.api.serializers import ProtocolSerializer
from orders.models import Protocol
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class ProtocolModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = ProtocolSerializer
    queryset = Protocol.objects.all()
