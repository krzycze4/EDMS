import os
from decimal import Decimal

from companies.factories import CompanyFactory
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from invoices.factories import InvoiceFactory
from invoices.forms import InvoiceForm
from invoices.models import Invoice


class InvoiceFormTests(TestCase):
    def setUp(self) -> None:
        self.buyer = CompanyFactory.create(is_mine=True)
        self.seller = CompanyFactory.create(is_mine=False)
        self.invoice = InvoiceFactory.build(buyer=self.buyer, seller=self.seller)

    def test_form_valid(self):
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.seller.pk,
                "buyer": self.buyer.pk,
                "net_price": self.invoice.net_price,
                "vat": self.invoice.vat,
                "gross": self.invoice.gross,
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": self.invoice.type,
                "linked_invoice": "",
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_buyer_is_the_same_as_seller(self):
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.buyer.pk,
                "buyer": self.buyer.pk,
                "net_price": self.invoice.net_price,
                "vat": self.invoice.vat,
                "gross": self.invoice.gross,
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": self.invoice.type,
                "linked_invoice": "",
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("seller", form.errors)
        self.assertIn("The buyer can't be the seller.", form.errors["seller"])

    def test_form_invalid_when_vat_is_too_big(self):
        invalid_vat_percent = Decimal(0.24)
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.seller.pk,
                "buyer": self.buyer.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.net_price * invalid_vat_percent),
                "gross": int(self.invoice.gross),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": self.invoice.type,
                "linked_invoice": "",
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("vat", form.errors)
        self.assertIn("VAT prize can't be bigger than 23% of net price.", form.errors["vat"])

    def test_form_invalid_when_net_plus_vat_not_equal_gross(self):
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.seller.pk,
                "buyer": self.buyer.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross - 1),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": self.invoice.type,
                "linked_invoice": "",
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("gross", form.errors)
        self.assertIn("The net price plus the vat is not equal the gross.", form.errors["gross"])

    def test_from_invalid_when_create_data_is_in_future(self):
        create_date_in_future = timezone.now().date() + timezone.timedelta(days=1)
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.seller.pk,
                "buyer": self.buyer.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross),
                "create_date": create_date_in_future,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": self.invoice.type,
                "linked_invoice": "",
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("create_date", form.errors)
        self.assertIn("You can't create any invoice with a future end_date.", form.errors["create_date"])

    def test_form_invalid_when_payment_date_before_create_date(self):
        payment_date_before_create_date = self.invoice.create_date - timezone.timedelta(days=1)
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.seller.pk,
                "buyer": self.buyer.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": payment_date_before_create_date,
                "type": self.invoice.type,
                "linked_invoice": "",
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("payment_date", form.errors)
        self.assertIn("Salary end_date can't be earlier than create end_date.", form.errors["payment_date"])

    def test_form_invalid_when_buyer_and_seller_not_my_company(self):
        self.buyer.is_mine = False
        self.seller.is_mine = False
        self.buyer.save()
        self.seller.save()
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.seller.pk,
                "buyer": self.buyer.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": self.invoice.type,
                "linked_invoice": "",
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("seller", form.errors)
        self.assertIn(
            "You can't add any invoice not related with our company. Change seller or...", form.errors["seller"]
        )
        self.assertIn("buyer", form.errors)
        self.assertIn("...change buyer to our company.", form.errors["buyer"])

    def test_form_invalid_when_original_invoice_is_linked_to_other_invoice(self):
        linked_invoice_pk = InvoiceFactory.create(type=Invoice.PROFORMA).pk
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.seller.pk,
                "buyer": self.buyer.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": self.invoice.type,
                "linked_invoice": linked_invoice_pk,
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("linked_invoice", form.errors)
        self.assertIn("Original can't be linked to any other invoice.", form.errors["linked_invoice"])

    def test_form_invalid_when_invoice_proforma_not_same_data_as_original(self):
        self.invoice.save()
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.buyer.pk,
                "buyer": self.seller.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": Invoice.PROFORMA,
                "linked_invoice": self.invoice.pk,
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("seller", form.errors)
        self.assertIn("Seller must be the same as in the original.", form.errors["seller"])

    def test_form_invalid_when_invoice_duplicate_not_same_data_as_original(self):
        self.invoice.save()
        different_payment_date = self.invoice.payment_date + timezone.timedelta(days=1)
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.seller.pk,
                "buyer": self.buyer.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": different_payment_date,
                "type": Invoice.DUPLICATE,
                "linked_invoice": self.invoice.pk,
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("payment_date", form.errors)
        self.assertIn("Payment Date must be the same as in the original.", form.errors["payment_date"])

    def test_form_invalid_when_object_scan_extension_is_wrong(self):
        self.invoice.scan = SimpleUploadedFile("test.exe", b"file_content", content_type="application/x-msdownload")
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.buyer.pk,
                "buyer": self.seller.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": self.invoice.type,
                "linked_invoice": self.invoice.pk,
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        valid_extensions = [
            ".pdf",
            ".jpg",
            ".jpeg",
            ".jfif",
            ".pjpeg",
            ".pjp",
            ".png",
            ".svg",
        ]
        valid_extensions_str = ", ".join(valid_extensions)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("scan", form.errors)
        self.assertIn(
            f"Incorrect extensions. Your file extension: {os.path.splitext(self.invoice.scan.name)[1]}. Valid extensions: {valid_extensions_str}",
            form.errors["scan"],
        )

    def test_linked_invoice_queryset_excludes_concerned_invoice(self):
        self.invoice.save()
        form = InvoiceForm(instance=self.invoice)
        queryset = form.fields["linked_invoice"].queryset
        self.assertNotIn(self.invoice, queryset)

    def test_form_invalid_when_correcting_invoice_linked_to_proforma_invoice(self):
        proforma = InvoiceFactory.create(type=Invoice.PROFORMA)
        form = InvoiceForm(
            data={
                "name": self.invoice.name,
                "seller": self.buyer.pk,
                "buyer": self.seller.pk,
                "net_price": int(self.invoice.net_price),
                "vat": int(self.invoice.vat),
                "gross": int(self.invoice.gross),
                "create_date": self.invoice.create_date,
                "service_date": self.invoice.service_date,
                "payment_date": self.invoice.payment_date,
                "type": Invoice.CORRECTING,
                "linked_invoice": proforma.pk,
                "scan": self.invoice.scan,
                "is_paid": self.invoice.is_paid,
            },
            files={"scan": self.invoice.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("linked_invoice", form.errors)
        self.assertIn(
            "Correcting invoice must be linked to duplicate or original invoice.", form.errors["linked_invoice"]
        )
