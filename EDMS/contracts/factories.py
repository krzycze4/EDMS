import factory
from _decimal import Decimal
from companies.factories import CompanyFactory
from contracts.models import Contract
from factory.django import DjangoModelFactory
from users.factories import UserFactory

from EDMS.factory_utils import draw_unique_random_number

used_numbers = set()


class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract

    name = factory.LazyAttribute(
        lambda _: f"contract{draw_unique_random_number(used_numbers=used_numbers, min_value=1, max_value=100)}"
    )
    create_date = factory.Faker("date")
    start_date = factory.Faker("date")
    end_date = factory.Faker("date")
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
