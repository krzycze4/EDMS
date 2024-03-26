from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
