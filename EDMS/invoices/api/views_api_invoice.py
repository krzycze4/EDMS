from invoices.api.serializers import InvoiceSerializer
from invoices.models import Invoice
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class InvoiceModelViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    permission_classes = (DjangoModelPermissions,)
    serializer_class = InvoiceSerializer
