from decimal import Decimal

import factory
from companies.factories import CompanyFactory
from companies.models import Company
from contracts.factories import ContractFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from factory.django import DjangoModelFactory
from orders.models import Order, Protocol
from users.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    name = factory.LazyAttribute(
        lambda order: f"{order.company.shortcut}-"
        f"{OrderFactory.declare_counter(order.company, order.create_date.month, order.create_date.year)}/"
        f"{order.create_date.month}/"
        f"{order.create_date.year}"
    )
    payment = Decimal(100000.00)
    status = Order.OPEN
    company = factory.SubFactory(CompanyFactory)
    user = factory.SubFactory(UserFactory)
    contract = factory.SubFactory(ContractFactory)
    create_date = timezone.now().date()
    start_date = create_date - timezone.timedelta(days=1)
    end_date = create_date + timezone.timedelta(days=365)
    description = "XYZ"

    @staticmethod
    def declare_counter(company: Company, month: int, year: int):
        # This function should mock the counter logic. For example:
        # Ideally, you'd want to query the number of existing orders for this company,
        # but for simplicity, we'll increment a static variable or use a simple logic.
        return Order.objects.filter(company=company, create_date__month=month, create_date__year=year).count() + 1


class ProtocolFactory(DjangoModelFactory):
    class Meta:
        model = Protocol

    name = "protocol"
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )
    create_date = timezone.now().date()
    user = factory.SubFactory(UserFactory)
    order = factory.SubFactory(OrderFactory)
