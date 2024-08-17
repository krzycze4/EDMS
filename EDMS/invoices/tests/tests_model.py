from companies.factories import CompanyFactory
from django.test import TestCase
from invoices.factories import InvoiceFactory


class InvoiceTests(TestCase):
    def setUp(self) -> None:
        buyer = CompanyFactory.create()
        seller = CompanyFactory.create()
        self.invoice = InvoiceFactory.build(buyer=buyer, seller=seller)

    def test_str_method(self):
        self.assertEqual(str(self.invoice), f"{self.invoice.name}")
