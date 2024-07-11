import factory
from _decimal import Decimal
from django.utils import timezone
from employees.models.models_salaries import Salary
from factory.django import DjangoModelFactory
from users.factories import UserFactory


class SalaryFactory(DjangoModelFactory):
    class Meta:
        model = Salary

    date = factory.LazyFunction(lambda: timezone.now().date())
    user = factory.SubFactory(UserFactory)
    fee = Decimal(7000)
