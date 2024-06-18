from orders.api.serializers import OrderSerializer
from orders.models import Order
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class OrderModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
