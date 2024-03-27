from orders.api.serializers import ProtocolSerializer
from orders.models import Protocol
from rest_framework.viewsets import ModelViewSet


class ProtocolModelViewSet(ModelViewSet):
    serializer_class = ProtocolSerializer
    queryset = Protocol.objects.all()
