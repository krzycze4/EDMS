from decimal import Decimal

import factory
from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from factory import Sequence
from factory.django import DjangoModelFactory
from orders.models import Order, Protocol
from users.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    name = Sequence(lambda n: f"Order #{n + 1}")
    payment = Decimal(100000.00)
    status = Order.OPEN
    company = factory.SubFactory(CompanyFactory)
    user = factory.SubFactory(UserFactory)
    contract = factory.SubFactory(ContractFactory)
    create_date = timezone.now().date()
    start_date = create_date - timezone.timedelta(days=1)
    end_date = create_date + timezone.timedelta(days=365)
    description = "XYZ"


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
