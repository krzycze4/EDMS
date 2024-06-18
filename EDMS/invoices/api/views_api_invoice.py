from invoices.api.serializers import InvoiceSerializer
from invoices.models import Invoice
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class InvoiceModelViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = InvoiceSerializer
