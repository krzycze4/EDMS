from invoices.models import Invoice
from invoices.serializers import InvoiceSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class InvoiceListCreateAPIView(ListCreateAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()


class InvoiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
