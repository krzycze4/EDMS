from django.test import TestCase
from invoices.factories import InvoiceFactory
from invoices.models import Invoice


class InvoiceFactoryTests(TestCase):
    def test_create_correct_object(self):
        InvoiceFactory.create()
        self.assertEqual(Invoice.objects.count(), 1)

    def test_create_correct_object_bulk(self):
        InvoiceFactory.create_batch(10)
        self.assertEqual(Invoice.objects.count(), 10)
