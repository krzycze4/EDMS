from django.test import TestCase
from orders.factories import OrderFactory, ProtocolFactory
from orders.models import Order, Protocol


class OrderFactoryTests(TestCase):
    def test_create_correct_object(self):
        OrderFactory.create()
        self.assertEqual(Order.objects.count(), 1)

    def test_create_correct_object_bulk(self):
        OrderFactory.create_batch(10)
        self.assertEqual(Order.objects.count(), 10)


class ProtocolFactoryTests(TestCase):
    def test_create_correct_object(self):
        ProtocolFactory.create()
        self.assertEqual(Protocol.objects.count(), 1)

    def test_create_correct_object_bulk(self):
        ProtocolFactory.create_batch(10)
        self.assertEqual(Protocol.objects.count(), 10)
