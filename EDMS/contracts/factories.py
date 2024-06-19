import secrets
from datetime import timedelta

import factory
from _decimal import Decimal
from companies.factories import CompanyFactory
from contracts.models import Contract
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from factory import Sequence
from factory.django import DjangoModelFactory
from users.factories import UserFactory

from EDMS.factory_utils import create_string_format_valid_date


class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract

    name = Sequence(lambda n: f"contract{n}")
    start_date = factory.LazyAttribute(lambda obj: create_string_format_valid_date(obj.create_date))
    end_date = factory.LazyAttribute(lambda obj: create_string_format_valid_date(obj.start_date))
    company = factory.SubFactory(CompanyFactory)
    price = Decimal(1000)
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )

    @factory.lazy_attribute
    def create_date(self):
        return (timezone.now().date() - timedelta(days=secrets.randbelow(366))).strftime("%Y-%m-%d")

    @factory.post_generation
    def employee(self, create, employees, **kwargs):
        if not create:
            return
        if employees:
            for employee in employees:
                self.employee.add(employee)
        else:
            self.employee.add(UserFactory())
