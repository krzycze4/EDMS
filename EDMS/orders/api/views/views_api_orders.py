from orders.api.serializers import OrderSerializer
from orders.models import Order
from rest_framework.viewsets import ModelViewSet


class OrderModelViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
