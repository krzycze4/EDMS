from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from invoices.api.serializers import InvoiceSerializer
from invoices.factories import InvoiceFactory
from invoices.models import Invoice


class InvoiceSerializerTests(TestCase):
    def setUp(self) -> None:
        self.invoice = InvoiceFactory.create()
        self.invoice_data = {
            "id": self.invoice.id,
            "name": self.invoice.name,
            "seller": self.invoice.seller.pk,
            "buyer": self.invoice.buyer.pk,
            "net_price": "{:.2f}".format(self.invoice.net_price),
            "vat": "{:.2f}".format(self.invoice.vat),
            "gross": "{:.2f}".format(self.invoice.gross),
            "create_date": self.invoice.create_date.strftime("%Y-%m-%d"),
            "service_date": self.invoice.service_date.strftime("%Y-%m-%d"),
            "payment_date": self.invoice.payment_date.strftime("%Y-%m-%d"),
            "type": self.invoice.type,
            "linked_invoice": None,
            "scan": self.invoice.scan.url,
            "is_paid": self.invoice.is_paid,
        }

    def test_object_serialization(self):
        serializer = InvoiceSerializer(instance=self.invoice)
        self.assertEqual(serializer.data, self.invoice_data)

    def test_object_deserialization(self):
        self.invoice.delete()

        valid_invoice_data = self.invoice_data.copy()
        valid_invoice_data["net_price"] = str(valid_invoice_data["net_price"])
        valid_invoice_data["vat"] = str(valid_invoice_data["vat"])
        valid_invoice_data["gross"] = str(valid_invoice_data["gross"])

        fake_file = SimpleUploadedFile(
            name="the_file.pdf", content=b"This is a test pdf file content.", content_type="application/pdf"
        )
        valid_invoice_data["scan"] = fake_file

        serializer = InvoiceSerializer(data=valid_invoice_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        expected_value = 1
        self.assertEqual(Invoice.objects.count(), expected_value)
