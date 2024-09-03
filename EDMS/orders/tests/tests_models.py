from contracts.factories import ContractFactory
from django.test import TestCase
from orders.factories import OrderFactory, ProtocolFactory
from orders.models import Order
from users.factories import UserFactory


class ProtocolTests(TestCase):
    def setUp(self) -> None:
        self.protocol = ProtocolFactory.build()

    def test_str_method(self):
        self.assertEqual(str(self.protocol), self.protocol.name)


class OrderTests(TestCase):
    def setUp(self) -> None:
        self.contract = ContractFactory.create()
        user = UserFactory()
        self.order = OrderFactory.build(company=self.contract.company, user=user, contract=self.contract)

    def test_str_method(self):
        self.assertEqual(str(self.order), self.order.name)

    def test_save_method(self):
        counter = Order.declare_counter(
            self.order, current_month=self.order.create_date.month, current_year=self.order.create_date.year
        )
        self.order.save()
        self.assertEqual(
            self.order.name,
            f"{self.contract.company.shortcut}-{counter}/{self.order.create_date.month}/"
            f"{self.order.create_date.year}",
        )
