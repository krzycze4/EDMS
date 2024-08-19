from datetime import timedelta
from decimal import Decimal

import factory
from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from django.utils import timezone
from factory import Sequence
from factory.django import DjangoModelFactory
from invoices.factories import InvoiceFactory
from orders.models import Order
from users.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    name = Sequence(lambda n: f"Order #{n + 1}")
    payment = Decimal(100000)
    status = Order.OPEN
    company = factory.SubFactory(CompanyFactory)
    user = factory.SubFactory(UserFactory)
    contract = factory.SubFactory(ContractFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now().date())
    start_date = factory.LazyAttribute(lambda obj: obj.create_date - timedelta(days=1))
    end_date = factory.LazyAttribute(lambda obj: obj.create_date + timedelta(days=365))
    description = "XYZ"

    @factory.post_generation
    def income_invoice(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for invoice in extracted:
                self.income_invoice.add(invoice)

        else:
            invoice = InvoiceFactory()
            self.income_invoice.add(invoice)

    @factory.post_generation
    def cost_invoice(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for invoice in extracted:
                self.cost_invoice.add(invoice)

        else:
            invoice = InvoiceFactory()
            self.cost_invoice.add(invoice)
