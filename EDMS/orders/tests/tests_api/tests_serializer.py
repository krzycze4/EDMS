from django.test import TestCase
from orders.api.serializers import OrderSerializer
from orders.factories import OrderFactory
from orders.models import Order


class InvoiceSerializerTests(TestCase):
    def setUp(self) -> None:
        self.order = OrderFactory.create()
        self.order_data = {
            "id": self.order.id,
            "name": self.order.name,
            "payment": f"{self.order.payment:.2f}",
            "status": self.order.status,
            "company": self.order.company.pk,
            "income_invoice": [invoice.pk for invoice in self.order.income_invoice.all()],
            "cost_invoice": [invoice.pk for invoice in self.order.cost_invoice.all()],
            "user": self.order.user.pk,
            "contract": self.order.contract.pk,
            "create_date": self.order.create_date.strftime("%Y-%m-%d"),
            "start_date": self.order.start_date.strftime("%Y-%m-%d"),
            "end_date": self.order.end_date.strftime("%Y-%m-%d"),
            "description": self.order.description,
        }

    def test_object_serialization(self):
        serializer = OrderSerializer(instance=self.order)
        self.assertEqual(serializer.data, self.order_data)

    def test_object_deserialization(self):
        self.order.delete()
        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        expected_value = 1
        self.assertEqual(Order.objects.count(), expected_value)
