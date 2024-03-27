from employees.api.serializers import PaymentSerializer
from employees.models.models_payment import Payment
from rest_framework.viewsets import ModelViewSet


class PaymentModelViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
