from employees.models.models_payment import Payment
from employees.serializers import PaymentSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class PaymentListCreateAPIView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
