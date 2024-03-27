from invoices.api.serializers import InvoiceSerializer
from invoices.models import Invoice
from rest_framework.viewsets import ModelViewSet


class InvoiceModelViewSet(ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
