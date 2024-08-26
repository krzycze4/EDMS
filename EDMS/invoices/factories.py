import factory
from _decimal import ROUND_HALF_UP, Decimal
from companies.factories import CompanyFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from factory import Sequence
from factory.django import DjangoModelFactory
from invoices.models import Invoice


class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = Invoice

    name = Sequence(lambda n: f"Invoice #{n + 1}")
    seller = factory.SubFactory(CompanyFactory)
    buyer = factory.SubFactory(CompanyFactory)
    net_price = Decimal(6000)
    vat = (net_price * Decimal(0.23)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    gross = (net_price + vat).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    create_date = factory.LazyAttribute(lambda _: timezone.now().date())
    service_date = factory.LazyAttribute(lambda obj: obj.create_date - timezone.timedelta(days=1))
    payment_date = factory.LazyAttribute(lambda obj: obj.create_date + timezone.timedelta(days=30))
    type = Invoice.ORIGINAL
    linked_invoice = None
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )
    is_paid = True
