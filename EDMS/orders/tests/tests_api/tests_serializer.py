from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from orders.api.serializers import OrderSerializer, ProtocolSerializer
from orders.factories import OrderFactory, ProtocolFactory
from orders.models import Order, Protocol
from users.factories import UserFactory


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


class ProtocolSerializerTests(TestCase):
    def setUp(self) -> None:
        user = UserFactory.create()
        order = OrderFactory.create(user=user)
        self.uploaded_file = SimpleUploadedFile(
            name="test_scan.pdf", content=b"This is a test scan content.", content_type="application/pdf"
        )
        self.protocol = ProtocolFactory.build(user=user, order=order, scan=self.uploaded_file)
        self.protocol.save()
        self.protocol.refresh_from_db()
        self.protocol_data = {
            "id": self.protocol.id,
            "name": self.protocol.name,
            "scan": self.protocol.scan.url,
            "create_date": self.protocol.create_date.strftime("%Y-%m-%d"),
            "user": self.protocol.user.pk,
            "order": self.protocol.order.pk,
        }

    def test_object_serialization(self):
        serializer = ProtocolSerializer(instance=self.protocol)
        self.assertEqual(serializer.data, self.protocol_data)

    def test_object_deserialization(self):
        self.protocol.delete()
        valid_data = self.protocol_data.copy()
        fake_file = SimpleUploadedFile(
            name="the_file.pdf", content=b"This is a test pdf file content.", content_type="application/pdf"
        )
        valid_data["scan"] = fake_file
        serializer = ProtocolSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        expected_value = 1
        self.assertEqual(Protocol.objects.count(), expected_value)
