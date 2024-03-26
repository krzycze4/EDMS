from orders.models import Protocol
from orders.serializers import ProtocolSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ProtocolListCreateAPIView(ListCreateAPIView):
    serializer_class = ProtocolSerializer
    queryset = Protocol.objects.all()


class ProtocolRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProtocolSerializer
    queryset = Protocol.objects.all()
