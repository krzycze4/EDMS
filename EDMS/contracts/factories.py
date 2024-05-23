import factory
from _decimal import Decimal
from companies.factories import CompanyFactory
from contracts.models import Contract
from django.utils import timezone
from factory import Sequence
from factory.django import DjangoModelFactory
from users.factories import UserFactory

from EDMS.factory_utils import create_string_format_valid_date

used_numbers = set()


class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract

    name = Sequence(lambda n: f"contract{n}")
    create_date = factory.LazyFunction(
        lambda: create_string_format_valid_date(timezone.now().date().strftime("%Y-%m-%d"))
    )
    start_date = factory.LazyAttribute(lambda obj: create_string_format_valid_date(obj.create_date))
    end_date = factory.LazyAttribute(lambda obj: create_string_format_valid_date(obj.start_date))
    company = factory.SubFactory(CompanyFactory)
    price = Decimal(1000)
    scan = factory.django.FileField(filename="the_file.pdf")

    @factory.post_generation
    def employee(self, create, employees, **kwargs):
        if not create:
            return
        if employees:
            for employee in employees:
                self.employee.add(employee)
        else:
            self.employee.add(UserFactory())
